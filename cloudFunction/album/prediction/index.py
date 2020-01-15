import os
import json
import time
import jieba.analyse
import cv2 as cv
import tensorflow as tf
from PIL import Image
from config import Config
from model import CaptionGenerator
from dataset import prepare_test_data
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

try:
    import cosClient
    import returnCommon
    from mysqlCommon import mysqlCommon
except:
    import common.testCommon

    common.testCommon.setEnv()

    import common.cosClient as cosClient
    import common.returnCommon as returnCommon
    from common.mysqlCommon import mysqlCommon

mysql = mysqlCommon()

config = Config()
config.phase = False
config.train_cnn = False
config.beam_size = 3
config.batch_size = 1
config.test_image_dir = "/tmp/images/prediction/"


def FromJieba(text, keywords_type, keywords_num):
    if keywords_type == "tfidf":
        return jieba.analyse.extract_tags(text, topK=keywords_num)
    elif keywords_type == "textrank":
        return jieba.analyse.textrank(text, topK=keywords_num)


def getChinese(English):
    try:
        cred = credential.Credential(os.environ.get('tencent_secret_id'), os.environ.get('tencent_secret_key'))
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tmt_client.TmtClient(cred, "ap-chengdu", clientProfile)

        req = models.TextTranslateRequest()
        params = '{"SourceText":"%s","Source":"en","Target":"zh","ProjectId":0}' % English
        req.from_json_string(params)

        resp = client.TextTranslate(req)
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        print(err)
        return False


def PNG_JPG(PngPath, JpgPath):
    img = cv.imread(PngPath, 0)
    w, h = img.shape[::-1]
    infile = PngPath
    outfile = JpgPath
    img = Image.open(infile)
    img = img.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile, quality=70)
            os.remove(PngPath)
        else:
            img.convert('RGB').save(outfile, quality=70)
            os.remove(PngPath)
        return outfile
    except Exception as e:
        print(e)
        return False


def main_handler(event, context):
    photoList = mysql.getPhotoInforPrediction()
    if photoList:
        json_data = photoList[0]
        photo_dict = photoList[1]

        for eve_file in ["289999.json", "289999.npy", "289999.txt"]:
            cosClient.download2disk("others/" + eve_file, '/tmp/' + eve_file)

        temp_path = "/tmp/images/"
        if not os.path.exists(temp_path + "temp/"):
            os.makedirs(temp_path + "temp/")
        if not os.path.exists(temp_path + "prediction/"):
            os.makedirs(temp_path + "prediction/")

        print("Save File To System")

        for eve_pic_infor in json_data:
            if eve_pic_infor["type"] == "png":
                cosClient.download2disk(eve_pic_infor["pic"], '/tmp/images/temp/' + eve_pic_infor["name"])
                PngPath = temp_path + "temp/%s" % (eve_pic_infor["name"])
                PNG_JPG(PngPath, os.path.splitext(PngPath)[0] + ".jpg")
            else:
                cosClient.download2disk(eve_pic_infor["pic"], "/tmp/images/prediction/" + eve_pic_infor["name"])

        tf.reset_default_graph()
        with tf.Session() as sess:
            data, vocabulary = prepare_test_data(config)
            model = CaptionGenerator(config)
            model.load(sess, "/tmp/289999.npy")
            tf.get_default_graph().finalize()
            file_list, caption = model.prediction(sess, data, vocabulary)
            caption_data = [{
                "file": file_list[i],
                "caption": caption[i]
            } for i in range(0, len(file_list))]

        try:
            for eve in caption_data:
                english = eve['caption']
                try:
                    chinese = json.loads(getChinese(english))["TargetText"]
                    time.sleep(0.2)
                except:
                    chinese = None
                remark = chinese if chinese else english
                tags = FromJieba(chinese, "textrank", 3) if chinese else "-"
                filename = eve['file'].split("/", )[-1]
                mysql.saveToPhotoDB(tags, remark, photo_dict[filename])
                for eve in tags:
                    mysql.saveToTagsDB(eve)
                    tag = mysql.getTags(eve)
                    if tag:
                        mysql.saveToPhotoTagsDB(tag, photo_dict[filename])

        except Exception as e:
            print(e)

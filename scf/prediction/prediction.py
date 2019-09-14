#!/usr/bin/python
import tensorflow as tf
import os, json
from config import Config
from model import CaptionGenerator
from dataset import prepare_test_data
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError
from PIL import Image
import cv2 as cv
import tensorflow as tf

appid = "1256773370"  # 请替换为您的 APPID
secret_id = "切换为自己的腾讯云SecreetId"  # 请替换为您的 SecretId
secret_key = "切换为自己的腾讯云SecreetKey"  # 请替换为您的 SecretKey
region = u'ap-guangzhou'  # 请替换为您bucket 所在的地域
token = ''
to_bucket = 'album-1256773370'  # 请替换为您用于存放压缩后图片的bucket

config = CosConfig(
    Secret_id=secret_id,
    Secret_key=secret_key,
    Region=region,
    Token=token
)
client = CosS3Client(config)

config = Config()
config.phase = False
config.train_cnn = False
config.beam_size = 3
config.batch_size = 1
config.test_image_dir = "/tmp/images/prediction/"


def PNG_JPG(PngPath, JpgPath):
    img = cv.imread(PngPath, 0)
    w, h = img.shape[::-1]
    infile = PngPath
    outfile = JpgPath
    img = Image.open(infile)
    img = img.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
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
    # print(event)

    # json_data = json.loads(event["queryString"]["pic_list"])
    json_data = json.loads(
        '[{"pid": 85, "pic": "large/5c46f1460ebd1f87d05c3d3704e0f614.jpg", "name": "5c46f1460ebd1f87d05c3d3704e0f614.jpg", "type": "jpg"}]')

    for eve_file in ["289999.json", "289999.npy", "289999.txt"]:
        response = client.get_object(
            Bucket="album-1256773370",
            Key="others/" + eve_file,
        )
        response['Body'].get_stream_to_file('/tmp/' + eve_file)

    temp_path = "/tmp/images/"
    os.makedirs(temp_path + "temp/")
    os.makedirs(temp_path + "prediction/")

    print("Save File To System")
    for eve_pic_infor in json_data:
        print("--------")
        print(eve_pic_infor)
        print("--------")
        if eve_pic_infor["type"] == "png":
            response = client.get_object(
                Bucket="album-1256773370",
                Key=eve_pic_infor["pic"],
            )
            response['Body'].get_stream_to_file('/tmp/images/temp/' + eve_pic_infor["name"])
            PngPath = temp_path + "temp/%s" % (eve_pic_infor["name"])
            PNG_JPG(PngPath, os.path.splitext(PngPath)[0] + ".jpg")
        else:
            response = client.get_object(
                Bucket="album-1256773370",
                Key=eve_pic_infor["pic"],
            )
            response['Body'].get_stream_to_file("/tmp/images/prediction/" + eve_pic_infor["name"])

    with tf.Session() as sess:
        # testing phase
        data, vocabulary = prepare_test_data(config)
        model = CaptionGenerator(config)
        model.load(sess, "/tmp/289999.npy")
        tf.get_default_graph().finalize()
        file_list, caption = model.prediction(sess, data, vocabulary)
        print(file_list)
        print(caption)
        result = []
        for i in range(0, len(file_list)):
            print(i)
            result.append(
                {
                    "file": file_list[i],
                    "caption": caption[i]
                }
            )

    result = json.dumps(result, ensure_ascii=False)
    return result


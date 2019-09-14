# -*- coding: utf-8 -*-
from imageai.Prediction import ImagePrediction
from imageai.Detection import ObjectDetection
import urllib.parse
import os
import base64
import json
import hashlib
import PIL.Image as image
import imghdr
import pymysql
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError


connection = pymysql.connect(host="切换为自己的数据库host",
                             user="root",
                             password="切换为自己的数据库密码",
                             port=int(62580),
                             db="mini_album",
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=1)

class ImageHandle:

    # 等比例压缩图片
    def resizeImg(self, **args):
        # try:
        args_key = {'ori_img': '', 'dst_img': '', 'dst_w': '', 'dst_h': '', 'save_q': 75}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]

        im = image.open(arg['ori_img'])
        ori_w, ori_h = im.size
        widthRatio = heightRatio = None
        ratio = 1

        if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
            if arg['dst_w'] and ori_w > arg['dst_w']:
                widthRatio = float(arg['dst_w']) / ori_w  # 正确获取小数的方式
            if arg['dst_h'] and ori_h > arg['dst_h']:
                heightRatio = float(arg['dst_h']) / ori_h

            if widthRatio and heightRatio:
                if widthRatio < heightRatio:
                    ratio = widthRatio
                else:
                    ratio = heightRatio

            if widthRatio and not heightRatio:
                ratio = widthRatio
            if heightRatio and not widthRatio:
                ratio = heightRatio

            newWidth = int(ori_w * ratio)
            newHeight = int(ori_h * ratio)
        else:
            newWidth = ori_w
            newHeight = ori_h
        im.resize((newWidth, newHeight), image.ANTIALIAS).save(arg['dst_img'], quality=arg['save_q'])

        '''
        image.ANTIALIAS还有如下值：
        NEAREST: use nearest neighbour
        BILINEAR: linear interpolation in a 2x2 environment
        BICUBIC:cubic spline interpolation in a 4x4 environment
        ANTIALIAS:best down-sizing filter
        '''
        # except Exception as e:
        #     errorLogger(e)

    def getExecutionPath(self):
        return os.getcwd()

    def getMd5(self, strData):
        m = hashlib.md5()
        m.update(strData)
        return m.hexdigest()

    def objectDetection(self, pathInputData):

        self.type = imghdr.what(pathInputData)
        if self.type == "jpeg":
            self.type = "jpg"
        if self.type not in ["jpg", "png"]:
            return None

        tempData = pathInputData[0:-4]

        pathOutputData = tempData + "out." + self.type
        zhuanhuanPic = tempData + "zh." + self.type

        # 目标图片大小
        dst_w = 400
        dst_h = 0
        # #保存的图片质量
        save_q = 40
        # 等比例压缩

        try:
            img = image.open(pathInputData)
            bg = image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, img)
            bg.save(pathInputData)
        except:
            pass

        self.resizeImg(ori_img=pathInputData,
                       dst_img=zhuanhuanPic,
                       dst_w=dst_w,
                       dst_h=dst_h,
                       save_q=save_q)

        try:
            detector = ObjectDetection()
            detector.setModelTypeAsRetinaNet()
            detector.setModelPath(os.path.join(self.getExecutionPath(),
                                               "/tmp/resnet50_coco_best_v2.0.1.h5"))
            detector.loadModel()
            detections = detector.detectObjectsFromImage(input_image=zhuanhuanPic,
                                                         output_image_path=pathOutputData)

            with open(pathOutputData, "rb") as f:
                # b64encode是编码，b64decode是解码
                base64_data = base64.b64encode(f.read()).decode("utf-8")

            result = []
            for eachObject in detections:
                result.append(eachObject["name"] + " : " + eachObject["percentage_probability"])

            return json.dumps({
                "result": result})
        except Exception as e:
            print(e)
            return False


def ana_picture(path):
    imageData = ImageHandle()
    result = imageData.objectDetection(path)
    return result


def main_handler(event, context):
    print("下载h5文件")
    secret_id = "切换为自己的腾讯云SecreetId"
    secret_key = "切换为自己的腾讯云SecreetKey"
    appid = "1256773370"  # 请替换为您的 APPID
    region = u'ap-guangzhou'  # 请替换为您bucket 所在的地域
    config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region)
    client = CosS3Client(config)

    response = client.get_object(Bucket='album-1256773370',
                                 Key='others/resnet50_coco_best_v2.0.1.h5', )
    response['Body'].get_stream_to_file('/tmp/resnet50_coco_best_v2.0.1.h5')
    response = client.get_object(Bucket='album-1256773370',
                                 Key='others/resnet50_weights_tf_dim_ordering_tf_kernels.h5', )
    response['Body'].get_stream_to_file('/tmp/resnet50_weights_tf_dim_ordering_tf_kernels.h5')

    key = str(event["key"]).encode("utf-8").decode('unicode_escape')
    new_key = key.replace("large/", "")
    download_path = '/tmp/{}'.format(new_key)

    response = client.get_object(Bucket="album-1256773370",
                                 Key=key, )
    response['Body'].get_stream_to_file(download_path)

    print("开始预测")

    print(ana_picture(download_path))

    try:
        connection.close()
    except:
        pass
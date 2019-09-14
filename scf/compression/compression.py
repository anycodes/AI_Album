# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError
from tencentserverless.scf import Client
from tencentserverless.exception import TencentServerlessSDKException
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
import pymysql

# from qcloud_cos import CosConfig
# from qcloud_cos import CosS3Client
# from qcloud_cos import CosServiceError
# from qcloud_cos import CosClientError

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

response = client.get_object(
    Bucket="album-1256773370",
    Key="watermarket/font.ttf",
)
response['Body'].get_stream_to_file('/tmp/font.ttf')

connection = pymysql.connect(host="切换为自己的数据库host",
                             user="root",
                             password="切换为自己的数据库密码",
                             port=int(62580),
                             db="mini_album",
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=1)


# 把图片长、宽压缩至原有图片的1/2
def resize_image(image_path, resized_path):
    try:
        with Image.open(image_path) as image:
            width, height = image.size
            temp = 500 / width
            new_heigh = temp * height
            image.thumbnail((500, new_heigh))
            try:
                image.save(resized_path)
            except Exception as e:
                print("error: ", e)
                try:
                    image = image.convert("RGBA")
                    image.save(resized_path)
                except Exception as e:
                    print("error: ", e)
                    image = image.convert("RGB")
                    image.save(resized_path)

    except Exception as e:
        print("error: ", e)


def add_word(pic_path, save_path):
    # 打开图片
    im = Image.open(pic_path).convert('RGBA')
    # 新建一个空白图片,尺寸与打开图片一样
    txt = Image.new('RGBA', im.size, (0, 0, 0, 0))
    # 设置字体
    fnt = ImageFont.truetype("/tmp/font.ttf", 40)
    # 操作新建的空白图片>>将新建的图片添入画板
    d = ImageDraw.Draw(txt)
    # 在新建的图片上添加字体
    d.text(
        (txt.size[0] - 220, txt.size[1] - 80),
        "Watermarking",
        font=fnt,
        fill=(255, 255, 255, 255)
    )
    # 合并两个图片
    out = Image.alpha_composite(im, txt)
    # 保存图像
    out.save(save_path)


def updatePhotoInfor(connection, large, small):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        update_stmt = (
            "UPDATE `photo` SET `small` = %s  WHERE `photo`.`large` = %s "
        )
        data = (small, large)
        cursor.execute(update_stmt, data)
        print(cursor.rowcount)
        cursor.close()
        return True
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    for record in event['Records']:
        try:
            bucket = record['cos']['cosBucket']['name'] + '-' + str(appid)
            key = record['cos']['cosObject']['key']
            key = key.replace(
                '/' + str(appid) + '/' + record['cos']['cosBucket']['name'] + '/',
                '',
                1
            )
            new_key = key.replace("large/", "")
            download_path = '/tmp/{}'.format(new_key)
            upload_path = '/tmp/new_pic-{}'.format(new_key)

            print(key)

            # 下载图片
            try:
                response = client.get_object(Bucket=bucket, Key=key, )
                response['Body'].get_stream_to_file(download_path)

                # 图像增加水印
                resize_image(download_path, upload_path)

                # 专线调用 生成tags
                # scf = Client(secret_id="切换为自己的腾讯云SecreetId",
                #              secret_key="切换为自己的腾讯云SecreetKey", region="ap-guangzhou")
                # scf.invoke('get_tags', namespace="album", data={"key": key})

                small = key.replace("large/", "small/")
                updatePhotoInfor(connection, key, small)
                # 图像上传
                client.put_object_from_local_file(
                    Bucket=to_bucket,
                    LocalFilePath=upload_path,
                    Key=small
                )
            except CosServiceError as e:
                print(e.get_error_code())
                print(e.get_error_msg())
                print(e.get_resource_location())
        except Exception as e:
            print(e)
    try:
        connection.close()
    except:
        pass
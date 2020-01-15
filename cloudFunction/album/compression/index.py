# -*- coding: utf8 -*-

import os
import json
from PIL import Image, ImageFont, ImageDraw

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


# 把图片长、宽压缩
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


def main_handler(event, context):
    for record in event['Records']:
        try:
            key = record['cos']['cosObject']['key'].replace(
                '/' + str(os.environ.get('tencent_appid')) + '/' + record['cos']['cosBucket']['name'] + '/',
                '',
                1
            )
            new_key = key.replace("large/", "")
            download_path = '/tmp/{}'.format(new_key)
            upload_path = '/tmp/new_pic-{}'.format(new_key)

            cosClient.download2disk(key, download_path)
            resize_image(download_path, upload_path)
            small = key.replace("large/", "small/")
            mysql.updatePhotoInfor(key, small)
            cosClient.upload2Cos(upload_path, small)
        except Exception as e:
            print(e)

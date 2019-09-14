# -*- coding: utf8 -*-

import pymysql
import json
import base64
import urllib.parse
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError
import hashlib
import os
import datetime
import random

connection = pymysql.connect(host="切换为自己的数据库host",
                             user="root",
                             password="切换为自己的数据库密码",
                             port=int(62580),
                             db="mini_album",
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=1)


def getFileMd5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()


def getFileKey(md5):
    random_data = str(random.randint(0, 10000))
    m = hashlib.md5()
    m.update((md5 + random_data).encode())
    return m.hexdigest()


def getUserInfor(connection, wecaht):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `users` WHERE `wechat`=%s"
        )
        data = (wecaht)
        cursor.execute(search_stmt, data)
        cursor.close()
        result = cursor.fetchall()
        if len(result) == 1:
            result = result[0]
            print(result)
            return result['uid']
        else:
            return False
    except Exception as e:
        print("getUserInfor", e)
        try:
            cursor.close()
        except:
            pass
        return False


def getAlbumInfor(connection, user, album):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `user` = %s AND `cid` = %s"
        )
        data = (user, album)
        cursor.execute(search_stmt, data)
        cursor.close()
        result = cursor.fetchall()
        if len(result) == 1:
            return result[0]["cid"]
        else:
            return False
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def savePicture(base64data):
    try:
        imgdata = base64.b64decode(urllib.parse.unquote(base64data))
        file = open('/tmp/picture.png', 'wb')
        file.write(imgdata)
        file.close()
        return True
    except Exception as e:
        print(e)
        return False


def upload2Cos(file='/tmp/picture.png', type="png"):
    try:
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
        name = getFileKey(getFileMd5(file)) + "." + type
        path = "large/" + name
        response = client.put_object_from_local_file(
            Bucket=to_bucket,
            LocalFilePath=file,
            Key=path
        )
        print(response)
        return (path, name)
    except Exception as e:
        print(e)
        return False


def save2Db(name, large, category, user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        insert_stmt = (
            "INSERT INTO `photo` (`name`, `large`, `category`, `creattime`, `creatarea`, `small`, `tags`, `remark`, `user`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        )
        data = (name, large, category, datetime.datetime.now(), "-", "-", "-", "-", user)
        cursor.execute(insert_stmt, data)
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
    try:
        body = json.loads(event['body'])
        wecaht = body['wechat']
        cid = body['cid']
        base64data = body['base64']
        type_data = body['type']
        index = body['index']
        if not cid:
            result = False
            msg = "获取相册信息异常，请重新选择相册"
        elif not wecaht:
            result = False
            msg = "请使用微信小程序登陆本页面"
        elif not base64data:
            result = False
            msg = "获取图片信息异常，请重新选择图像上传"
        else:
            user = getUserInfor(connection, wecaht)
            if user:
                album = getAlbumInfor(connection, user, cid)
                if album:
                    save_result = savePicture(base64data)
                    if save_result:
                        upload_result = upload2Cos(file='/tmp/picture.png', type=type_data)
                        if not upload_result:
                            result = False
                            msg = "图像上传COS失败，请稍后重试"
                        else:
                            if save2Db(upload_result[1], upload_result[0], str(album), user):
                                result = True
                                msg = "上传成功"
                            else:
                                result = False
                                msg = "图像存储数据库失败，请稍后重试"
                    else:
                        result = False
                        msg = "图像存储服务端失败，请稍后重试"
                else:
                    result = False
                    msg = "获取相册信息异常，请重新选择相册"
            else:
                result = False
                msg = "用户信息异常，请联系管理员处理"
    except Exception as e:
        result = False
        msg = "操作异常，请联系管理员处理"

    try:
        connection.close()
    except:
        pass

    return {
        "result": result,
        "msg": msg,
        "index": int(index)
    }

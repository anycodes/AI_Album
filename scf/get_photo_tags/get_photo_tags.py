# -*- coding: utf8 -*-

import pymysql
import json
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


def getUrl(key):
    try:
        response = client.get_presigned_url(
            Method='GET',
            Bucket='album-1256773370',
            Key=key
        )
        return response
    except:
        return "https://album-1256773370.cos.ap-guangzhou.myqcloud.com/" + key


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


def getPhotoList(tags):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            '''SELECT * FROM photo WHERE pid IN (SELECT photo FROM (SELECT tid FROM tags WHERE name=%s) t '''
            '''LEFT JOIN photo_tags pt ON pt.tag=t.tid)'''
        )
        print(search_stmt)
        data = (tags)
        cursor.execute(search_stmt, data)
        result = cursor.fetchall()
        cursor.close()
        result_list = []
        for eve in result:
            large_pic = eve["large"]
            small_pic = large_pic if eve["small"] == "-" else eve["small"]
            result_list.append(
                {
                    "pid": eve["pid"],
                    "url": getUrl(small_pic),
                    "url_large": getUrl(large_pic),
                    "tags": eve["remark"],
                }
            )
        return result_list
    except Exception as e:
        print("getPhotoList", e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    try:
        body = json.loads(event['body'])
        wecaht = body['wechat']
        tags = body['tags']
        if not wecaht:
            result = False
            msg = "请使用微信小程序登陆本页面"
        elif not tags:
            result = False
            msg = "标签不可为空"
        else:
            user = getUserInfor(connection, wecaht)
            if user:
                result = {
                    "pic": getPhotoList(tags)
                }
                msg = "查询成功"
            else:
                result = False
                msg = "用户信息异常，请联系管理员处理"
    except Exception as e:
        print(e)
        result = False
        msg = "操作异常，请联系管理员处理"
    return {
        "result": result,
        "msg": msg,
    }

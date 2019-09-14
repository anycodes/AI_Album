# -*- coding: utf8 -*-

import pymysql
import json
import jieba, pymysql
from gensim import corpora, models, similarities
from collections import defaultdict
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

def getReasultList(sentence, remarks, count=100):
    documents = []
    for eve_sentence in remarks:
        tempData = " ".join(jieba.cut(eve_sentence))
        documents.append(tempData)
    texts = [[word for word in document.split()] for document in documents]
    frequency = defaultdict(int)
    for text in texts:
        for word in text:
            frequency[word] += 1
    dictionary = corpora.Dictionary(texts)
    new_xs = dictionary.doc2bow(jieba.cut(sentence))
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    featurenum = len(dictionary.token2id.keys())
    sim = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featurenum)[tfidf[new_xs]]
    tempList = [(sim[i], remarks[i]) for i in range(0, len(remarks))]

    tempList.sort(key=lambda x: x[0], reverse=True)
    if len(tempList) >= count:
        return tempList[0:count]
    else:
        return tempList


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


def getPhotoList(user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            '''SELECT * FROM `photo` WHERE user=%s'''
        )
        print(search_stmt)
        data = (user)
        cursor.execute(search_stmt, data)
        result = cursor.fetchall()
        cursor.close()
        result_list = []
        for eve in result:
            print(eve)
            large_pic = eve["large"]
            small_pic = large_pic if eve["small"] == "-" else eve["small"]
            result_list.append(
                {
                    "pid": eve["pid"],
                    "url": getUrl(small_pic),
                    "url_large": getUrl(large_pic),
                    "tags": eve["remark"],
                    "remark": eve["remark"]
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
        search = body['search']
        if not wecaht:
            result = False
            msg = "请使用微信小程序登陆本页面"
        elif not search:
            result = False
            msg = "请输入要搜索的内容"
        else:
            user = getUserInfor(connection, wecaht)
            if user:
                photo_list = getPhotoList(user)
                photo_dict = {}
                temp_list = []
                for eve_infor in photo_list:
                    if eve_infor["remark"] not in photo_dict:
                        photo_dict[eve_infor["remark"]] = []
                    photo_dict[eve_infor["remark"]].append(eve_infor)
                    temp_list.append(eve_infor["remark"])

                print(photo_dict)
                print(temp_list)

                result = []
                for eve_result in getReasultList(search, temp_list, count=100):
                    for eve_data in photo_dict[eve_result[1]]:
                        result.append(eve_data)
                result = {
                    "pic": result
                }
                msg = "获取成功"

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

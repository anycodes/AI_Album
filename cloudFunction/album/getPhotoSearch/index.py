# -*- coding: utf8 -*-

import json
import jieba
from gensim import corpora, models, similarities
from collections import defaultdict

try:
    import returnCommon
    from mysqlCommon import mysqlCommon
except:
    import common.testCommon

    common.testCommon.setEnv()

    import common.returnCommon as returnCommon
    from common.mysqlCommon import mysqlCommon

mysql = mysqlCommon()


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


def main_handler(event, context):
    try:
        print(event)

        body = json.loads(event['body'])

        wecaht = body['wechat']
        search = body['search']

        if not wecaht:
            return returnCommon.return_msg(True, "请使用微信小程序登陆本页面。")
        if not search:
            return returnCommon.return_msg(True, "服务异常，请稍后再试")

        user = mysql.getUserInfor(wecaht)
        if user:
            photo_list = mysql.getPhotoListUser(user)
            photo_dict = {}
            temp_list = []
            for eve_infor in photo_list:
                if eve_infor["remark"] not in photo_dict:
                    photo_dict[eve_infor["remark"]] = []
                photo_dict[eve_infor["remark"]].append(eve_infor)
                temp_list.append(eve_infor["remark"])
            result = []
            for eve_result in getReasultList(search, temp_list, count=100):
                for eve_data in photo_dict[eve_result[1]]:
                    result.append(eve_data)
            return returnCommon.return_msg(False, {"pic": result})
    except Exception as e:
        print(e)
    return returnCommon.return_msg(True, "用户信息异常，请联系管理员处理")


def test():
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": json.dumps({
            "wechat": "12345",
            "search": "test",
        }),
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))


if __name__ == "__main__":
    test()

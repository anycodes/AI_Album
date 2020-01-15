# -*- coding: utf8 -*-

import json
import base64
import urllib.parse

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


def main_handler(event, context):
    try:
        print(event)

        body = json.loads(event['body'])

        wecaht = body['wechat']
        cid = body['cid']
        base64data = body['base64']
        type_data = body['type']
        index = body['index']

        if not wecaht:
            return returnCommon.return_msg(True, {"msg": "请使用微信小程序登陆本页面。", "index": int(index)})
        if not cid:
            return returnCommon.return_msg(True, {"msg": "获取相册信息异常，请重新选择相册。", "index": int(index)})
        if not base64data:
            return returnCommon.return_msg(True, {"msg": "获取图片信息异常，请重新选择图像上传。", "index": int(index)})

        user = mysql.getUserInfor(wecaht)
        if user:
            album = mysql.getAlbumInfor(user, cid)["cid"]
            if album:
                save_result = savePicture(base64data)
                if save_result:
                    upload_result = cosClient.upload2Cos(file='/tmp/picture.png', type=type_data)
                    if not upload_result:
                        return returnCommon.return_msg(True, {"msg": "图像上传COS失败，请稍后重试。", "index": int(index)})
                    else:
                        if mysql.save2Db(upload_result[1], upload_result[0], str(album), user):
                            return returnCommon.return_msg(False, {"msg": "上传成功", "index": int(index)})
                        return returnCommon.return_msg(True, {"msg": "图像存储数据库失败，请稍后重试。", "index": int(index)})
                return returnCommon.return_msg(True, {"msg": "图像存储服务端失败，请稍后重试。", "index": int(index)})
            return returnCommon.return_msg(True, {"msg": "获取相册信息异常，请重新选择相册。", "index": int(index)})
    except Exception as e:
        print(e)
    return returnCommon.return_msg(True, {"msg": "用户信息异常，请联系管理员处理。", "index": int(index)})


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
            "cid": "1",
            "base64data": "aaa",
            "type_data": "1"
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

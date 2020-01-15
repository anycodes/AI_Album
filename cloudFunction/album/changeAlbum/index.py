# -*- coding: utf8 -*-

import json

try:
    import returnCommon
    from mysqlCommon import mysqlCommon
except:
    import common.testCommon

    common.testCommon.setEnv()

    import common.returnCommon as returnCommon
    from common.mysqlCommon import mysqlCommon

mysql = mysqlCommon()


def main_handler(event, context):
    try:
        print(event)

        body = json.loads(event['body'])

        wecaht = body['wechat']
        name = body['name']
        sorted = body['sorted']
        remark = body['remark']
        area = body['area']
        cid = body['cid']

        if not wecaht:
            return returnCommon.return_msg(True, "请使用微信小程序登陆本页面。")
        if not name or not cid:
            return returnCommon.return_msg(True, "服务异常，请稍后再试")

        user_infor = mysql.getUserInfor(wecaht)
        if user_infor != False:
            infor = mysql.getAlbumInforCid(cid, user_infor)
            if infor:
                if infor != name:
                    length = mysql.getAlbumInforName(name, user_infor)
                    if length != 0:
                        return returnCommon.return_msg(True, "相册名重复，请更换相册名")
                change_result = mysql.updateAlbumInfor(name, sorted, cid, remark, area)
                if change_result:
                    return returnCommon.return_msg(False, "修改成功")
                return returnCommon.return_msg(True, "修改失败，请稍后再试")
            return returnCommon.return_msg(True, "相册不存在，请按照规范操作")
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
            "name": "test_album_changed",
            "sorted": "1",
            "area": "jilin",
            "remark": "",
            "cid": "1"
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

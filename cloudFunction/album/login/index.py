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
        nickname = body['nickname']
        remark = str(body['remark'])

        if not wecaht:
            return returnCommon.return_msg(True, "请使用微信小程序登陆本页面。")

        if not mysql.getUserInfor(wecaht):
            if not nickname:
                return returnCommon.return_msg(True, "参数异常，请重试。")
            if mysql.addUserInfor(wecaht, nickname, remark):
                return returnCommon.return_msg(False, "注册成功")
            return returnCommon.return_msg(True, "注册失败，请重试。")
        return returnCommon.return_msg(False, "登录成功")
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
            "nickname": "test",
            "remark": "",
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

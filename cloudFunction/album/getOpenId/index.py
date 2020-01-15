# -*- coding: utf8 -*-
import os
import json
import urllib.request
import urllib.parse

try:
    import returnCommon
except:
    import common.testCommon

    common.testCommon.setEnv()

    import common.returnCommon as returnCommon

AppId = os.environ.get('mini_program_app_id')
AppSecret = os.environ.get('mini_program_app_secret')


def main_handler(event, context):
    try:
        url = "https://api.weixin.qq.com/sns/jscode2session"
        data = {
            'appid': AppId,
            'secret': AppSecret,
            'js_code': json.loads(event["body"])["code"],
            'grant_type': 'authorization_code'
        }
        post_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url=url, data=post_data)
        resp = urllib.request.urlopen(req).read().decode("utf-8")
        try:
            return returnCommon.return_msg(False, {"openid": json.loads(resp)["openid"]})
        except:
            return returnCommon.return_msg(True, "获取OpenId失败")
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
            "code": "12345"
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

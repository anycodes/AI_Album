# -*- coding: utf8 -*-
import urllib.request
import urllib.parse
import json

AppId = 'appid'
AppSecret = 'appsecret'

def main_handler(event, context):
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
        return {
            "openid": json.loads(resp)["openid"],
        }
    except:
        return {
            "openid": False
        }

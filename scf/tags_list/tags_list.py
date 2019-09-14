# -*- coding: utf8 -*-

import pymysql
import json
import random

connection = pymysql.connect(host="切换为自己的数据库host",
                             user="root",
                             password="切换为自己的数据库密码",
                             port=int(62580),
                             db="mini_album",
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=1)


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


def getTagsList(uid):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT name FROM tags WHERE tid IN (SELECT DISTINCT pt.tag FROM (SELECT pid FROM photo WHERE user=%s) p "
            "LEFT JOIN photo_tags pt ON pt.photo=p.pid)"
        )
        print(search_stmt)
        data = (uid)
        cursor.execute(search_stmt, data)
        cursor.close()
        tags_list = []
        temp_list = []
        temp_length = 0
        for eve_tag in cursor.fetchall():
            print(eve_tag)
            temp_list.append(eve_tag['name'])
            temp_length = temp_length + len(eve_tag['name'])
            status = random.choice((True, True, False, False, False))
            if (status and len(temp_list) >= 2) or len(temp_list) > 4 or temp_length > 10:
                tags_list.append(temp_list)
                temp_list = []
                temp_length = 0
        tags_list.append(temp_list)
        return tags_list
    except Exception as e:
        print("getTagsList", e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    try:
        body = json.loads(event['body'])
        wecaht = body['wechat']
        if not wecaht:
            result = False
            msg = "请使用微信小程序登陆本页面"
        else:
            user = getUserInfor(connection, wecaht)
            if user:
                result = getTagsList(user)
                msg = "查询成功"
            else:
                result = False
                msg = "用户信息异常，请联系管理员处理"
    except Exception as e:
        print(e)
        result = False
        msg = "操作异常，请联系管理员处理"

    try:
        connection.close()
    except:
        pass

    return {
        "result": result,
        "msg": msg,
    }

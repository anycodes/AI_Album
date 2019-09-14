# -*- coding: utf8 -*-

import pymysql
import json

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
        return len(result)
    except Exception as e:
        print("getUserInfor", e)
        try:
            cursor.close()
        except:
            pass
        return False

def addUseerInfor(connection, wecaht, nickname, remark):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        insert_stmt = (
            "INSERT INTO users(wechat,nickname,remark) "
            "VALUES (%s,%s,%s)"
        )
        data = (wecaht, nickname, remark)
        cursor.execute(insert_stmt, data)
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(e)
        cursor.close()
        connection.close()
        return False


def main_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    wecaht = body['wechat']
    nickname = body['nickname']
    remark = str(body['remark'])

    if getUserInfor(connection, wecaht) == 0:
        if addUseerInfor(connection, wecaht, nickname, remark):
            result = True
        else:
            result = False
    else:
        result = True

    return {
        "result": result
    }

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
        if len(result) == 1:
            result = result[0]
            print(result)
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


def getAlbumInfor(connection, user, album):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `user` = %s AND `cid` = %s"
        )
        data = (user, album)
        cursor.execute(search_stmt, data)
        cursor.close()
        result = cursor.fetchall()
        if len(result) == 1:
            return {
                "name": result[0]["name"],
                "creattime": str(result[0]["publish"]),
                "creatarea": result[0]["area"],
                "remark": result[0]["remark"],
                "cid": result[0]["cid"],
            }
        else:
            return False
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    try:
        print(event)
        body = json.loads(event['body'])
        wecaht = body['wechat']
        cid = body['cid']
        user = getUserInfor(connection, wecaht)
        result = getAlbumInfor(connection, user, cid)
    except Exception as e:
        print(e)
        result = []
    return result

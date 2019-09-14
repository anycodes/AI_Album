# -*- coding: utf8 -*-

import pymysql
import json
import datetime

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


def deleteAlbum(connection, cid, user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        delete_stmt = (
            "DELETE FROM `category` WHERE `category`.`cid` = %s AND `user`=%s"
        )
        data = (cid, user)
        cursor.execute(delete_stmt, data)
        print(cursor.rowcount)
        cursor.close()
        return True
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def deletePhoto(connection, cid):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        delete_stmt = (
            "DELETE FROM photo WHERE category=%s"
        )
        data = (cid)
        cursor.execute(delete_stmt, data)
        print(cursor.rowcount)
        cursor.close()
        return True
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def deletePhotoTags(connection, cid):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        delete_stmt = (
            "DELETE FROM photo_tags WHERE photo in (SELECT pid FROM photo WHERE category=%s)"
        )
        data = (cid)
        cursor.execute(delete_stmt, data)
        print(cursor.rowcount)
        cursor.close()
        return True
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    wecaht = body['wechat']
    cid = body['cid']

    if not wecaht:
        result = False
        msg = "请使用微信小程序登陆本页面"
    elif not cid:
        result = False
        msg = "服务异常，请稍后再试"
    else:
        user_infor = getUserInfor(connection, wecaht)
        if user_infor != False:
            # user_infor = int(user_infor)
            if deleteAlbum(connection, cid, user_infor):
                deletePhoto(connection, cid)
                deletePhotoTags(connection, cid)
                result = True
                msg = "删除成功"
            else:
                result = False
                msg = "操作异常，请按照规范操作"
        else:
            result = False
            msg = "用户信息异常，请联系管理员处理"

    try:
        connection.close()
    except:
        pass
    return {
        "result": result,
        "msg": msg
    }

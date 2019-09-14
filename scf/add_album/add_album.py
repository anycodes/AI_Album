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
                             )
connection.autocommit(1)


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


def getAlbumInfor(connection, name, user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `name` = %s AND `user` = %s"
        )
        data = (name, user)
        cursor.execute(search_stmt, data)
        cursor.close()
        return len(cursor.fetchall())
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def addAlbumInfor(connection, name, sorted, user, remark, area):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        insert_stmt = (
            "INSERT INTO `category` (`name`, `sorted`, `user`, `remark`, `publish`, `area`) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
        )
        data = (name, sorted, user, remark, datetime.datetime.now(), area)
        cursor.execute(insert_stmt, data)
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
    name = body['name']
    sorted = body['sorted']
    remark = body['remark']
    area = body['area']

    if not wecaht:
        result = False
        msg = "请使用微信小程序登陆本页面"
    elif not name:
        result = False
        msg = "服务异常，请稍后再试"
    else:
        user_infor = getUserInfor(connection, wecaht)
        if user_infor != False:
            # user_infor = int(user_infor)
            if getAlbumInfor(connection, name, user_infor) == 0:
                add_result = addAlbumInfor(connection, name, sorted, user_infor, remark, area)
                if add_result:
                    result = True
                    msg = "添加成功"
                else:
                    result = False
                    msg = "添加失败，请稍后再试"
            else:
                result = False
                msg = "相册重复，请更换名称"
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

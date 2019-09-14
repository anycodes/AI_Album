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


def getAlbumInforCid(connection, cid, user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `cid` = %s AND `user` = %s"
        )
        data = (cid, user)
        cursor.execute(search_stmt, data)
        cursor.close()
        result = cursor.fetchall()
        if len(result) == 1:
            return result[0]['name']
        else:
            return False
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def getAlbumInforName(connection, name, user):
    try:
        print(name, user)
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `name` = %s AND `user` = %s "
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


def updateAlbumInfor(connection, name, sorted, cid, remark, area):
    try:
        print(cid)
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        update_stmt = (
            "UPDATE `category` SET `name` = %s, `sorted` = %s, `remark` = %s, `area` = %s WHERE `category`.`cid` = %s "
        )
        data = (name, sorted, remark, area, cid)
        cursor.execute(update_stmt, data)
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
    name = body['name']
    sorted = body['sorted']
    remark = body['remark']
    area = body['area']
    cid = body['cid']

    if not wecaht:
        result = False
        msg = "请使用微信小程序登陆本页面"
    elif not name or not cid:
        result = False
        msg = "服务异常，请稍后再试"
    else:
        user_infor = getUserInfor(connection, wecaht)
        if user_infor != False:
            # user_infor = int(user_infor)
            infor = getAlbumInforCid(connection, cid, user_infor)
            print(infor)
            if infor:
                status = True
                if infor != name:
                    length = getAlbumInforName(connection, name, user_infor)
                    print(length)
                    if length != 0:
                        status = False
                        result = False
                        msg = "相册名重复，请更换相册名"
                if status:
                    change_result = updateAlbumInfor(connection, name, sorted, cid, remark, area)
                    if change_result:
                        result = True
                        msg = "修改成功"
                    else:
                        result = False
                        msg = "修改失败，请稍后再试"
            else:
                result = False
                msg = "相册不存在，请按照规范操作"
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

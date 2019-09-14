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


def getPhotoInfor(connection, album):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `photo` WHERE `category` = %s "
        )
        data = (album)
        cursor.execute(search_stmt, data)
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
            small_data = result[0]["large"] if result[0]["small"] == "-" else result[0]["small"]
            return "https://album-1256773370.cos.ap-guangzhou.myqcloud.com/" + small_data
        else:
            return "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1364033727,724695302&fm=26&gp=0.jpg"
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1364033727,724695302&fm=26&gp=0.jpg"


def getAlbumInfor(connection, user):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `category` WHERE `user` = %s"
        )
        print(search_stmt)
        data = (user)
        cursor.execute(search_stmt, data)
        cursor.close()
        temp_list = []

        for eve in cursor.fetchall():
            print(eve)
            temp_list.append(
                {
                    "name": eve["name"],
                    "creattime": str(eve["publish"]),
                    "creatarea": eve["area"],
                    "remark": eve["remark"],
                    "cid": eve["cid"],
                    "url": getPhotoInfor(connection, eve["cid"])
                }
            )
        return temp_list
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
        user = getUserInfor(connection, wecaht)
        result = getAlbumInfor(connection, user)
        temp = []
        for eve in result:
            temp.append(eve['name'])
        result = {
            "list_data": temp,
            "result_data": result
        }
    except Exception as e:
        print(e)
        result = []

    try:
        connection.close()
    except:
        pass

    return result

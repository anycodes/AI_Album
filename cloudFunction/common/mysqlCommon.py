# -*- coding: utf8 -*-

import os
import random
import pymysql
import datetime

try:
    import cosClient
except:
    import common.cosClient as cosClient


class mysqlCommon:
    def __init__(self):
        self.getConnection({
            "host": os.environ.get('mysql_host'),
            "user": os.environ.get('mysql_user'),
            "port": int(os.environ.get('mysql_port')),
            "db": os.environ.get('mysql_db'),
            "password": os.environ.get('mysql_password')
        })

    def getConnection(self, conf):
        self.connection = pymysql.connect(host=conf['host'],
                                          user=conf['user'],
                                          password=conf['password'],
                                          port=int(conf['port']),
                                          db=conf['db'],
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=1)

    def doAction(self, stmt, data):
        try:
            self.connection.ping(reconnect=True)
            cursor = self.connection.cursor()
            cursor.execute(stmt, data)
            result = cursor
            cursor.close()
            return result
        except Exception as e:
            print(e)
            try:
                cursor.close()
            except:
                pass
            return False

    def addUserInfor(self, wecaht, nickname, remark):
        insert_stmt = (
            "INSERT INTO users(wechat, nickname, remark) "
            "VALUES (%s,%s,%s)"
        )
        data = (wecaht, nickname, remark)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

    def getUserInfor(self, wecaht):
        search_stmt = (
            "SELECT * FROM `users` WHERE `wechat`=%s"
        )
        data = (wecaht)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        result = result.fetchall()
        return result[0]['uid'] if len(result) == 1 else False

    def addAlbumInfor(self, name, sorted, user, remark, area):
        insert_stmt = (
            "INSERT INTO `category` (`name`, `sorted`, `user`, `remark`, `publish`, `area`) "
            "VALUES (%s, %s, %s, %s, %s, %s) "
        )
        data = (name, sorted, user, remark, datetime.datetime.now(), area)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

    def getAlbumInforCid(self, cid, user):
        search_stmt = (
            "SELECT * FROM `category` WHERE `cid` = %s AND `user` = %s"
        )
        data = (cid, user)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        result = result.fetchall()
        return result[0]['name'] if len(result) == 1 else False

    def getAlbumInforName(self, name, user):
        search_stmt = (
            "SELECT * FROM `category` WHERE `name` = %s AND `user` = %s "
        )
        data = (name, user)
        result = self.doAction(search_stmt, data)
        return False if result == False else len(result.fetchall())

    def updateAlbumInfor(self, name, sorted, cid, remark, area):
        update_stmt = (
            "UPDATE `category` SET `name` = %s, `sorted` = %s, `remark` = %s, `area` = %s WHERE `category`.`cid` = %s "
        )
        data = (name, sorted, remark, area, cid)
        result = self.doAction(update_stmt, data)
        return False if result == False else True

    def deleteAlbum(self, cid, user):
        delete_stmt = (
            "DELETE FROM `category` WHERE `category`.`cid` = %s AND `user`=%s"
        )
        data = (cid, user)
        result = self.doAction(delete_stmt, data)
        return False if result == False else True

    def deletePhotoByCid(self, cid):
        delete_stmt = (
            "DELETE FROM photo WHERE category=%s"
        )
        data = (cid)
        result = self.doAction(delete_stmt, data)
        return False if result == False else True

    def deletePhotoTags(self, cid):
        delete_stmt = (
            "DELETE FROM photo_tags WHERE photo in (SELECT pid FROM photo WHERE category=%s)"
        )
        data = (cid)
        result = self.doAction(delete_stmt, data)
        return False if result == False else True

    def deletePhotoByPid(self, pid, user):
        delete_stmt = (
            "DELETE FROM `photo` WHERE `photo`.`pid` = %s AND `user`=%s"
        )
        data = (pid, user)
        result = self.doAction(delete_stmt, data)
        return False if result == False else True

    def getPhotoInfor(self, album):
        search_stmt = (
            "SELECT * FROM `photo` WHERE `category` = %s "
        )
        data = (album)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        else:
            result = result.fetchall()
            if len(result) > 0:
                small_data = result[0]["large"] if result[0]["small"] == "-" else result[0]["small"]
                return cosClient.getUrl(small_data)
        return "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1364033727,724695302&fm=26&gp=0.jpg"

    def getAllAlbumInfor(self, user):
        search_stmt = (
            "SELECT * FROM `category` WHERE `user` = %s"
        )
        data = (user)
        result = self.doAction(search_stmt, data)
        return False if result == False else [{
            "name": eve["name"],
            "creattime": str(eve["publish"]),
            "creatarea": eve["area"],
            "remark": eve["remark"],
            "cid": eve["cid"],
            "url": self.getPhotoInfor(eve["cid"])
        } for eve in result.fetchall()]

    def getAlbumInfor(self, user, album):
        search_stmt = (
            "SELECT * FROM `category` WHERE `user` = %s AND `cid` = %s"
        )
        data = (user, album)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        result = result.fetchall()
        return {
            "name": result[0]["name"],
            "creattime": str(result[0]["publish"]),
            "creatarea": result[0]["area"],
            "remark": result[0]["remark"],
            "cid": result[0]["cid"],
        } if len(result) == 1 else False

    def getPhotoListCid(self, cid):
        search_stmt = (
            "SELECT * FROM `photo` WHERE `category` = %s"
        )
        data = (cid)
        result = self.doAction(search_stmt, data)
        return False if result == False else [{
            "pid": eve["pid"],
            "url": cosClient.getUrl(eve["large"]),
            "url_large": cosClient.getUrl(eve["large"] if eve["small"] == "-" else eve["small"]),
            "tags": eve["remark"],
        } for eve in result.fetchall()]

    def getPhotoList(self, tags, user):
        search_stmt = (
            '''SELECT * FROM photo WHERE user=%s AND pid IN (SELECT photo FROM (SELECT tid FROM tags WHERE name=%s) t '''
            '''LEFT JOIN photo_tags pt ON pt.tag=t.tid)'''
        )
        data = (user, tags)
        result = self.doAction(search_stmt, data)
        return False if result == False else [{
            "pid": eve["pid"],
            "url": cosClient.getUrl(eve["large"]),
            "url_large": cosClient.getUrl(eve["large"] if eve["small"] == "-" else eve["small"]),
            "tags": eve["remark"],
        } for eve in result.fetchall()]

    def getPhotoListUser(self, user):
        search_stmt = (
            '''SELECT p.*, c.* FROM `photo` AS p, category AS c WHERE p.user=%s AND c.cid=p.category'''
        )
        data = (user)
        result = self.doAction(search_stmt, data)
        return False if result == False else [{
            "pid": eve["pid"],
            "url": cosClient.getUrl(eve["large"]),
            "url_large": cosClient.getUrl(eve["large"] if eve["small"] == "-" else eve["small"]),
            "tags": eve["remark"],
            "remark": "%s, %s, %s, %s" % (
                eve["c.name"], str(eve["area"]), str(eve["c.remark"]), eve["remark"])
        } for eve in result.fetchall()]

    def getTagsList(self, uid):
        search_stmt = (
            "SELECT name FROM tags WHERE tid IN (SELECT DISTINCT pt.tag FROM (SELECT pid FROM photo WHERE user=%s) p "
            "LEFT JOIN photo_tags pt ON pt.photo=p.pid)"
        )
        data = (uid)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        else:
            tags_list = []
            temp_list = []
            temp_length = 0
            for eve_tag in result.fetchall():
                temp_list.append(eve_tag['name'])
                temp_length = temp_length + len(eve_tag['name'])
                status = random.choice((True, True, False, False, False))
                if (status and len(temp_list) >= 2) or len(temp_list) > 4 or temp_length > 8:
                    tags_list.append(temp_list)
                    temp_list = []
                    temp_length = 0
            tags_list.append(temp_list)
            return tags_list

    def save2Db(self, name, large, category, user):
        insert_stmt = (
            "INSERT INTO `photo` (`name`, `large`, `category`, `creattime`, `creatarea`, `small`, `tags`, `remark`, `user`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        )
        data = (name, large, category, datetime.datetime.now(), "-", "-", "-", "-", user)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

    def updatePhotoInfor(self, large, small):
        update_stmt = (
            "UPDATE `photo` SET `small` = %s  WHERE `photo`.`large` = %s "
        )
        data = (small, large)
        result = self.doAction(update_stmt, data)
        return False if result == False else True

    def getPhotoInforPrediction(self):
        search_stmt = (
            'SELECT * FROM `photo` WHERE remark="-"'
        )
        data = ()
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        else:
            result = result.fetchall()
            if len(result) > 0:
                result_list = []
                photo_dict = {}
                for eve in result[0:60]:
                    photo_dict[eve['name']] = eve['pid']
                    result_list.append(
                        {
                            "pid": eve["pid"],
                            "pic": eve["large"],
                            "name": eve["name"],
                            "type": eve["name"].split(".")[1],
                        }
                    )
                return (result_list, photo_dict)
            return False

    def saveToPhotoDB(self, tags, remark, pid):
        insert_stmt = (
            "UPDATE `photo` SET `tags` = %s, `remark` = %s  WHERE `photo`.`pid` = %s"
        )
        data = (" ".join(tags), remark, pid)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

    def saveToTagsDB(self, tags):
        insert_stmt = (
            "INSERT INTO `tags` (`tid`, `name`, `remark`) "
            "VALUES (NULL, %s, NULL)"
        )
        data = (tags)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

    def getTags(self, tags):
        search_stmt = (
            'SELECT * FROM `tags` WHERE `name`=%s'
        )
        data = (tags)
        result = self.doAction(search_stmt, data)
        if result == False:
            return False
        result = result.fetchall()
        return result[0]['tid'] if len(result) == 1 else False

    def saveToPhotoTagsDB(self, tags, photo):
        insert_stmt = (
            "INSERT INTO `photo_tags` (`ptid`, `tag`, `photo`, `remark`) "
            "VALUES (NULL, %s, %s, NULL)"
        )
        data = (tags, photo)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True

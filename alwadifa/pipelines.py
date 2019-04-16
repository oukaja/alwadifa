# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import uuid


class AlwadifaPipeline(object):

    def __init__(self):
        self.db = pymysql.connect(host="localhost",  # your host
                                  user="root",  # username
                                  passwd="",  # password
                                  db="alwadifa",  # name of the database
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
        cursor = self.db.cursor()
        self.db.set_charset("utf8")
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        cursor.close()
        self.db.commit()

    def process_item(self, item, spider):
        i = dict(item)
        cursor = self.db.cursor()
        id = uuid.uuid4().__str__()
        publication = i["publication"]
        titre = i["titre"] # //div[@class='article_title_club']/h1/text()
        body = i["body"]
        link = i["link"]
        try:
            cursor.execute(
                query="INSERT INTO offres(id, link, publication, titre, body) VALUES (%s, %s, %s, %s, %s)",
                args=(id, link, publication, titre, body))
        except Exception as e:
            print(e)
        finally:
            self.db.commit()
            cursor.close()
        cursor.close()

    def spider_closed(self, spider):
        self.db.close()

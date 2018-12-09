# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from typing import List, Any
from scrapy.conf import settings
from pymongo import MongoClient


class WeiboPipeline(object):
    # # result_list = []
    #
    def __init__(self):
        host = settings['DB_HOST']
        port = settings['DB_PORT']
        db_name = settings['DB_NAME']
        self.conn = MongoClient(host, port)
        # connect db
        db = self.conn[db_name]
        self.collection = db['kp_weibo']

    # def open_spider(self, spider):
    #     self.file = open('result.txt', 'a+', encoding='utf8')
    #     print('the file opened')

    def process_item(self, item, spider):
        # write to text
        # line = json.dumps(dict(item))
        # line = line.replace("'", '"')
        # line = line.replace("\n", '')
        # new_line = "u'" + line + "'"
        # self.file.write(eval(new_line) + '\n')

        # write to db
        # self.collection.insert(dict(item))
        # self.post.insert(dict(eval(new_line)))
        item_dict = dict(item)
        self.collection.update(
            {'id': item_dict['id']},
            {'$set': {'text': item_dict['text'], 'created_at': item_dict['created_at'],'format_create_time': item['format_create_time'],
                      'comments_count': item_dict['comments_count'], 'type': item_dict['type']}}, True, True)
        return item

    def close_spider(self, spider):
        # self.file.close()
        # print('the file is close')

        self.conn.close()
        print('close db..')

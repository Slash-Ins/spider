# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from typing import List, Any


class WeiboPipeline(object):

    # # result_list = []
    #
    # def __init__(self):
    #     self.result_list = []

    def open_spider(self, spider):
        self.file = open('result.txt', 'a+', encoding='utf8')
        print('the file opened')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        line = line.replace("'", '"')
        line = line.replace("\n",'')
        new_line = "u'"+line+"'"

        # line.decode('unicode_escape')
        # self.result_list.append(line)
        # self.file.write(str(self.result_list))
        self.file.write(eval(new_line)+'\n')
        return item

    def close_spider(self, spider):
        self.file.close()
        print('the file is close')

# -*- coding: utf-8 -*-
import scrapy
import json
import requests
# from scrapy import log
from ..items import WeiboItem

class WeiboKpSpider(scrapy.Spider):
    name = 'weibo_kp_spider'
    allowed_domains = ['weibo.com']
    base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=1076036548680453'
    req = requests.get(base_url)
    res = req.json()
    total_num = res['data']['cardlistInfo']['total']
    max_page = int(int(total_num / 10)) + 1
    print('======================= max_page ====================')
    print(max_page)
    # page = 0
    start_urls_list = []
    # for i in range(1, max_page + 1):
    for i in range(1, 4):
        url = base_url + '&page=' + str(i)
        start_urls_list.append(url)

    start_urls = start_urls_list

    # start_urls = ['http://weibo.com/']

    def parse(self, response):
        content = json.loads(response.body)
        # self.logger.info('response content : %s', content)
        # print(content)
        weibo_info = content['data']['cards']
        # self.logger.info('weibo_info : %s', weibo_info)
        result = {}
        for card in weibo_info:
            self.logger.info('========================================================')
            item = WeiboItem()
            if card['card_type'] == 9:
                item['created_at'] = card['mblog']['created_at']
                item['text'] = card['mblog']['text']
                item['comments_count'] = card['mblog']['comments_count']
                yield item
                # self.logger.info(card['mblog']['created_at'])
                # self.logger.info(card['mblog']['text'])
                # self.logger.info(card['mblog']['comments_count'])
                # result = {'created_at': card['mblog']['created_at'], 'text': card['mblog']['text'],
                #           'comments_count': card['mblog']['comments_count']}
                # log.msg('============== result ======================')
                # log.msg(result)
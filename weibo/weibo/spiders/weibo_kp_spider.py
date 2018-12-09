# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from datetime import datetime,timedelta,timezone

# from weibo.tools import get_time_today_string, get_time_yesterday_string
# from scrapy import log
from ..items import WeiboItem


def get_time_today_string():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    # print(utc_dt)
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    bj_dt_string = bj_dt.strftime('%Y-%m-%d')
    return bj_dt_string


def get_time_yesterday_string():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    # print(utc_dt)
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    bj_dt_y = bj_dt + timedelta(-1)
    bj_dt_y_string = bj_dt_y.strftime('%Y-%m-%d')
    # print(bj_dt_y)
    return bj_dt_y_string

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
    for i in range(1, max_page + 1):
        # for i in range(1, 6):
        url = base_url + '&page=' + str(i)
        start_urls_list.append(url)

    start_urls = start_urls_list

    # start_urls = ['http://weibo.com/']



    def parse(self, response):
        content = json.loads(response.body)

        weibo_info = content['data']['cards']

        for card in weibo_info:
            self.logger.info('========================================================')
            item = WeiboItem()
            if card['card_type'] == 9:
                item['id'] = card['mblog']['id']
                item['created_at'] = card['mblog']['created_at']
                item['text'] = card['mblog']['text']
                item['comments_count'] = card['mblog']['comments_count']
                if '总结' in item['text']:
                    item['type'] = 'summary'
                elif 'https://m.weibo.cn/status/' in item['text']:
                    if ('转' in item['text'] and '评' in item['text']) or '热度博' in item['text'] or '热度' in item['text']:
                        item['type'] = 'hot'
                    elif '回控' in item['text'] \
                            or '控评' in item['text'] \
                            or '合集' in item['text'] \
                            or '汇总' in item['text'] \
                            or '总汇' in item['text'] \
                            or '打卡方式' in item['text'] in item['text'] \
                            or '目标打卡' in item['text'] \
                            or '捞' in item['text'] \
                            or '控' in item['text']:
                        item['type'] = 'kp'
                    elif '目标' in item['text'] and '评论' in item['text']:
                        item['type'] = 'hot'
                    else:
                        item['type'] = 'kp'
                else:
                    item['type'] = 'others'

                if '小时' in item['created_at'] or '分钟' in item['created_at']:
                    item['format_create_time'] = get_time_today_string()[2:]
                elif '昨天' in item['created_at']:
                    item['format_create_time'] = get_time_yesterday_string()[2:]
                else:
                    if len(item['created_at']) == 5:
                        current_year = get_time_yesterday_string()[2:4]
                        item['format_create_time'] = current_year + '-' + item['created_at']
                    else:
                        item['format_create_time'] = item['created_at']

                yield item

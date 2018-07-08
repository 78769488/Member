# -*- coding: utf-8 -*-
import json
import os
import time

import scrapy
from scrapy.http import Request
from redis import StrictRedis, ConnectionPool

from .. import settings


class MemberSpider(scrapy.Spider):
    name = 'member'
    allowed_domains = ['www.okooo.com']
    start_urls = ['http://www.okooo.com/']

    get_fans_page = 0
    data_path = settings.FILE_PATH
    if not os.path.isdir(data_path):
        os.mkdir(data_path)

    @staticmethod
    def gen_uid():
        for uid in range(10):
            yield uid

    def parse(self, response):
        list_uid = self.gen_uid()
        base_url = "http://www.okooo.com/member/{uid}/"
        redis_url = settings.REDIS_URL
        pool = ConnectionPool.from_url(redis_url)
        redis_client = StrictRedis(connection_pool=pool)
        for uid in list_uid:
            redis_client.sadd('uuid', uid)
        len_uuid = redis_client.scard('uuid')
        while len_uuid > 0:
            len_uuid -= 1
            uid = redis_client.spop('uuid').decode("utf-8")
            print("spop uid===%s, type(uid)===%s" % (uid, type(uid)))
            url = base_url.format(uid=uid)
            yield Request(url=url, callback=self.parse_uid)

    def parse_uid(self, response):
        print(response.xpath('//title/text()').extract_first())


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
# import json
# from scrapy.mail import MailSender
from redis import StrictRedis, ConnectionPool


class MemberPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self, path, redis_url, settings):
        self.path = path
        self.file_phone = None
        self.file_all = None
        self.settings = settings
        self.redis_url = redis_url
        # print("爬取深度：", val if val else "无限")
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        print("保存结果目录：", self.path)

    def process_item(self, item, spider):
        # 操作并进行持久化
        try:
            name = item.get('name', None)
            uid = item.get("uid", "uid")
            name = name.replace("首页-彩友圈", "")
            # if name.isdigit() and len(name) == 11:
            # print(name, uid)
            self.redis.hsetnx("uuid", uid, name)

            # return表示会被后续的pipeline继续处理
            return item

            # 表示将item丢弃，不会被后续pipeline处理
            # raise DropItem()
        except Exception as e:
            print(e)

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:
        :return:
        """
        print("初始化时候，用于创建pipeline对象")
        path = crawler.settings.get('FILE_PATH')
        redis_url = crawler.settings.get("REDIS_URL")
        settings = crawler.settings
        print(path)
        return cls(path, redis_url, settings)
        # pass

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        pool = ConnectionPool.from_url(self.redis_url)
        self.redis = StrictRedis(connection_pool=pool)
        print('爬虫开始执行.....%s' % spider)
        fill_all = os.path.join(self.path, spider.name + '_all.txt')
        file_phone = os.path.join(self.path, spider.name + '_phone.txt')
        self.file_all = open(fill_all, 'a+', encoding='utf-8')
        self.file_phone = open(file_phone, 'a+', encoding='utf-8')

    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print('爬虫关闭.....%s' % spider)

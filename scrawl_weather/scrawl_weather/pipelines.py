# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
from scrawl_weather.items import Page_urls, Table_data


class ScrawlWeatherPipeline(object):
    def __init__(self):
        #  csv文件的位置,无需事先创建  用于存储中间的url
        store_file1 = os.path.dirname(__file__) + '/Data/urls.csv'
        self.file1 = open(store_file1, 'w', newline='')
        self.writer1 = csv.writer(self.file1)

        #  csv文件的位置,  用于存储最后需要的数据
        store_file2 = os.path.dirname(__file__) + '/Data/weather.csv'
        self.file2 = open(store_file2, 'w', newline='')
        self.writer2 = csv.writer(self.file2)

    def process_item(self, item, spider):
        # 根据item类型处理不同的存储任务
        if isinstance(item, Page_urls):
            if item['url_link']:
                self.writer1.writerow([item['url_link']])
        elif isinstance(item, Table_data):
            self.writer2.writerow([item['data_city_name'], item['data_date'], item['data_weather'], item['data_tempture'], item['data_swing']])
            return item
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file1.close()
        self.file2.close()


class Pipelline_url_ToCSV(object):
    def __init__(self):
        #  csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/Data/urls.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'w', newline='')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if item['url_link']:
            # self.writer.writerow((item['image_name'].encode('utf8', 'ignore'), item['image_urls']))
            self.writer.writerow([item['url_link']])
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class Pipelline_table_date_ToCSV(object):
    def __init__(self):
        #  csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/Data/weather.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'w', newline='')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        self.writer.writerow([item['date_time'], item['date_weather'], item['date_tempture'], item['date_swing']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()

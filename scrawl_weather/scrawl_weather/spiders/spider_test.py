'''
爬取天气数据
'''
import scrapy
from scrawl_weather.items import Page_urls, Table_data
import numpy as np
import pandas as pd


class SpiderTest(scrapy.Spider):
    #  每一个爬虫的唯一标识
    name = "spider_test"
    start_urls = ['http://tianqihoubao.com/lishi/anyi/month/201912.html']
    start_url = 'http://tianqihoubao.com'
    url_temp = 'http://tianqihoubao.com/lishi/anyi/month/201912.html'

    def parse(self, response):
        # 提取数据
        url_item = Table_data()
        title_name = response.xpath('//div[@id="content"]/h1/text()').extract()[0]
        head, sep, tail = title_name.replace(' ', '').replace('\r\n', '').partition('历史')
        # 获取数据对应列表
        data_date_list = response.xpath('//table/tr/td/a/text()').extract()
        data_date_list.insert(0, ' ')  # 列表长度不一致，在第一个位置插入空元素
        data_weather_list = response.xpath('//table/tr/td[2]/text()').extract()
        data_tempture_list = response.xpath('//table/tr/td[3]/text()').extract()
        data_swing_list = response.xpath('//table/tr/td[4]/text()').extract()
        len_list = np.arange(1, len(data_weather_list), 1).tolist()
        for i in len_list:
            url_item['data_city_name'] = head
            url_item['data_date'] = data_date_list[i].replace(' ', '').replace('\r\n', '')
            url_item['data_weather'] = data_weather_list[i].replace(' ', '').replace('\r\n', '')
            url_item['data_tempture'] = data_tempture_list[i].replace(' ', '').replace('\r\n', '')
            url_item['data_swing'] = data_swing_list[i].replace(' ', '').replace('\r\n', '')
            yield url_item

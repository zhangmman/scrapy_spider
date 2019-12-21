'''
爬取天气数据
'''
import scrapy
from scrawl_weather.items import Page_urls, Table_data
import numpy as np
import pandas as pd


class WeatherSpider(scrapy.Spider):
    #  每一个爬虫的唯一标识
    name = "weather"
    # 定义爬虫爬取的起始点， 起始点可以是多个， 这里只有一个
    start_urls = ['http://tianqihoubao.com/lishi/jiangxi.htm']
    start_url = 'http://tianqihoubao.com'

    def parse(self, response):
        # 提取数据
        # css()方法找到所有这样的article 元素， 并依次迭代
        products = response.xpath('//div[@class="citychk"]')
        for product in products:
            url_item = Page_urls()
            url_list = product.xpath('.//dl/dd/a/@href').extract()
            for url in url_list:
                url_item['url_link'] = self.start_url+url
                yield url_item
                yield scrapy.Request(url_item['url_link'], callback=self.parse_page1)

    def parse_page1(self, response):
        # 提取page1中的内容
        products = response.xpath('//div[@class="box pcity"][9]')
        for product in products:
            url_item = Page_urls()
            url_list = product.xpath('.//ul/li/a/@href').extract()
            for url in url_list:
                url_item['url_link'] = self.start_url+url
                yield url_item
                yield scrapy.Request(url_item['url_link'], callback=self.parse_page2)

    def parse_page2(self, response):
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

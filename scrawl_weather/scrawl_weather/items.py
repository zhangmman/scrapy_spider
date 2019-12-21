# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrawlWeatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Page_urls(ScrawlWeatherItem):
    url_link = scrapy.Field()


class Table_data(ScrawlWeatherItem):
    data_city_name = scrapy.Field()
    data_date = scrapy.Field()
    data_weather = scrapy.Field()
    data_tempture = scrapy.Field()
    data_swing = scrapy.Field()

import scrapy
from scrapy import Request
import json
# from PIL import Image


class ImagesSpider(scrapy.Spider):
    # BASE_URL = 'http://image.so.com/zj?ch=art&sn=%s&listtype=new&temp=1'
    BASE_URL = 'https://image.so.com/zjl?ch=beauty&t1=595&src=banner_beauty&sn=%s&listtype=new&temp=1'
    start_index = 0

    # 限制最大数据量,防止磁盘爆炸
    MAX_DOWNLOAD_NUM = 1000

    name = 'images'
    start_urls = [BASE_URL % 0]

    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))
        # 提取所有图片下载url到一个列表,赋给item的'image_urls'字段
        yield {'image_urls': [info['qhimg_url'] for info in infos['list']]}

        # 如果count字段大于0,并且下载数量不足MAX_DOWNLOAD_NUM,继续获取下一页图片信息
        self.start_index += infos['count']
        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index)


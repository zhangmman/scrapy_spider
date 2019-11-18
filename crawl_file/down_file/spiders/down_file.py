'''
https://blog.csdn.net/qq_37295506/article/details/80489334
https://blog.csdn.net/qq_37295506/article/details/80588660
'''
import scrapy
from scrapy.linkextractors import LinkExtractor
from down_file.items import DownFileItem


class DownloadBookSpider(scrapy.Spider):
    name = 'down_file'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/examples/index.html']

    def parse(self, response):

        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound', deny='/index.html$')
        print(len(le.extract_links(response)))
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_example)   # 发送页面请求，并通过parse_example解析页面

    def parse_example(self, response):
        href = response.css('a.reference.external::attr(href)').extract_first()
        url = response.urljoin(href)
        example = DownFileItem()
        example['file_urls'] = [url]
        return example










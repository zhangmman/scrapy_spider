# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class LoginspiderPipeline(object):
    def __init__(self):
        super().__init__()
        self.file = open("login.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        self.file.write("{}|{}\n".format(item["key"], item["value"]))
        return item

    def __del__(self):
        self.file.close()

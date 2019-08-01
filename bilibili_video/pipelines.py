# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import json


class BilibiliSpiderPipeline(object):
    """
    保存到csv文件中
    """

    def open_spider(self, spider):
        self.file = open('bilibili.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()

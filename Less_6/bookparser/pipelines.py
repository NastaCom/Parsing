# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books

    def process_item(self, item, spider):
        if item['name']:
            item['name'] = str(re.sub('\n', '', item['name']))
        if item['price_old']:
            item['price_old'] = int(item['price_old'][0])
        else:
            item['price_old'] = None
        if item['price_new']:
            item['price_new'] = int(item['price_new'][0])
        else:
            item['price_new'] = None
        if item['rate']:
            item['rate'] = item['rate'][0]
        else:
            item['rate'] = None

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

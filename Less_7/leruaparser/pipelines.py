# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua

    def process_item(self, item, spider):
        item['features'] = dict(zip(item['features_name'], item['features_value']))
        del item['features_name']
        del item['features_value']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class LeruaPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=True):
    #     print()
    #     image_g = ()
    #     dir_name = item['name']
    #     return f''


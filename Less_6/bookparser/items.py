# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    price_old = scrapy.Field()
    price_new = scrapy.Field()
    authors = scrapy.Field()
    rate = scrapy.Field()
    link = scrapy.Field()


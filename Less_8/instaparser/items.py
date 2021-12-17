# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    friend_type = scrapy.Field()
    friend_id = scrapy.Field()
    friend_username = scrapy.Field()
    friend_full_name = scrapy.Field()
    friend_photo = scrapy.Field()

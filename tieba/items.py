# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    forum = scrapy.Field()
    note = scrapy.Field()
    reply = scrapy.Field()
    type = scrapy.Field()

    def __init__(self, *args, **kwargs):
        super(TiebaItem, self).__init__(*args, **kwargs)
        self['type'] = kwargs['type']

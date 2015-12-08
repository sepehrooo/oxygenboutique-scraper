# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OxygendemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    designer = scrapy.Field()
    description = scrapy.Field()
    type_ = scrapy.Field()
    raw_color = scrapy.Field()
    image_urls = scrapy.Field()
    stock_status = scrapy.Field()
    link = scrapy.Field()
    code = scrapy.Field()
    sale_discount = scrapy.Field()
    usd_price = scrapy.Field()
    gender = scrapy.Field()
    eur_price = scrapy.Field()
    gpb_price = scrapy.Field()


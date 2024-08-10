# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JumiaItem(scrapy.Item):
    sku = scrapy.Field()
    gtin = scrapy.Field()
    material = scrapy.Field()
    weight = scrapy.Field()
    country = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    img_urls = scrapy.Field()
    product_detail = scrapy.Field()
    key_features = scrapy.Field()

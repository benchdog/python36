# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NovelCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class theGoldenLotusItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    paragraph = scrapy.Field()

class OrdinaryWorldItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()


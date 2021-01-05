import scrapy
from ..items import NovelCrawlItem
from lxml import etree

class ThegoldenlotusSpider(scrapy.Spider):
    name = 'theGoldenLotus'
    allowed_domains = ['https://mp.weixin.qq.com']
    start_urls = ['https://mp.weixin.qq.com/s/pp-UayL88CxOfAt5q7SeIw']

    def parse(self, response):
        html = etree.HTML(response.text)
        a_list = html.xpath('//a[@target="_blank"]')
        # item = NovelCrawlItem()
        # item['href'] = a_list
        for a in a_list:
            item = NovelCrawlItem()
            item['href'] = a.xpath("./@href")
            item['name'] = a.text
            yield item
        # pass
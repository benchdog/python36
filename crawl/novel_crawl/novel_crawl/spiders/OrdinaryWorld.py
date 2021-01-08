#coding:utf8
import scrapy
from ..items import OrdinaryWorldItem
from lxml import etree
from bs4 import BeautifulSoup
import time,random

class OrdinaryworldSpider(scrapy.Spider):
    name = 'OrdinaryWorld'
    allowed_domains = ['https://mp.weixin.qq.com']
    # 第一部
    # start_urls = ['https://mp.weixin.qq.com/s/uegfM9ijxQiQMZC8FdRJUg']
    # 第二部
    # start_urls = ['https://mp.weixin.qq.com/s?__biz=MzkwODE3NjkzNQ==&mid=2247485225&idx=1&sn=d376e4cd693001c16143ab984fac9baf&chksm=c0ccbc61f7bb35772e2dc7cabc71417d3b8aee95ea4d65144107dae1ca9c738f189a95e87ec3&scene=21#wechat_redirect']
    # 第三部
    start_urls = ['https://mp.weixin.qq.com/s?__biz=MzkwODE3NjkzNQ==&mid=2247485364&idx=1&sn=20c6e7c26160798f4a211e2280137240&chksm=c0ccbcfcf7bb35eafeb88d14c7c32b938ee8f75cecf450e1c5bab1ed6042e8cadd2244a7b74b&scene=21#wechat_redirect']

    voice_url_prefix = 'https://res.wx.qq.com/voice/getvoice?mediaid='

    def parse(self, response):
        html = etree.HTML(response.text)
        a_list = html.xpath('//a[@target="_blank"]')
        for a in a_list:
            # item = OrdinaryWorldItem()
            # item['title'] = a.text if a.text else str(a.xpath("./strong/text()")[0])
            # item['url'] = str(a.xpath("./@href")[0])
            title = a.text if a.text else str(a.xpath("./strong/text()")[0])
            if '平凡的世界' in title:
                item = OrdinaryWorldItem()
                item['title'] = title + '.mp3'
                href = str(a.xpath("./@href")[0])
                yield scrapy.Request(url=href, callback=self.parse_page, meta={'item':item}, dont_filter=True)
                # time.sleep(random.random())

    def parse_page(self, response):
        item =  response.meta['item']
        html = etree.HTML(response.text)
        # voice_title = '听书《平凡的世界》第一部' + str(html.xpath('//section/mpvoice/@name'))[1-4] + '.mp3'
        voice_url = self.voice_url_prefix + str(html.xpath('//section/mpvoice/@voice_encode_fileid')[0])
        yield scrapy.Request(url=voice_url, callback=self.download_voice, meta={'item':item}, dont_filter=True)
        # time.sleep(random.random())

    def download_voice(self, response):
        item = response.meta['item']
        title = item['title']
        with open('F:\\ordinaryworld\\' + title, 'wb') as fw:
            fw.write(response.body)

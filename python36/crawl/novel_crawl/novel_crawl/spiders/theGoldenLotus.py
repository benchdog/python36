#coding: utf8
import scrapy
from ..items import theGoldenLotusItem
from lxml import etree
import re

class ThegoldenlotusSpider(scrapy.Spider):
    name = 'theGoldenLotus'
    allowed_domains = ['https://mp.weixin.qq.com']
    start_urls = ['https://mp.weixin.qq.com/s/pp-UayL88CxOfAt5q7SeIw']

    def parse(self, response):
        html = etree.HTML(response.text)
        a_list = html.xpath('//a[@target="_blank"]')
        for a in a_list:
            # item = NovelCrawlItem()
            # item['href'] = a.xpath("./@href")
            # item['title'] = a.text
            if '词话本《金瓶梅》' in str(a.text):
                item = theGoldenLotusItem()
                item['title'] = a.text
                href = str(a.xpath("./@href")[0])
                yield scrapy.Request(href, callback=self.parse_page, meta={'item':item}, dont_filter=True)

    def parse_page(self, response):
        item = response.meta['item']
        html = etree.HTML(response.text)
        l1 = html.xpath('//p/span/strong/text()')
        l2 = html.xpath('//p/strong/span/text()')
        l3 = html.xpath('//p/span/strong/span/text()')
        l4 = html.xpath('//p/strong/text()')
        for i in range(len(l1)):
            if re.match('第.{1,3}?回', l1[i]):
                l0 = l1[i:]
                l = l0 + l2 + l3 + l4
                break
        for i in range(len(l2)):
            if re.match('第.{1,3}?回', l2[i]):
                l0 = l2[i:]
                l = l0 + l1 + l3 + l4
                break
        for i in range(len(l3)):
            if re.match('第.{1,3}?回', l3[i]):
                l0 = l3[i:]
                l = l0 + l2 + l1 + l4
                break
        for i in range(len(l4)):
            if re.match('第.{1,3}?回', l4[i]):
                l0 = l4[i:]
                l = l0 + l2 + l3 + l1
                break

        for i in l:
            # for j in ['.*《金瓶梅》.*', '.+《金瓶梅》.*', '往期.*']:
            for j in ['^读+', '^《金瓶梅》.+', '往期.+']:
                # print(value)
                if re.match(j, i) != None or (str(i)).startswith('读《金瓶梅》') or len(i) > 16 or len(i) < 3:
                    l.remove(i)
                    # print(i)
                # else:
                #     l[i] = l[i].replace('\xa0','')
        print(l)
        # l2 = html.xpath('//p/strong/span/text()')
        #
        # for e in ['李子有毒', '往期精彩回放：', '【编按】', '连载', '风月情深', '。若有人识得此意，方许他读《金瓶梅》也。', '"Top Stories" is disabled', '微信版本过低', '长按识别前往小程序']:
        #     if e in l3:
        #         l3.remove(e)
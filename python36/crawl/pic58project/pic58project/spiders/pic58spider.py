# -*- coding: utf-8 -*-
import scrapy


class Pic58spiderSpider(scrapy.Spider):
    name = 'pic58spider'
    allowed_domains = ['www.58pic.com']
    start_urls = ['https://baidu.com']

    def parse(self, response):
        # pass

        author = response.xpath('/html/body/div[4]/div[3]/div/a/p[2]/span/span[2]/text()').extract()
        theme = response.xpath('/html/body/div[4]/div[3]/div/a/p[1]/span[1]/text()').extract()
        self.log("________________________________")
        # self.log(author)
        # self.log(theme)
        self.log(response)
        self.log("++++++++++++++++++++++++++++++++++")
        # for i in range(1,21):
        #     print(i,' **** ',theme[i-1], ':', author[i-1] )
#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
import re
from tutorial.items import TutorialItem
from scrapy import Request
#---------------------------------------------------------------------------
class JdSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://wap.jd.com/category/all.html"
    ]

    def parse(self, response):
        '获取全部分类商品'
        req = []
        for sel in response.xpath('/html/body/div[5]/div[2]/a'):
            name = sel.xpath('text()').extract()
            href = sel.xpath('@href').extract()
            for i in href:
                if 'category' in i:
                    url = "http://wap.jd.com" + i
                    # print url
                    r = Request(url, callback=self.parse_category)
                    req.append(r)
        return req

    def parse_category(self,response):
        '获取分类页'
        req = []
        for sel in response.xpath('/html/body/div[5]/div/a'):
            href = sel.xpath('@href').extract()
            for i in href:
                url = "http://wap.jd.com" + i
                # print url
                r = Request(url, callback=self.parse_list)
                req.append(r)
        return req

    def parse_list(self,response):
        '分别获得商品的地址和下一页地址'
        req = []

        '下一页地址'
        next_list = response.xpath('/html/body/div[21]/a[1]/@href').extract()
        if next_list:
            url = "http://wap.jd.com" + next_list[0]
            r = Request(url, callback=self.parse_list)
            req.append(r)

        '商品地址'
        for sel in response.xpath('/html/body/div[contains(@class, "pmc")]/div[1]/a'):
            href = sel.xpath('@href').extract()
            for i in href:
                url = "http://wap.jd.com" + i
                r = Request(url, callback=self.parse_product)
                req.append(r)
        return req

    def parse_product(self,response):
        '商品页获取title,price,product_id'
        url = re.sub('product','comments',response.url)
        r = Request(url,callback=self.parse_comments)

        title = response.xpath('//title/text()').extract()[0][:-7]
        price = response.xpath('/html/body/div[4]/div[4]/font/text()').extract()[0][1:]
        product_id = response.url.split('/')[-1][:-5]

        item = TutorialItem()
        item['title'] = title
        item['price'] = price
        item['product_id'] = product_id
        r.meta['item'] = item
        print title,price,product_id
        return r

    def parse_comments(self,response):
        '获取商品comment数'
        comment_5 = response.xpath('/html/body/div[4]/div[2]/a[1]/font[2]/text()').extract()
        comment_3 = response.xpath('/html/body/div[4]/div[2]/a[2]/font/text()').extract()
        comment_1 = response.xpath('/html/body/div[4]/div[2]/a[3]/font/text()').extract()
        comment = comment_5 + comment_3 + comment_1
        totle_comment = sum([int(i.strip()) for i in comment])
        item = response.meta['item']
        item['comment'] = totle_comment
        return item
############################################################################

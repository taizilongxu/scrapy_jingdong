#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
import scrapy
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
                    print url
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
                print url
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
                print url
                r = Request(url, callback=self.parse_product)
                req.append(r)
        return req

    def parse_product(self,response):
        req = []
        url = re.sub('product','comments',response.url)
        r = Request(url,callback=self.parse_comments)
        req.append(r)

        title = response.xpath('//title/text()').extract()[0][:-6]
        price = response.xpath('/html/body/div[4]/div[4]/font/text()').extract()[0]
        print title,price
        print "sucess!"
        return req



############################################################################

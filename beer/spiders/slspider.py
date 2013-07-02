# coding: utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from beer.items import Beer

class SuperiorLqSpider(BaseSpider):
    name = "superiorlq"
    allowed_domains = ["superiorliquormarket.com"]
    start_urls = [
        "http://www.superiorliquormarket.com/Beer_c_77.html"
    ]
    
    def parse(self, response):
        beers = []
        hxs = HtmlXPathSelector(response)
        p = hxs.select('//form[@id="frmsortby"]/table/tr[5]/td/table/tr[2]/td/table/tr') 
        for row in p:
            item = Beer()
            #LHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[0]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[0]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[0]
            beers.append(item)
            #RHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[2]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[3]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[1]
            beers.append(item)
            
        return beers
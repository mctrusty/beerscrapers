# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from beer.items import Beer

class SuperiorLqSpider(CrawlSpider):
    name = "superiorlq"
    allowed_domains = ["superiorliquormarket.com"]
    start_urls = [
        "http://www.superiorliquormarket.com"
    ]
    
    rules = (
        Rule(SgmlLinkExtractor(allow=('Beer_c_77.html'))),
        Rule(SgmlLinkExtractor(allow=('Beer_c_77-\d+-3.html')), callback = 'parse_item', follow=True),
    )
    
    def parse_item(self, response):
        beers = []

        # After page 1, tr[5] becomes tr[4] bc there's no category list
        row = 4 # The row is 
        if (response.url == "http://www.superiorliquormarket.com/Beer_c_77-1-3.html"):
            row = 5
            
        selector = '//form[@id="frmsortby"]/table/tr[' + str(row) + ']/td/table/tr[2]/td/table/tr'
        hxs = HtmlXPathSelector(response)
        p = hxs.select(selector) 
        
        for row in p:
            item = Beer()
            #LHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[0]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[0]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[0]
            yield item

            #RHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[2]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[3]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[1]
            yield item
            
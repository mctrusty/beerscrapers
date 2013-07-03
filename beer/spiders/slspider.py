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
        hxs = HtmlXPathSelector(response)
		# After page 1, tr[5] becomes tr[4] bc there's no cat list
        p = hxs.select('//form[@id="frmsortby"]/table/tr[5]/td/table/tr[2]/td/table/tr') 
		
        for row in p:
            item = Beer()
            #LHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[0]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[0]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[0]
            yield item
			#beers.append(item)
            #RHS:
            item['beer'] = row.select('td/table/tr/td/a/text()').extract()[2]
            item['link'] = row.select('td/table/tr/td/a/@href').extract()[3]
            item['price'] = row.select('td//span[@class="price"]/text()').extract()[1]
            yield item
			#beers.append(item)
            
        #return beers
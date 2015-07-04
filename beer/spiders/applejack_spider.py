from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor

from beer.items import Beer

class AppleJackSpider(CrawlSpider):
    name = "applejack"
    allowed_domains = ["applejack.com"]
    start_urls = [
        "http://www.applejack.com/beer/catalog/"
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('\?dd=\d+')), callback = 'parse_item', follow=True),
    )

    def parse_item(self, response):            
        selector = '//div[@class="productListItem"]'
        hxs = HtmlXPathSelector(response)
        rows = hxs.select(selector) 
        for row in rows:
            item = Beer()
            item['store'] = 'applejack'
            item['beer'] = row.select('h5/a/text()').extract()
            item['price'] = row.select('div//span[@class="listValue"]/text()').extract()
            item['link'] =  row.select('h5/a/@href').extract()
            yield item

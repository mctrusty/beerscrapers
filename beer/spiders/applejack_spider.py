from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor

from beer.items import Beer

class AppleJackSpider(CrawlSpider):
    name = "applejack"
    allowed_domains = ["applejack.com"]
    start_urls = [
        "http://www.applejack.com/beer/"
    ]
    
    rules = (
        Rule(LinkExtractor(allow=('\?page=\d+&sortby=sort_item_order&l=\d+&item_type=beer')), callback = 'parse_item', follow=True),
    )

    def parse_item(self, response):            
        selector = '/html/body/div[4]/div/div[3]/div[2]/div[3]/div'
        hxs = HtmlXPathSelector(response)
        rows = hxs.select(selector) 
        for row in rows:
            item = Beer()
            item['store'] = 'ChIJ_Qn9pM6Fa4cRDCMtavWGqh8'
            item['beer'] = row.select('table/tr/td[3]/table/tr/td/a/text()').extract()[0]
            item['price'] = row.select('table/tr/td[5]/div[1]/div[1]/text()').extract()[0]
            item['link'] =  row.select('table/tr/td[3]/table/tr/td/a/@href').extract()[0]
            yield item

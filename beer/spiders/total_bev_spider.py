from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from beer.items import Beer

class TotalBevSpider(Spider):
    name = "totalbev"
    allowed_domains = "totalbev.com"
    start_urls = [
        "http://www.totalbev.com/Beer",
        #"http://www.totalbev.com/Beer?page=\d+"
    ]
    
    def parse(self, response):
        sel = Selector(response)
        products = sel.css('.product-title').xpath('text()').extract()
        prices = response.css('span.price-value > span').xpath('text()').extract()
        sizes = response.css('div.extra-field-show-on').re('Size:\s+(.*)')

        for x in range(0,12):
            item = Beer()
            item['store'] = 'ChIJF1Qd58CJa4cRt9sMAOqW5cE'
            item['beer'] = products[x]
            item['price'] = prices[x]
            item['size'] = sizes[x]
            yield item
        
    
    

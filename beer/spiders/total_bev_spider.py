import re;
from scrapy.shell import inspect_response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor

from beer.items import Beer

class TotalBevSpider(CrawlSpider):
    name = "totalbev"
    allowed_domains = ["totalbev.com"]
    start_urls = [
        "http://totalbev.com/Beer/"
    ]

    rules = (
#        Rule(LinkExtractor(allow=('/Beer/'), deny=('/Beer/\?rf_selection')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('\?page=\d+')), follow=True, callback='parse_item'),
    )
    
    uspkg = re.compile('^(?P<size>\d+(?:\.\d+)?OZ|\d+\sML)\s(?:(?:(?P<qty>\d+) PACK)?\s?(?P<pkg>BOTTLE|CAN))?')
    suitcase = re.compile('^(?:(?P<qty>\d+) PACK)')
    europkg = re.compile('^(?P<size>\d+) ML')
    uskeg = re.compile('Keg|KEG (?P<size>\d+(:?\.\d+)?)')

    def split_pkg_info(self, beer, field):
        uspkginfo = re.search(self.uspkg, field)
        suitcaseinfo = re.search(self.suitcase, field)
        europkginfo = re.search(self.europkg, field)
        uskeginfo = re.search(self.uskeg, field)
        if (uspkginfo):
            beer['size'] = uspkginfo.group('size')
            beer['quantity'] = uspkginfo.group('qty')
            beer['pkg'] = uspkginfo.group('pkg')
        elif (suitcaseinfo):
            beer['size'] = '12 OZ'
            beer['quantity'] = suitcaseinfo.group('qty')
            beer['pkg'] = 'CAN'
        elif (europkginfo):
            beer['size'] = europkginfo.group('size') + 'ML'
            beer['quantity'] = 1
            beer['pkg'] = 'BOTTLE'
        elif (uskeginfo):
            beer['size'] = uskeginfo.group('size')
            beer['quantity'] = 1
            beer['pkg'] = 'KEG'

    def parse_item(self, response):
        sel = Selector(response)
        products = sel.css('.product-title').xpath('text()').extract()
        prices = response.css('span.price-value > span').xpath('text()').extract()
        sizes = response.css('div.extra-field-show-on').re('Size:\s+(.*)')

        for x in range(0,12):
            item = Beer()
            item['store'] = 'ChIJF1Qd58CJa4cRt9sMAOqW5cE'
            item['beer'] = products[x]
            item['price'] = prices[x]
            self.split_pkg_info(item, sizes[x])
#            item['size'] = sizes[x]
            yield item
        
    
    

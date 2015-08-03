import re
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
        Rule(LinkExtractor(allow=('\?page=\d+&sortby=sort_item_order&l=25&item_type=beer'), canonicalize=False), callback = 'parse_item', follow=True),
    )

    pkginfo = '\((?:(?P<qty>\d+)\spack\s)?(?P<size>\d+oz)?\s?(?P<pkg>bottle|can)s?\)'
    beerinfo = "(?P<brewer>(?:\w|\d|\s|-|'|#)+) - (?P<beer>(?:\w|\d|\s|-|'|#)+) "
    multi_info = beerinfo + pkginfo
    eurobottle = beerinfo + '\((?P<size>\d+ml)\)'
    usbottle = beerinfo + '\((?P<size>\d+(?:\.\d+)oz)\)'

    def parse_beer(self, beer, field):
        #multi = > 1 container per pkg
        #import pdb; pdb.set_trace()
        multi = re.search(self.multi_info, field)
        eurosingle = re.search(self.eurobottle, field)
        usbottle = re.search(self.usbottle, field)
        if multi:
            beer['brewer'] = multi.group('brewer')
            beer['beer'] = multi.group('beer')
            beer['quantity'] = multi.group('qty')
            beer['size'] = multi.group('size')
            beer['pkg'] = multi.group('pkg')
        elif eurosingle:
            beer['brewer'] = eurosingle.group('brewer')
            beer['beer'] = eurosingle.group('beer')
            beer['quantity'] = 1
            beer['size'] = eurosingle.group('size')
            beer['pkg'] = 'bottle'
        elif usbottle:
            beer['brewer'] = usbottle.group('brewer')
            beer['beer'] = usbottle.group('beer')
            beer['quantity'] = 1
            beer['size'] = usbottle.group('size')
            beer['pkg'] = 'bottle'
        else:
            beer['beer'] = field

    def parse_item(self, response):            
        #import pdb; pdb.set_trace()
        selector = '/html/body/div[4]/div/div[3]/div[2]/div[3]/div'
        hxs = HtmlXPathSelector(response)
        rows = hxs.select(selector) 
        for row in rows:
            item = Beer()
            item['store'] = 'ChIJ_Qn9pM6Fa4cRDCMtavWGqh8'
            #item['beer'] = 
            self.parse_beer(item, row.select('table/tr/td[3]/table/tr/td/a/text()').extract()[0])
            item['price'] = row.select('table/tr/td[5]/div[1]/div[1]/text()').extract()[0]
            item['link'] =  row.select('table/tr/td[3]/table/tr/td/a/@href').extract()[0]
            
            yield item

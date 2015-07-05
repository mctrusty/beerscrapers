# coding: utf-8
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
import logging

from beer.items import Beer
    
class SuperiorLqSpider(CrawlSpider):
    name = "superiorlq"
    allowed_domains = ["superiorliquormarket.com"]
    start_urls = [
        "http://www.superiorliquormarket.com"
    ]
    
    rules = [
        Rule(LinkExtractor(allow=('Beer_c_77\.html')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=('view_category\.asp\?cat=77&sortby=\[sortby\]&page=\d+')), callback = 'parse_item', follow=True),
    ]
    
    # Beer names are listed in the format: MFG - Beer (qty)
    #splitter = re.compile('(.*?) - (.*?) \(([^\)]+)\)')
    splitter = re.compile('(?P<brewer>.*?) - (?P<beer>.*?)\s?(?P<size>(?:\d+\.)?\d+\s?(?:OZ)? (?:CAN|BOTTLE)S?||(?:\d+OZ)\s?BOTTLE$|\d+L|\d/\d\s?BBL|\d+\s?ML\s?(?:BOTTLES?)?|BOTTLE)\s\((?P<qty>[^\)]+)\)')

    def parse_item(self, response):
        from scrapy.shell import inspect_response
        beers = []

        # After page 1, tr[5] becomes tr[4] bc there's no category list
        row = 4 # The row is 
        if ((response.url == "http://www.superiorliquormarket.com/Beer_c_77-1-3.html") or
            (response.url == "http://www.superiorliquormarket.com/Beer_c_77.html")):
            row = 5
            
        import pdb
        selector = '//form[@id="frmsortby"]/table/tr[' + str(row) + ']/td/table/tr[2]/td/table/tr'
        hxs = HtmlXPathSelector(response)
        p = hxs.select(selector) 
#        pdb.set_trace()
        #beer information is laid out in a 2 column table. rhs/lhs = right hand/left hand side
        for row in p:
            item = Beer()
            #LHS
            #beerinfo = row.select('td/table/tr/td/a/text()').re(self.splitter)
            beery = row.select('td/table/tr/td/a/text()').extract()
#            pdb.set_trace()
            #inspect_response(response, self)            
            info = None
            if len(beery) > 0:
                info = re.search(self.splitter, beery[0])
            
            if info is None:
                logging.warning('No pattern match for %s' % beery)
            else:
                item['store'] = 'superiorliquor'
                item['brewer'] = info.group('brewer')
                item['beer'] = info.group('beer')
                item['quantity'] = info.group('qty')        
                item['size'] = info.group('size')
                #item['beer'] = row.select('td/table/tr/td/a/text()').extract()[0]
                item['link'] = row.select('td/table/tr/td/a/@href').extract()[0]
                item['price'] = row.select('td//span[@class="price"]/text()').extract()[0]
                yield item

            #RHS:
            if len(beery) > 1:
                info = re.search(self.splitter, beery[2])
            if info is None:
                logging.warning('No pattern match for %s' % beery)
            else: 
                item['brewer'] = info.group('brewer')
                item['beer'] = info.group('beer')
                item['quantity'] = info.group('qty')
                item['size'] = info.group('size')
                #item['beer'] = row.select('td/table/tr/td/a/text()').extract()[2]
                item['link'] = row.select('td/table/tr/td/a/@href').extract()[3]
                item['price'] = row.select('td//span[@class="price"]/text()').extract()[1]
                yield item
            

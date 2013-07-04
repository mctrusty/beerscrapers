from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from beer.items import Beer

class TotalBevSpider(BaseSpider):
    name = "totalbev"
    allowed_domains = "totalbev.com"
    start_urls = [
        "http://www.totalbev.com/default.aspx?pageid=57&deptID=11&submit=search&scat=Domestic Beer&pz=&#results",
        "http://www.totalbev.com/default.aspx?pageid=57&deptID=12&submit=search&scat=Imported%20Beer&pz=&#results",
        "http://www.totalbev.com/default.aspx?pageid=57&deptID=13&submit=search&scat=MicroBrew&pz=&#results",
        "http://www.totalbev.com/default.aspx?pageid=57&deptID=19&submit=search&scat=Kegs&pz=&#results"
    ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//table[@id="ContentTable"]//table/tr')
        
        for row in rows:
            item = Beer()
            item['beer'] = row.select('td[3]/font/b/text()').extract()
            item['price'] = row.select('td[5]/font/b/text()').extract()
            item['size'] = row.select('td[4]/font/b/text()').extract()
            yield item
        
    
    
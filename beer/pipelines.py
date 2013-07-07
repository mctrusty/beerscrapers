import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class BeerPipeline(object):
    pat = re.compile('(?P<brewer>.*?) (?P<beer>(?:\d+\.)?\d+\s?OZ (?:CANS|BOTTLES?)|(?:\d+OZ)\s?BOTTLE$|\d/\d\s?BBL|\d+\s?ML\s?(?:BOTTLES?)?|BOTTLE)\s\(?P<qty>([^\)]+)\)')
    
    def process_item(self, item, spider):
        if item['beer']:
            match = re.search(self.pat, item['beer'])
            if match is not None:
                item['beer'] = match.group(1)
                if len(match.groups()) > 1:
                    item['size'] = match.group(2)
        
        return item

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Beer(Item):
    # define the fields for your item here like:
    # name = Field()
    store  = Field()
    brewer = Field()
    beer = Field()
    size = Field() #size of individual unit - 12 oz can, pint, etc
    quantity = Field() #number of units in package - 12 pack, 6 pack, etc
    link = Field()
    pkg = Field()
    price = Field()
    pass

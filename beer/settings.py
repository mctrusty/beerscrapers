
# Scrapy settings for beer project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'beer'

SPIDER_MODULES = ['beer.spiders']
NEWSPIDER_MODULE = 'beer.spiders'

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'michael',
            'password':'7a07eChing',
            'database':'beer'
}

ITEM_PIPELINES = ['beer.pipelines.BeerPostgresPipeline']

#ITEM_PIPELINES = [
#    'beer.pipelines.BeerPipeline'
#]

LOG_FILE = "beerlogs.txt"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'beer (+http://www.yourdomain.com)'

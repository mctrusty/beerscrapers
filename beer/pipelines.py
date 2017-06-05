from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer
from kafka import KafkaProducer
from kafka.errors import KafkaError
from sqlalchemy.orm import sessionmaker
from .models import Beers, db_connect, create_beers_table
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

class BeerPostgresPipeline(object):
    """Pipeline for storing beer data in Postgres"""
    def __init__(self):
        engine = db_connect()
        create_beers_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save beer info in database.
        Called for every item pipeline component
        """
        session = self.Session()
        beer = Beers(**item)

        try:
            session.add(beer)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

class KafkaBeerPipeline(object):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        #serializer = MessageSerializer(client)
    def process_item(self, item, spider):
        client = SchemaRegistryClient(url='http://localhost:8081')
        schema_id, avro_schema, schema_version = client.get_latest_schema('beerscraper')
        serializer = MessageSerializer(client)
        encoded = serializer.encode_record_with_schema('beer',avro_schema,item.__dict__['_values'])
        self.producer.send('beer',encoded)


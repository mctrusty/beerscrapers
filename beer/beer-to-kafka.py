#
# uses datamountaineer libraries https://github.com/datamountaineer/python-serializers
# and the avro.schema library
#

from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

# obtain schema from registry client
client = SchemaRegistryClient(url='http://localhost:8081')
schema_id, avro_schema, schema_version = client.get_latest_schema('beerscraper')

# use schema to encode message
record = {'store':'superior', 'brewer':'avery', 'size':'12oz','qty':'6','price':'8.99'}
serializer = MessageSerializer(client)
encoded = serializer.encode_record_with_schema('beer',avro_schema,record)
#encoded
#b'\x00\x00\x00\x00\x03\x10superior\navery\x00\x0812oz\x026\x00\x088.99'

# write encoded message to topic
from kafka import KafkaProducer
from kafka.errors import KafkaError
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
producer.send('beer',encoded)



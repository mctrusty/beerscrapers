#
# uses datamountaineer libraries https://github.com/datamountaineer/python-serializers
# and the avro.schema library
#

from datamountaineer.schemaregistry.client import SchemaRegistryClient
from datamountaineer.schemaregistry.serializers import MessageSerializer, Util
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

#replace beer.avsc with input file or variable
with open('beer.avsc') as f:
    schema = avro.schema.Parse(f.read())

client = SchemaRegistryClient(url='http://localhost:8081')
schema_id = client.register('beerscraper', schema)


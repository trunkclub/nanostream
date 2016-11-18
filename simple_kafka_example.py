import nanostream
from nanostream.nanostream_kafka import (
    NanoKafkaListener, NanoKafkaProducer)
from nanostream.nanostream_processor import NanoStreamProcessor
from nanostream.nanostream_pipeline import NanoStreamGraph

class MyProcessor(NanoStreamProcessor):
    def process_item(self, message):
        # Do whatever to the message
        # Return a dictionary
        message['foo'] = 'bar'
        return message

def main():
    bootstrap_servers=(
        'tls09.prd.aws1.trunkclub.systems:9092,'
        'tls10.prd.aws1.trunkclub.systems:9092')
    listener = NanoKafkaListener(
        bootstrap_servers=bootstrap_servers,
        topics=['public.members.v1'],
        payload_only=True,
        offset_dictionary={'public.members.v1': {0: 10000, 1:100000}})
    processor = MyProcessor()
    producer = NanoKafkaProducer(
        bootstrap_servers=bootstrap_servers, topic='blame_zac_for_this')
    pipeline = NanoStreamGraph()
    pipeline.add_edge(listener, processor, producer)
    pipeline.start()
    print 'It might not look like it, but everything is running.'
    print 'We are publishing tons of data to the topic "blame.zac.for.this".'
    print 'Type "exit()" to quit.'

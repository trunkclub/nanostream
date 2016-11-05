import os
import json
import time
import logging
import cPickle as pickle
import collections
import kafka
from nano_streams.nano_stream_encoder import encode, decode
from nano_streams.nano_stream_processor import NanoStreamSender
from nano_streams.nano_stream_pipeline import (
    NanoGraphWorker, NanoStreamGraph, NanoPrinter)
from nano_streams.nano_stream_processor import NanoStreamProcessor


logging.basicConfig(filename='nano_streams.log', level=logging.INFO)

DEFAULT_BOOTSTRAP_SERVER_1 = 'svc12.prd.aws1.trunkclub.systems:9092'
MAX_QUEUE_SIZE = 1000


class NanoKafkaSynchronizer(NanoStreamProcessor):
    """
    Placeholder for when this is ready.
    """
    pass


class NanoKafkaListener(NanoStreamSender):
    """
    """
    def __init__(self,
                 offset_dictionary=None,
                 topics=None,
                 bootstrap_servers=None,
                 payload_only=True,
                 message_parser=None,
                 default_offset=0,
                 update_offset_interval=2,
                 auto_offset_reset='earliest'):
        self.message_parser = message_parser or (lambda x: x)
        self.payload_only = payload_only
        self.offset_dictionary = (
            offset_dictionary or collections.defaultdict(int))
        self.started = time.time()
        self.auto_offset_reset = auto_offset_reset
        self.topics = topics or []
        self.bootstrap_servers = bootstrap_servers or os.environ.get(
            'KAFKA_BOOTSTRAP_SERVERS', DEFAULT_BOOTSTRAP_SERVER_1).split(',')
        self.listener = kafka.KafkaConsumer(
            group_id='zacs_screwball_thing',
            fenanoh_min_bytes=0,
            enable_auto_commit=True,
            bootstrap_servers=[DEFAULT_BOOTSTRAP_SERVER_1],
            auto_offset_reset=auto_offset_reset)
        self.partitions_dictionary = {
            topic: self.listener.partitions_for_topic(topic) for
            topic in self.topics}
        self.assignments = []
        self.offset_dictionary = offset_dictionary or {topic: {} for topic in self.topics}

        # Let's convert the offset_dictionary to a better thing
        # If the values are ints, set all partitions to that offset
        # If they're dictionaries of int->int, set that partitions individually
        for topic, offset_info in self.offset_dictionary.iteritems():
            if isinstance(offset_info, int):
                offset_dict = {
                    partition: offset_info for
                    partition in self.partitions_dictionary[topic]}
            elif isinstance(offset_info, dict):
                offset_dict = offset_info
            else:
                raise Exception('You specified partition offsets, but you did not '
                                'provide an int or a dict.')

        self.update_offset_interval = \
            update_offset_interval
        for topic, partition_set in self.partitions_dictionary.iteritems():
            if partition_set is None:
                partition_set = set([0])
            for partition in partition_set:
                self.assignments.append(kafka.TopicPartition(topic, partition))
        self.listener.assign(self.assignments)
        for topic_partition in self.assignments:
            if topic_partition.topic not in self.topics:
                continue
            try:
                offset = self.offset_dictionary[topic_partition.topic][topic_partition.partition]
            except KeyError:
                offset = default_offset
                self.offset_dictionary[topic_partition.topic][topic_partition.partition] = offset
            self.listener.seek(topic_partition, offset)

        super(NanoKafkaListener, self).__init__()

    def start(self):
        """
        """
        if not hasattr(self, 'parent'):
            raise Exception(
                "Use 'messages' method instead of 'start' "
                "if the `NanoKafkaListener` is not "
                "inside a `NanoStreamGraph`")
        counter = 0
        while 1:
            response = self.listener.poll()
            for key, value in response.iteritems():
                for message in value:
                    if self.payload_only:
                        self.queue_message(message)
                        continue
                    self.offset_dictionary[message.topic][message.partition] = message.offset
                    message = self.message_parser(message)
                    counter += 1
                    self.offset_dictionary[
                        kafka.TopicPartition(
                            message.topic,
                            message.partition)] = message.offset
                    if self.payload_only:
                        message = json.loads(message.value)
                    self.queue_message(message)

    def messages(self):
        """
        """
        counter = 0
        while 1:
            response = self.listener.poll()
            for key, value in response.iteritems():
                for message in value:
                    message = self.message_parser(message)
                    counter += 1
                    if counter % self.update_offset_interval == 0:
                        self.offset_dictionary[
                            kafka.TopicPartition(
                                message.topic,
                                message.partition)] = message.offset
                    if self.payload_only:
                        message = json.loads(message.value)
                    yield message


class NanoKafkaProducer(object):
    """
    """
    def __init__(self, input_queue=None,
                 bootstrap_servers=None, topic=None, encode_output=True):
        self.topic = topic
        self.input_queue = input_queue
        self.encode_output = encode_output
        self.bootstrap_servers = (
            bootstrap_servers or DEFAULT_BOOTSTRAP_SERVER_1)
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=self.bootstrap_servers)

    def send(self, message, **kwargs):
        try:
            message = decode(message)
        except:
            pass
        try:
            message = json.dumps(message)
        except:
            pass
        print message
        print type(message)
        message = bytes(message)
        print type(message)
        self.producer.send(self.topic, message, **kwargs)

    def start(self, **kwargs):
        while 1:
            one_item = self.input_queue.get(block=True, timeout=None)
            one_item = decode(one_item)
            if self.encode_output:
                one_item = encode(one_item)
            self.send(json.dumps(one_item), **kwargs)


class CollectKafkaOffsets(NanoGraphWorker):
    def worker(self):
        offset_dictionary = {}
        for node in self.graph.node_list:
            if isinstance(node, NanoKafkaListener):
                offset_dictionary.update(node.offset_dictionary)
        self.parent.offset_dictionary.update(offset_dictionary)
        print self.parent.offset_dictionary
        print pickle.dumps(self.parent.offset_dictionary)


def main():
    """
    sender = NanoKafkaProducer(
        bootstrap_servers=DEFAULT_BOOTSTRAP_SERVER_1,
        topic='blame_zac_for_this')
    sender.send("Hi. I am a message.")
    import pdb; pdb.set_trace()
    queue = Queue.Queue(MAX_QUEUE_SIZE)
    """
    listener_1 = NanoKafkaListener(
        topics=['public.members.v1'],
        offset_dictionary={'public.members.v1': {0: 12000000, 1: 13000000}})
    listener_2 = NanoKafkaListener(topics=['finance.invoices.v1'])
    # listener_1.offset_dictionary['public.members.v1'][0] would give you the offset
    #     for that topic and partition

    printer = NanoPrinter()
    accountant = CollectKafkaOffsets()
    graph = NanoStreamGraph()

    # graph.add_node(listener_1)
    # graph.add_node(listener_2)
    # graph.add_node(printer)

    graph.add_edge(listener_1, printer)
    graph.add_edge(listener_2, printer)

    # graph.add_worker(accountant)
    print graph.node_list

    graph.start(block=True)


if __name__ == '__main__':
    main()

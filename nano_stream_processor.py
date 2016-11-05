import Queue
from tc_stream_encoder import encode, decode


class TrunkClubStreamSender(object):
    """
    Anything with an output queue.
    """
    def __init__(self, *args, **kwargs):
        self.output_queue_list = []

    def queue_message(self, message):
        message = encode(message)
        for output_queue in self.output_queue_list:
            output_queue.put(message, block=True, timeout=None)


class TrunkClubStreamListener(object):
    """
    Anything that reads from an input queue.
    """
    def start(self):
        while 1:
            one_item = self.input_queue.get(block=True, timeout=None)
            one_item = decode(one_item)
            one_item = self.process_item(one_item)
            if hasattr(self, 'output_queue_list') and len(
                    self.output_queue_list) > 0:
                self.queue_message(one_item)


class TrunkClubStreamProcessor(TrunkClubStreamListener, TrunkClubStreamSender):
    """
    """
    def __init__(self, input_queue=None, output_queue=None):
        self.input_queue = None
        super(TrunkClubStreamProcessor, self).__init__()
        self.start = super(TrunkClubStreamProcessor, self).start

    def process_item(self, *args, **kwargs):
        raise Exception("process_item needs to be overridden in child class.")


class PrintStreamProcessor(TrunkClubStreamProcessor):
    """
    Just a class that prints, for testing purposes only.
    """
    def process_item(self, item):
        print item
        return item


class ExtractKeysStreamProcessor(TrunkClubStreamProcessor):
    """
    Just extracts the keys from a dictionary. For testing.
    """
    def process_item(self, item):
        output = item.keys()
        return output

from nanostream.timed_dict import TimedDict
from nanostream.nanostream_processor import (
    NanoStreamProcessor, NanoStreamSender)


class InnerJoin(NanoStreamProcessor):
    def __init__(self, join_keys=None, delimiter='|', expiration_window=5):
        self.join_keys = join_keys or {}
        self.timed_dict = TimedDict()

    def process_item(self, item):
        join_path = self.join_keys[item.from_queue].split(self.delimiter)
        tmp_dict = item
        for key in join_path:
            tmp_dict = tmp_dict.get(key)
        join_value = tmp_dict

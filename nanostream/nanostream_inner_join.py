from nanostream.timed_dict import TimedDict
from nanostream.nanostream_processor import (
    NanoStreamProcessor, NanoStreamSender)


class InnerJoin(NanoStreamProcessor):
    def __init__(self, join_keys=None, expiration_window=5):
        self.join_keys = join_keys

    def start(self):
        pass

import random
import hashlib
from nanostream_processor import *

class FileReader(NanoStreamProcessor):
    """
    Reads a file and passes its contents down the pipeline.
    """

    def process_item(self, item):
        with open(item, 'r') as nano_file:
            contents = nano_file.read()
        return contents


def random_hash(seed=None):
    return hashlib.md5(seed or str(random.random)).hexdigest()


class FileWriter(NanoStreamProcessor):
    """
    Writes the message to a file with a random name in a specified
    directory.
    """

    def __init__(self, path=None):
        self.path = path or '.'
        super(FileWriter, self).__init__()

    def process_item(self, item):
        with open('/'.join([self.path, random_hash()]), 'w') as nano_file:
            nano_file.write(item)
        return item

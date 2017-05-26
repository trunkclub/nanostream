import json
from jsonschema import validate
from nanostream.nanostream_processor import (
    NanoStreamProcessor)


class JsonValidator(NanoStreamProcessor):
    def __init__(
            self, schema_filename):

        with open(schema_filename, 'r') as json_schema_file:
            self.schema = json.load(json_schema_file)

        super(JsonValidator, self).__init__()

    def process_item(self, item):
        if isinstance(item, str):
            item = json.loads(item)
        try:
            validate(item, self.schema)
            return item
        except ValidationError:
            pass  # We'll log the error here

"""
We pass messages through the nanostream as base64-encoded
pickle files.
"""
import cPickle as pickle
import base64


def encode(something):
    return base64.b64encode(pickle.dumps(something))

def decode(something):
    return pickle.loads(base64.b64decode(something))

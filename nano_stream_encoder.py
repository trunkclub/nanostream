import cPickle as pickle
import base64


def encode(something):
    return base64.b64encode(pickle.dumps(something))

def decode(something):
    return pickle.loads(base64.b64decode(something))

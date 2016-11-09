"""
Copyright (C) 2016 Zachary Ernst
zernst@trunkclub.com or zac.ernst@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import Queue
import types
from nano_stream_encoder import encode, decode


class NanoStreamSender(object):
    """
    Anything with an output queue.
    """
    def __init__(self, *args, **kwargs):
        self.output_queue_list = []

    def queue_message(self, message):
        message = encode(message)
        for output_queue in self.output_queue_list:
            output_queue.put(message, block=True, timeout=None)


class NanoStreamListenerMultiplex(object):
    def __init__(self, *args, **kwargs):
        self.multiplex_workers = kwargs['workers']
        self.listener_class = kwargs['listener_class']
        del kwargs['workers']
        self.listeners = [
            NanoStreamListener(
                *args, index=index, workers=1,
                child_class=self.listener_class, **kwargs)
            for index in range(self.multiplex_workers)]
        for index, listener in enumerate(self.listeners):
            listener.multiplexer_index = index
            child_class_function_dict = {
                function_name: function for function_name, function
                in self.listener_class.__dict__.iteritems() if
                isinstance(function, types.FunctionType)}
            for function_name, the_function in child_class_function_dict.iteritems():
                setattr(
                    listener, function_name, types.MethodType(
                        the_function, listener, self.listener_class)) 

    def start(self):
        for i in self.listeners:
            i.start()


class NanoStreamListener(object):
    """
    Anything that reads from an input queue.
    """

    def __init__(self, workers=1, index=0, child_class=None, **kwargs):
        self.workers = workers
        self.child_class = child_class
        # Change the class if we're going to multiplex it
        if self.workers > 1:
            self.child_class = self.__class__
            self.__class__ = NanoStreamListenerMultiplex
            self.__init__(
                workers=workers, listener_class=self.child_class, **kwargs)
        else:
            self.input_queue = None
            self.index = index

    def start(self):
        while 1:
            one_item = self.input_queue.get(block=True, timeout=None)
            one_item = decode(one_item)
            one_item = self.process_item(one_item)
            if hasattr(self, 'output_queue_list') and len(
                    self.output_queue_list) > 0:
                self.queue_message(one_item)


class NanoStreamProcessor(NanoStreamListener, NanoStreamSender):
    """
    """
    def __init__(self, input_queue=None, output_queue=None):
        super(NanoStreamProcessor, self).__init__()
        self.start = super(NanoStreamProcessor, self).start

    def process_item(self, *args, **kwargs):
        raise Exception("process_item needs to be overridden in child class.")


class PrintStreamProcessor(NanoStreamProcessor):
    """
    Just a class that prints, for testing purposes only.
    """
    def process_item(self, item):
        print item
        return item


class ExtractKeysStreamProcessor(NanoStreamProcessor):
    """
    Just extracts the keys from a dictionary. For testing.
    """
    def process_item(self, item):
        output = item.keys()
        return output

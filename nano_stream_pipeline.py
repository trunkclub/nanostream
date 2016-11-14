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
import networkx as nx
import Queue
import threading
import time
from nano_stream_processor import NanoStreamProcessor, NanoStreamListener, NanoStreamSender, NanoStreamListenerMultiplex


DEFAULT_MAX_QUEUE_SIZE = 128


class NanoStreamGraph(object):
    """
    They're actually directed graphs.
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_list = []  # nodes are listeners, processors, etc.
        self.edge_list = []  # edges are queues
        self.thread_list = []  # We'll add these when `start` is calledt
        self.workers = []  # A list of functions to execute intermittantly
        self.worker_interval = None
        self.offset_dictionary = {}

    def add_node(self, node):
        self.node_list.append(node)
        self.graph.add_node(node)
        node.parent = self

    def add_edge(self, *ordered_nodes, **kwargs):
        """
        Create an edge connecting `source` to `target`. The edge
        is really just a queue
        """
        max_queue_size = kwargs.get('max_queue_size', DEFAULT_MAX_QUEUE_SIZE)
        if len(ordered_nodes) < 2:
            raise Exception("Adding edges requires >= 2 nodes.")
        for index in range(len(ordered_nodes) - 1):
            source = ordered_nodes[index]
            target = ordered_nodes[index + 1]
            if source not in self.node_list:
                self.add_node(source)
            if target not in self.node_list:
                self.add_node(target)
            if isinstance(target, NanoStreamListenerMultiplex):
                target_list = target.listeners
            else:
                target_list = [target]
            for target in target_list:
                edge_queue = target.input_queue or Queue.Queue(max_queue_size)
                self.graph.add_edge(source, target, {'edge_queue': edge_queue})
                source.output_queue_list.append(edge_queue)
                target.input_queue = edge_queue

    def add_worker(self, worker_object, interval=3):
        self.workers.append((worker_object, interval,))
        worker_object.parent = self 
        
    def start(self, block=False):
        """
        We check whether any of the nodes have a "run_on_start" function.
        """
        for node in self.graph.nodes():
            if hasattr(node, 'run_on_start'):
                node.run_on_start()
        for node in self.graph.nodes():
            worker = threading.Thread(target=node.start)
            worker.setDaemon(True)
            self.thread_list.append(worker)
            worker.start()
        for worker_tuple in self.workers:
            if not isinstance(worker_tuple[0], NanoGraphWorker):
                raise Exception("Needs to be a NanoGraphWorker")
            worker_tuple[0].graph = self
        
            def _thread_worker(self):
                while 1:
                    time.sleep(worker_tuple[1])
                    worker_tuple[0].worker()
            
            thread_worker = threading.Thread(
                target=_thread_worker, args=(self,))
            thread_worker.setDaemon(True)
            thread_worker.start()
            if block:
                thread_worker.join()


class NanoGraphWorker(object):
    """
    Subclass this, and override the `worker` method. Call `add_worker`
    on the `NanoStreamGraph` object.
    """
    def __init__(self):
        pass

    def worker(self, *args, **kwargs):
        raise NotImplementedError("Need to override worker method")


class NanoPrinter(NanoStreamProcessor):
    def process_item(self, message):
        pass
        # print message


def test_multiplexer():

    class NanoCounter(NanoStreamSender):
   
        def __init__(self):
            self.counter = 0
            super(NanoCounter, self).__init__()
        
        def start(self):
            while 1:
                output = 'NanoCounter:' + str(self.counter)
                self.counter += 1
                self.queue_message(output)

    
    class NanoMultiPrint(NanoStreamListener):
        def process_item(self, message):
            print message
            time.sleep(1)

    nano_counter = NanoCounter()
    nano_multi_print = NanoMultiPrint(workers=3)
    import pdb; pdb.set_trace()
    pipeline = NanoStreamGraph()
    pipeline.add_edge(nano_counter, nano_multi_print)
    pipeline.start()



if __name__ == '__main__':
    test_multiplexer()
    
def bar():    
    import nano_kafka
    from nano_stream_processor import NanoStreamProcessor

    class NanoPrinter(NanoStreamProcessor):
        def process_item(self, message):
            pass

    class PrintFooWorker(NanoGraphWorker):
        def worker(self):
            print 'foo'
            print self.__dict__

    collect_offsets_worker = nano_kafka.CollectKafkaOffsets()

    my_printer = NanoPrinter()
    my_foo_printer = PrintFooWorker()
    some_listener = nano_kafka.NanoKafkaListener(
        topics=['public.members.v1'])
    pipeline = NanoStreamGraph()
    pipeline.add_node(some_listener)
    pipeline.add_node(my_printer)
    pipeline.add_edge(some_listener, my_printer)
    pipeline.add_worker(my_foo_printer)
    # pipeline.start()

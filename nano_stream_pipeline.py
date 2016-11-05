import networkx as nx
import Queue
import threading
import time
from trunk_club_streams.tc_stream_processor import TrunkClubStreamProcessor


DEFAULT_MAX_QUEUE_SIZE = 128


class TrunkClubStreamGraph(object):
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
            edge_queue = target.input_queue or Queue.Queue(max_queue_size)
            self.graph.add_edge(source, target, {'edge_queue': edge_queue})
            source.output_queue_list.append(edge_queue)
            target.input_queue = edge_queue

    def add_worker(self, worker_object, interval=3):
        self.workers.append((worker_object, interval,))
        worker_object.parent = self 
        
    def start(self, block=False):
        for node in self.graph.nodes():
            worker = threading.Thread(target=node.start)
            worker.setDaemon(True)
            self.thread_list.append(worker)
            worker.start()
        for worker_tuple in self.workers:
            if not isinstance(worker_tuple[0], TrunkClubGraphWorker):
                raise Exception("Needs to be a TrunkClubGraphWorker")
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


class TrunkClubGraphWorker(object):
    """
    Subclass this, and override the `worker` method. Call `add_worker`
    on the `TrunkClubStreamGraph` object.
    """
    def __init__(self):
        pass

    def worker(self, *args, **kwargs):
        raise NotImplementedError("Need to override worker method")


class TrunkClubPrinter(TrunkClubStreamProcessor):
    def process_item(self, message):
        pass
        # print message


if __name__ == '__main__':
    import tc_kafka
    from tc_stream_processor import TrunkClubStreamProcessor

    class TrunkClubPrinter(TrunkClubStreamProcessor):
        def process_item(self, message):
            pass

    class PrintFooWorker(TrunkClubGraphWorker):
        def worker(self):
            print 'foo'
            print self.__dict__

    collect_offsets_worker = tc_kafka.CollectKafkaOffsets()

    my_printer = TrunkClubPrinter()
    my_foo_printer = PrintFooWorker()
    some_listener = tc_kafka.TrunkClubKafkaListener(
        topics=['public.members.v1'])
    pipeline = TrunkClubStreamGraph()
    pipeline.add_node(some_listener)
    pipeline.add_node(my_printer)
    pipeline.add_edge(some_listener, my_printer)
    pipeline.add_worker(my_foo_printer)
    pipeline.start()

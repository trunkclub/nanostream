import sys
import yaml
import time
from nanostream_processor import *
from nanostream_pipeline import NanoStreamGraph
from nanostream_file_handler import FileReader, FileWriter
from nanostream_watchdog import WatchdogDirectoryListener


class NanoStreamCounter(NanoStreamSender):
    def start(self):
        print 'starting...'
        iteration = 1
        while 1:
            print 'iteration...', iteration
            self.queue_message('Hi!')
            print self.output_queue_list[0].queue.qsize()
            time.sleep(1)
            iteration += 1
    
if __name__ == '__main__':
    PIPELINE_CONFIG_FILE = sys.argv[1]

    with open(PIPELINE_CONFIG_FILE, 'r') as pipeline_file:
        pipeline_config = yaml.load(pipeline_file)

    print pipeline_config

    node_obj_dict = {}

    for node_config in pipeline_config['node_sequence']:
        node_class = globals()[node_config['class']]
        del node_config['class']
        node_name = node_config['name']
        del node_config['name']
        parents = node_config.get('parents', [])
        try:
            del node_config['parents']
        except KeyError:
            pass
        node_obj = node_class(**node_config)
        node_config['node_obj'] = node_obj
        node_config['class'] = node_class
        node_config['name'] = node_name
        node_config['parents'] = parents
        node_obj_dict[node_name] = node_obj

    nanostream_graph = NanoStreamGraph()
    for node_name, node_obj in node_obj_dict.iteritems():
        nanostream_graph.add_node(node_obj)
    for node_config in pipeline_config['node_sequence']:
        child_node = node_obj_dict[node_config['name']]
        for parent in node_config['parents']:
            parent_node = node_obj_dict[parent]
            print parent_node, '>>', child_node
            nanostream_graph.add_edge(parent_node, child_node)
    nanostream_graph.start()

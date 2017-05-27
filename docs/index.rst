.. NanoStream documentation master file, created by
   sphinx-quickstart on Sat May 27 19:32:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NanoStream
==========

The purpose of NanoStream is to enable us to use the very nice design patterns
afforded by large-scale streaming frameworks such as Spark or Storm, but
without the heavyweight dependencies and infrastructure requirements. I expect
some version of this to be useful for ETL work, especially.

NanoStream defines a class called ``NanoStreamProcessor`` which reads incoming
data from a queue, and does something with it, optionally passing the results
to another ``NanoStreamProcessor`` downstream. These classes are instantiated
and linked to each other in a directed acyclic graph (think of a flowchart with
no loops) known as a ``NanoStreamGraph`` or "pipeline".

For example, it's easy to write design a pipeline that watches for new files
to appear in a directory, read them, transform them somehow, and publish the
results to Kafka. In this example, there would be four nodes in your
pipeline, where each node is an instance of a class designed to perform a
single task. The first is a ``DirectoryListener``, the second is a ``FileReader``,
the third is some other class that (e.g.) validates the file or performs a
computation, and the fourth would be a ``KafkaProducer``. Those three classes
are pre-defined in the ``NanoStream`` package, so you shouldn't have to write
any code whatsoever in order to use them. Instead, you'd set up the pipeline
in a simple configuration file.

If you need to do something that doesn't exist in one of the classes already,
you can write your own with minimal hassle. It would follow this template:

.. code::

   class MyAmazingClass(NanoStreamProcessor):

       def process_item(self, message):
           DO SOMETHING WITH message
           return result

By inheriting from ``NanoStreamProcessor``, you get all the functionality
required to incorporate ``MyAmazingClass`` into a pipeline. The only
thing you are required to do is provide a method called ``process_item``
that does the actual work and returns the result. Anything you return
will be passed downstream to the appropriate nodes in your pipeline. Any
pickle-able Python object can be sent through the pipeline.

All nodes work in their own threads, so there are no bottlenecks. Of course,
you're not getting true multiprocessing, as Python threads all operate in
the same core. There is experimental code to use true multiprocessing instead
of threading, but it should not (yet) be considered safe.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Configuration files for ``NanoStream`` pipelines look like this:

.. code::

    pipeline_name: watchdog_example
    node_sequence:
      - name: watchdog
        class: WatchdogDirectoryListener
        watchdog_path: inbox
      - name: printer
        class: PrintStreamProcessor 
        parents:
          - watchdog
      - name: read_the_file
        class: FileReader
        parents:
          - watchdog
      - name: copy_the_file
        class: FileWriter
        parents:
          - read_the_file
        path: outbox

These files are in YAML format; the description of the pipeline is
under the key ``node_sequence``. Each node sequence requires
a unique name, the name of the class that will be used, any parents
of the node (i.e. the nodes which send their results to its queue),
and any parameters that are to be sent to the class's constructor
(if any).

To run the pipeline, do: ``python -i pipeliner.py CONFIG_FILE``, which
will read your configuration file, instantiate the appropriate
``NanoStreamGraph``, and start it.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

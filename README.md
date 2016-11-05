# nanostream: Small-scale streaming data

Streaming data tools such as Storm, Flink, and Sparq allow you to set up a data
processing pipeline in a clear, intuitive manner. You work on creating each
processor in the pipeline, and then stitch those together, with appropriate
data sources and sinks.

That workflow is not only useful for processing huge amounts of data in a
heavyweight production environment. Sometimes, it would be nice to set up a
pipeline that won't have to handle zillions of messages, and consequently,
wouldn't depend on a large, complex streaming data tool.  This is what
`nanostreams` is for.

To use `nanostreams`, you inherit from a couple of simple mix-in classes, write
your pipeline steps in pure Python, and connect them. Your pipeline will have a
`start` method that will run everything asynchronously. It'll use back-pressure
to prevent any queues from becoming overrun.

This package trades off scalability for simplicity. If you're Facebook, you
won't want to use `nanostreams`. But let's face it: you're not Facebook, and
odds are that your data is not Big(tm). Your data is probably Big Enough(tm)
that you have to think about efficiency, but not so Big(tm) that it justifies
putting a whole new platform into your production environment.

The `nanostreams` package lets you write a simple, asynchronous data processing
pipeline as easily as possible, with no heavyweight dependencies whatsoever.
You can plug your processing steps together in whatever configuration you like,
and set up and tear down your pipeline all in one place, with no remote calls
to servers, no fancy configuration files, and without ever adding any more work
to your devops team.

The package includes classes for reading from and writing to Kafka. This allows
you to (e.g.) listen to several Kafka topics at the same time, process the
messages however you like (asynchronously, so your throughput will be pretty
quick), and if you like, emit the results back to Kafka.

We use this tool for a lot of ETL work, where we listen to lots of Kafka topics
simultaneously, aggregate the messages, push the results into databases, or
publish them to other topics, where they can be picked up for further
processing. We could have used Storm or its various cousins to do the same
thing, but we can easily process thousands of Kafka messages per second and
accomplish the same thing with a fraction of the hassle, and no extra work for
devops.

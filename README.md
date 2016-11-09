# nanostream: Small-scale streaming data

Streaming data tools such as Storm, Flink, and Sparq allow you to set up a data
processing pipeline in a clear, intuitive manner. You work on creating each
processor in the pipeline, and then stitch those together into a directed
graph, with appropriate data sources and sinks. This is a very clear and practical
design pattern.

That workflow isn't just useful for processing huge amounts of data. It can be
just as useful for smaller problems. But the smaller data sets
don't justify installing, learning, configuring, and maintaining a heavyweight
system like Storm, Flink, or Sparq. It would be nice to have a system that
combined the clarity of the stream-processing pattern with the simplicity and
light footprint of a Python module. This is what `nanostream` is for.

To use `nanostream`, you inherit from a couple of simple mix-in classes, write
your pipeline steps in pure Python, and connect them in a directed graph
topology. Your pipeline will have a `start` method that will run everything
asynchronously. It'll use back-pressure to prevent any queues from becoming
overrun. Everything runs in-memory, making it pretty fast.

# Intended audience

This package trades off scalability for simplicity. It does not try to
replicate the functionality of the well-known, large-scale stream processing
frameworks that are out there already.  If you're Facebook, you won't want to
use `nanostream`. But let's face it: you're not Facebook, and the odds are that
your data is not "Big".

There's a vast middle-ground between "Small" data that doesn't demand a careful
implementation strategy, and "Big" data that requires large, distributed
processing. That middle-ground is "Big Enough" data: it demands efficiency and
clear, reusable design patterns, but doesn't justify adding greater complexity
to your infrastructure. Most business needs are driven by "Big Enough" data.

# What it is

The `nanostream` package lets you write a simple, asynchronous data processing
pipeline as easily as possible, with no heavyweight dependencies whatsoever.
You can plug your processing steps together in whatever configuration you like,
and set up and tear down your pipeline all in one place, with no remote calls
to servers, no fancy configuration files, and without adding any more work to
your devops team. You write in pure Python, and you can pass any pickle-able
object through the pipeline.

The package includes classes for reading from and writing to Kafka. This allows
you to (e.g.) listen to several Kafka topics at the same time, process the
messages however you like (asynchronously, so your throughput will be pretty
quick), and if you like, emit the results back to Kafka.

We (at Trunk Club) use this tool for a lot of ETL work. It listens to lots of
Kafka topics simultaneously, aggregates the messages, transforms them, and
finally pushes the results into databases or publishes them to other Kafka
topics. We've found that we can process a few thousand events per second using
`nanostream`, while requiring nothing more than a `pip install` to get running.

# This is an alpha release

This package has all the flaws you'd expect from an alpha release. I'm working
on documentation now, writing unit tests, cleaning up code, and so on. Although
we use it in production, it's not the kind of package you'd want to blithely
install and use. That being said, if you are very brave, you can `pip install
nanostream` to get it.

Expect this repo to be under very active development.

`zernst@trunkclub.com`

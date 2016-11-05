# nanostream: Small-scale streaming data

You'd like to set up a pipeline for stream processing, and you know
that Storm, Flink, or Sparq would work. But you're not in the
"big data" business. You don't need a distributed system with servers
and clients. If you were to use these "heavyweight" tools, it would
be like hitting a mosquito with a pile of cannonballs. But it sure
would be nice to set up a streaming data pipeline without all the
overhead.

If that's your situation, then you're the intended audience for
`nanostream`. Nanostream makes it very easy to process streaming
data in a pipeline with parallelism and multithreading. You can
create simple processing steps in pure Python with no boilerplate,
and configure them in a simple, intuitive manner. The stream processing

Sometimes, you want the functionality of a streaming data service like
Storm, Flink, or Sparq, but the scale of your data doesn't require
such a heavy system.

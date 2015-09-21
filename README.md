# Introduction

This is the HW 2 submission for Ahsen Uppal and Teo Georgiev. This
shows an example of a Python-based proxy conversion server. This proxy
server reads a list of conversion server resources from a file. It
then builds an internal graph representation of the conversion server
network, and processes conversion requests by doing a shortest-path
traversal through the conversion network.

Because there was such a large number of unidirectional conversion
servers to launch and manage, we decided to write these ourselves. But
we can use any internet-connected conversion servers as specified in
the conversion_servers.txt file that the proxy server reads.

Note the proxy server requires Scipy for matrix support.
On Ubuntu, you can do ```sudo apt-get install scipy```.

There is a launch.sh script for starting the network of unidirectional
conversion servers. Some of these servers are in Python and some are
in Java. The provided launch.sh script starts 18 unidirectional
conversion servers.

# Files

We have submitted the following files:
```
README.md       : This file
launch.sh       : Launch script for 18 conversion servers + 1 proxy server.
ConvServer.java : Java-based conversion server. By default, this
                  program runs a ft to in conversion server, but
                  with optional command-line arguments, it can run as
                  an any unit to any unit conversion server.
convServer.py   : Python-based conversion server. By default, this
                  program runs a in to cm conversion server, but
                  with optional command-line arguments, it can run as
                  an any unit to any unit conversion server.
proxy_conv_server.py : Python-based proxy-server. It reads a list of
                       conversion servers from a file. It then builds
                       an internal graph representation of the
                       conversion server network, and processes
                       conversion requests by doing a shortest-path
                       traversal through the conversion network.
trace.txt       : Example of a multi-step "cool" conversion showing a
                  7-step conversion from cm to g.
```

# Running

To run all of the software, first build the java server:
```
javac ConvServer.java
```

Then launch all of the conversion servers (mix of Python and Java-based):
```
./launch.sh
```

# Multi-step Cool Conversions

The launch.sh and conversion_servers.txt specify this conversion
server network:

```
cm <-> in <-> ft <-> m <-> b <-> kg <-> lbs <-> g
                           ^
                           |
                           `--> y <-> $
```
Each bi-directional edge represents two launched conversion server
instances, one for each direction.

Because the proxy server performs a full Floyd-Warshall all pairs
shortest path traversal, it can convert any unit to any other unit if
provided with a fully-connected network of conversion servers.
For example, a cm to g conversion goes through 7 hops. The following
trace shows this conversion while:
```echo 'cm g 30' | nc localhost 5555``` 
is executed on a separate command-line.

Output of netcat client:
```
>echo 'cm g 30' | nc localhost 5555
Welcome, you are connected to a Python-based proxy unit conversion server
210.91113610798647
```

Output of launced conversion servers and proxy server (running on port
5555):
```
Script started on Sun Sep 20 22:52:35 2015
>./launch.sh
Started Python-based ft to m conversion server on port 5570
Started Python-based cm to in conversion server on port 5575
Started Python-based b to kg conversion server on port 5582
Started Python-based y to $ conversion server on port 5580
Started Python-based b to y conversion server on port 5578
Started Python-based y to b conversion server on port 5579
Started Python-based m to b conversion server on port 5577
Started Python-based in to ft conversion server on port 5573
Started Python-based g to lbs conversion server on port 5587
Started Python-based lbs to g conversion server on port 5586
Started Python-based kg to lbs conversion server on port 5584
Started Python-based $ to y conversion server on port 5581
Started Python-based kg to b conversion server on port 5583
Started Python-based m to ft conversion server on port 5571
Started Python-based b to m conversion server on port 5576
Started Java-based ft to in conversion server on port 5572
Started Java-based ft to in conversion server on port 5574
Started Java-based lbs to kg conversion server on port 5585
Started Python-based proxy conversion server.
Edges:
[[0 1 0 1 0 0 0 0 0 0]
 [1 0 1 0 0 0 0 0 0 0]
 [0 1 0 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 0 1 0 0]
 [0 0 0 0 0 0 1 1 0 0]
 [0 0 0 0 0 0 1 0 0 0]
 [0 0 0 0 1 1 0 0 0 0]
 [0 0 0 1 1 0 0 0 0 1]
 [0 0 0 0 0 0 0 0 0 1]
 [0 0 0 0 0 0 0 1 1 0]]
Next paths:
[[-1  1  1  3  3  3  3  3  3  3]
 [ 0 -1  2  0  0  0  0  0  0  0]
 [ 1  1 -1  1  1  1  1  1  1  1]
 [ 0  0  0 -1  7  7  7  7  7  7]
 [ 7  7  7  7 -1  6  6  7  7  7]
 [ 6  6  6  6  6 -1  6  6  6  6]
 [ 4  4  4  4  4  5 -1  4  4  4]
 [ 3  3  3  3  4  4  4 -1  9  9]
 [ 9  9  9  9  9  9  9  9 -1  9]
 [ 7  7  7  7  7  7  7  7  8 -1]]
Proxy server listening on port 5555
Accepted connection from client ('127.0.0.1', 49361)
Received message: cm g 30

Query cm in 30.0 to server at localhost 5575.
Accepted connection from client ('127.0.0.1', 39176)
Received message:  cm in 30.0

Proxy request returning 11.811023622047244
Query in ft 11.811023622047244 to server at localhost 5573.
Accepted connection from client ('127.0.0.1', 43498)
Received message:  in ft 11.811023622047244

Proxy request returning 0.9842519685039369
Query ft m 0.9842519685039369 to server at localhost 5570.
Accepted connection from client ('127.0.0.1', 35208)
Received message:  ft m 0.9842519685039369

Proxy request returning 0.3
Query m b 0.3 to server at localhost 5577.
Accepted connection from client ('127.0.0.1', 33881)
Received message:  m b 0.3

Proxy request returning 1.6872890888638918
Query b kg 1.6872890888638918 to server at localhost 5582.
Accepted connection from client ('127.0.0.1', 36248)
Received message:  b kg 1.6872890888638918

Proxy request returning 0.21091113610798648
Query kg lbs 0.21091113610798648 to server at localhost 5584.
Accepted connection from client ('127.0.0.1', 37430)
Received message:  kg lbs 0.21091113610798648

Proxy request returning 0.46497946186349315
Query lbs g 0.46497946186349315 to server at localhost 5586.
Accepted connection from client ('127.0.0.1', 44625)
Received message:  lbs g 0.46497946186349315

Proxy request returning 210.91113610798647
^CExiting...
Script done on Sun Sep 20 22:52:50 2015
```

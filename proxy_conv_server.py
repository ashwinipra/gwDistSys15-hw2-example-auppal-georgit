#!/usr/bin/env python

# Ahsen Uppal
# and
# Teo Georgiev

#
#  CS 6421 - Python-based proxy conversion server. 
#  It reads a list of conversion servers from a file. It then builds
#  an internal graph representation of the conversion server network,
#  and processes conversion requests by doing a shortest-path
#  traversal through the conversion network.
#
#  Execution:    python proxy_conv_server.py portnum [conversion-servers-input-file]
#


import sys, socket
import numpy as np

BUFFER_SIZE = 1024

proxy_table = {}

# A list of all available units, and conversions to and from unit ids
units = ('ft', 'in', 'cm', 'm', 'kg', 'g', 'lbs', 'b', '$', 'y')
n_units = len(units)
unit_to_id = {}
id_to_unit = {}
for i,e in enumerate(units):
    unit_to_id[e] = i
    id_to_unit[i] = e


MAX_DIST = 99

# Find paths using the Floyd-Warshall
# algorithm for all-pairs shortest distances.
def compute_distances(edges, n_units):
    dist = np.zeros((n_units, n_units), dtype=int)
    next = np.empty((n_units, n_units), dtype=int)
    next.fill(-1)

    for i in range(n_units):
        for j in range(n_units):
            dist[i][j] = MAX_DIST

    for i in range(n_units):
        dist[i][i] = 0

    for i in range(n_units):
        for j in range(n_units):
            if edges[i][j] > 0:
                dist[i][j] = edges[i][j]
                next[i][j] = j

    for k in range(n_units):
        for i in range(n_units):
            for j in range(n_units):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next[i][j] = next[i][k]

    return (next, dist)

# Path reconstruction from next-neighbor matrix.
def get_path(next, src, dst):
    path = []
    u = unit_to_id[src]
    v = unit_to_id[dst]

    if next[u, v] == -1:
        return path

    while u != v:
        u = next[u, v]
        path.append(u)

    return path
    
# Issue a request to a conversion server and return the result
def proxy_request(src_unit, dst_unit, amount, host, port):
    msg = '%s %s %s\n' % (src_unit, dst_unit, amount)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.sendall(msg.encode('UTF-8'))
    greeting = s.recv(BUFFER_SIZE)
    converted = s.recv(BUFFER_SIZE)
    value = float(converted.decode('UTF-8'))
    print("Proxy request returning %s" % value)
    return value


def process(conn, next):
    greeting = "Welcome, you are connected to a Python-based proxy unit conversion server\n"
    conn.send(greeting.encode('UTF-8'))
    userInput = conn.recv(BUFFER_SIZE).decode('UTF-8')
    if not userInput:
        print("Error reading message")
        return

    print("Received message: %s" % (userInput))
    tokens = userInput.split()
    input_unit,output_unit,amount = tokens

    p = get_path(next, input_unit, output_unit)

    if not p:
        msg = "Could not find a suitable input conversion server :(\n"
        print(msg)
        conn.send(msg.encode('UTF-8'))
        return

    u = unit_to_id[input_unit]
    c = float(amount)
    for i in p:
        v = i
        s,d = id_to_unit[u],id_to_unit[v]
        host,port = proxy_table[(s,d)]
        print ('Query %s %s %s to server at %s %s.' % (s,d, c, host, port))
        c = proxy_request(s, d, c, host, port) 
        u = v

    conn.send(("%s\n" % c).encode('UTF-8'))


if __name__ == '__main__':

    if len(sys.argv) < 3:
        sys.stderr.write("usage: python {0} port conversion-servers.txt\n".format(sys.argv[0]))
        sys.exit(1)

    server_port = int(sys.argv[1])
    with open(sys.argv[2]) as f:
        for l in f:
            try:
                host,port,input_unit,output_unit = l.split()
                proxy_table[(input_unit, output_unit)] = (host, port)
            except:
                pass

    edges = np.zeros((n_units, n_units), dtype=int)
    for i in proxy_table.items():
        u0 = i[0][0]
        u1 = i[0][1]
        edges[unit_to_id[u0]][unit_to_id[u1]] = 1

    next,dist = compute_distances(edges, n_units)

    print ("Started Python-based proxy conversion server.")
    print('Edges:')
    print(edges)
    print('Next paths:')
    print(next)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", server_port))
    s.listen(5)
    exit_flag = False
    try:
        print ("Proxy server listening on port %s" % (server_port))
        while not exit_flag:
            conn, addr = s.accept()
            print ('Accepted connection from client %s' % str(addr))
            try:
                process(conn, next)
            except:
                print ('Failed to process request from client.')
            conn.close()
    except KeyboardInterrupt:
        exit_flag = True

    print("Exiting...")
    s.close()
    sys.exit(0)

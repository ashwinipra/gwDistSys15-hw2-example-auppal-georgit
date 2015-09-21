#!/usr/bin/env python
# Ahsen Uppal
# and
# Teo Georgiev

#
#  CS 6421 - Simple Python based conversion server. 
#  By default, it is an in to cm conversion server, but with optional
#  command-line arguments, it can run as any type of conversion
#  server.
#
#  Execution:    python convServer.py portnum [unit1 unit2]
#


import socket
import sys

length_units = {'ft' : 0.3048,
                'in' : 0.0254,
                'cm' : 0.01,
                'm'  : 1.0,
                'b'  : 0.1778,
}

mass_units = {'kg'  : 1.0,
              'g'   : 0.001,
              'lbs' : 0.45359237,
              'ounces' : 0.0283495231,
              'b'   : 0.125,
}

currency_units = {'$'  : 1.0,
                  'y'  : 0.008319,
                  'b'  : 0.19,
}

def process(conn, force_src_unit=None, force_dst_unit=None):
    greeting = "Welcome, you are connected to a Python-based %s to %s conversion server\n" % (force_src_unit, force_dst_unit)
    conn.send(greeting.encode('UTF-8'))
    userInput = conn.recv(BUFFER_SIZE).decode('UTF-8')
    if not userInput:
        print("Error reading message")
        return

    print("Received message: ", userInput)
    tokens = userInput.split()
    input_unit,output_unit,amount = tokens

    try:
        amount = float(amount)
    except:
        conn.send(("Invalid amount: %s\n" % (amount).encode('UTF-8')))
        return

    found = False
    for d in (length_units, mass_units, currency_units):
        if input_unit in d and output_unit in d:
            converted = amount * d[input_unit] / d[output_unit]
            found = True
            break
    if not found:
            conn.send(("Incompatible units %s and %s\n" % (input_unit,output_unit)).encode('UTF-8'))
            return

    if (force_src_unit and force_src_unit != input_unit) or (force_dst_unit and force_dst_unit != output_unit):
            conn.send(("Sorry, this is a %s to %s server\n" % (force_src_unit, force_dst_unit)).encode('UTF-8'))
            return

    conn.send(("%s\n" % converted).encode('UTF-8'))

if __name__ == '__main__':
    force_src_unit = 'in'
    force_dst_unit = 'cm'
    BUFFER_SIZE = 1024
    interface = ""

    if len(sys.argv) < 2:
        sys.stderr.write("usage: python {0} portnum\n".format(sys.argv[0]))
        sys.exit(1)

    portnum = int(sys.argv[1])

    if len(sys.argv) > 3:
        force_src_unit = sys.argv[2]
        force_dst_unit = sys.argv[3]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((interface, portnum))
    s.listen(5)
    exit_flag = False
    try:
        print("Started Python-based %s to %s conversion server on port %s" % (force_src_unit, force_dst_unit, portnum))
        while not exit_flag:
            conn, addr = s.accept()
            print ('Accepted connection from client', addr)
            try:
                process(conn, force_src_unit, force_dst_unit)
            except:
                print ('Failed to process request from client.')
            conn.close()
    except KeyboardInterrupt:
        exit_flag = True

    print("Exiting...")
    s.close()
    sys.exit(0)

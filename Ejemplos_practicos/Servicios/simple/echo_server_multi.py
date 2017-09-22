#!/usr/bin/python
#-*- coding: utf-8-*-
# Echo server múltiple connexiones concurrentes
# 07/09/2017
# ----------------------------------------------------------------------

import socket, sys, select

HOST = ''                 
PORT = 50007             
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conns=[s]

while True:
    actius,x,y = select.select(conns,[],[])
    for actual in actius:
        if actual == s:
            conn, addr = s.accept()
            print 'Connected by', addr
            conns.append(conn)
        else:
            data = actual.recv(1024)
            if not data:
                sys.stdout.write("Client finalizado: %s \n" % (actual))
                actual.close()
                conns.remove(actual)
            else:
                actual.sendall(data)
s.close()

sys.exit(0)

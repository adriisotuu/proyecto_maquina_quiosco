#!/usr/bin/python
#-*- coding: utf-8-*-
# SERVIDOR
# telnet-server.py
# 12/09/2017
# ----------------------------------------------------------------------

import os, sys, socket, select
from subprocess import Popen,PIPE

HOST = ''
PORT = 50023

print os.getpid()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conns = [s]

while True:
	actius,x,y = select.select(conns,[],[])
	for actual in actius:
		if actual == s:
			conn, addr = s.accept()
			print 'Conectado por', addr
			conns.append(conn)
		else:
			command = actual.recv(1024)
			if not command:
				sys.stderr.write("Conexión cerrada por el cliente\n")
				actual.close()
				conns.remove(actual)
			else:
				pipeData = Popen(command,shell=True, stdout=PIPE, stderr=PIPE)
				for line in pipeData.stdout:
					actual.send(line)
				for line in pipeData.stderr:
					actual.send(line)
				actual.sendall(chr(4),socket.MSG_DONTWAIT)
s.close()

sys.exit(0)

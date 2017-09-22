#!/usr/bin/python
#-*- coding: utf-8-*-
# CLIENTE
# telnet-client.py
# 12/09/2017
# ----------------------------------------------------------------------

import sys, socket

HOST = ''
PORT = 50023

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT))

while True:
	command = raw_input('telnet> ')
	if not command: continue
	if command in ["quit","q"]: break
	s.sendall(command)
	while True:
		dataRecv = s.recv(1024)
		if dataRecv[-1] == chr(4):
			sys.stdout.write(dataRecv[:-1])
			break
		sys.stdout.write(dataRecv)

s.close()

sys.exit(0)

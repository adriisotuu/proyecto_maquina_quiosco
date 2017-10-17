#!/usr/bin/python
#-*- coding: utf-8-*-
# SERVIDOR
# server-psax.py
# 08/09/2017
# ----------------------------------------------------------------------

import socket, sys, select

import os, sys, socket, signal, time
from subprocess import Popen, PIPE

PIDFile = "/var/run/server-psax.pid"

pid = os.fork()

# Proceso padre
if pid != 0:
	fileIn = open(PIDFile,'w')
	fileIn.write('%s\n' %(pid))
	fileIn.close()
	
	sys.exit(0)

# Proceso hijo
HOST = ''
PORT = 50000

# Lista de tuplas [(IP, TIMESTAMP),(...),(...)]
allClients = []
# Lista de IPs diferentes
differentClients = []

def handlerTerm(signum,frame):
	sys.stdout.write("Servidor finalitzado\n")
	sys.exit(1)
	
def handlerUsr1(signum,frame):
	global allClients
	sys.stdout.write("Listado de clientes que se han conectado:\n")
	for e in allClients:
		sys.stdout.write("%-20s %s\n" %(e[0],e[1]))
	sys.stdout.write("Servidor finalitzado\n")
	sys.exit(2)
	
def handlerUsr2(signum,frame):
	global differentClients
	sys.stdout.write("Clientes que se han conectado:\n")
	differentClients.sort()
	for e in differentClients:
		sys.stdout.write("%s\n" %(e))
	sys.stdout.write("Servidor finalitzado\n")
	sys.exit(3)

signal.signal(signal.SIGTERM,handlerTerm)
signal.signal(signal.SIGUSR1,handlerUsr1)
signal.signal(signal.SIGUSR2,handlerUsr2)

## Crear socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

sys.stderr.write("Servidor iniciado\n")
sys.stderr.write("%d\n" %(os.getpid()))

while True:
	conn, addr = s.accept()
	ipClient = addr[0]
	sys.stderr.write("Conectado por %s\n" %(ipClient))
	timestamp = time.strftime("%Y%m%d_%H:%M:%S")
	allClients.append((ipClient, timestamp))
	if ipClient not in differentClients:
		differentClients.append(ipClient)
	nameFile = "/tmp/psax-%s-%s.log" %(ipClient, timestamp)
	fileIn = open(nameFile,'w')
	while True:
		dataRecv = conn.recv(1024)
		if not dataRecv: break
		fileIn.write(dataRecv)
	fileIn.close()
	conn.close()

sys.exit(0)

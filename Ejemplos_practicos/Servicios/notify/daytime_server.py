#!/usr/bin/python
#-*- coding: utf-8-*-
# SERVIDOR DAYTIME
# daytime_server.py
# 15/09/2017
# ----------------------------------------------------------------------

import os,sys,socket
from subprocess import Popen,PIPE
# dnf install python-systemd
from systemd.daemon import notify

HOST = ''
PORT = 50013

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

sys.stderr.write("%s\n" %(os.getpid()))

# Enviar READY=1; Indica a systemd que el inicio del servicio ha finalizado.
notify('READY=1')

while True:
	conn, addr = s.accept()
	sys.stderr.write("Conectado por %s\n" %(addr[0]))
	
	# Enviar una cadena de estado a systemd que describe el estado del servicio.
	notify('STATUS=Conectado por %s\n' %(addr[0]))
	
	command = "/usr/bin/date"
	pipeData = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
	for line in pipeData.stdout:
		conn.sendall(line)
	conn.close()

# Enviar STOPPING=1; Indica a systemd que el servicio está iniciando su parada.
notify('STOPPING=1')

sys.exit(0)

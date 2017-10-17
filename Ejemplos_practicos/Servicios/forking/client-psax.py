#!/usr/bin/python
#-*- coding: utf-8-*-
# CLIENTE
# client-psax.py -s|--server host
# 08/09/2017
# ----------------------------------------------------------------------

import argparse,sys,socket
from subprocess import Popen,PIPE

PORT = 50000

#1 CONTROL DE ARGUMENTOS
parser = argparse.ArgumentParser(description='client-psax.py -s|--server host')

parser.add_argument('-s', '--server', dest='hostArg', metavar='host', help='host a conectar', required=True)

args = parser.parse_args()
HOST = args.hostArg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

command = "/usr/bin/ps ax"

pipeData = Popen(command,shell=True, stdout=PIPE, stderr=PIPE)
for line in pipeData.stdout:
	s.sendall(line)
	
s.close()

sys.exit(0)

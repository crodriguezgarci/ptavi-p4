#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])

# Método al que pertenecerá el mensaje.
    METODO = sys.argv[3]
# Nombre de usuario.
    USUARIO = sys.argv[4]
#Tiempo de expiración.
    EXPIRES = sys.argv[5]
except IndexError:
    print "Usage: client.py ip puerto register sip_address expires_value"
    exit()
#Contenido del mensaje.
LINE = METODO.upper() + " sip:" + USUARIO + " SIP/2.0\r\n"
LINE = LINE + "Expire: " + EXPIRES + "\r\n\r\n"
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto.
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))
#Enviamos el mensaje de respuesta.
print "Enviando: " + LINE + USUARIO
my_socket.send(LINE)
#Recibimos y sacamos la información de los nuevos mensajes recibidos.
data = my_socket.recv(1024)
print 'Recibido -- ', data
print "Terminando socket..."
# Cerramos todo.
my_socket.close()
print "Fin."

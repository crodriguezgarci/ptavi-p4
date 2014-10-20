#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        self.registro = {}
        print "Petición recibida del Cliente: ",
        print "IP:" + str(self.client_address[0]),
        print " Puerto: " + str(self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            print line
            line = line.split()
            if line[0] == "REGISTRER" and line[2] == "SIP/1.0":
                line[1] = line[1].split(":")
                self.registro[str(self.client_address[0])] = line[1][1]
                self.wfile.write(line[2] + "200 OK\r\n\r\n")
if __name__ == "__main__":
    PORT = int(sys.argv[1])
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT ), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()

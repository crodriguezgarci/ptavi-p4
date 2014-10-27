#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

registro = {}


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def borrar_caducados(self,registro):
        self.lista_aux = []
        for key in registro:
            if time.time() >= float(registro[key][2]) + float(registro[key][1]):
               	self.lista_aux.append(key)
        for key in self.lista_aux:
            del registro[key]

    def register2file(self,registro):
        fichero = open("registered.txt", "w")
        fichero.write("User \t IP \t Expires \n")
        for key in registro:
            fichero.write(key + " " + registro[key][0] + " ")
            fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(registro[key][2]))
            fichero.write (fecha + "\n")


    def handle(self):

        print "Petición recibida del Cliente: ",
        print "IP:" + str(self.client_address[0]),
        print " Puerto: " + str(self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            line = line.split()
            if line[0] == "REGISTER" and line[2] == "SIP/1.0":
                line[1] = line[1].split(":")
                if line[4] != "0":
                    fecharegistro = time.time()
                    registro[line[1][1]] = [str(self.client_address[0]),line[4], fecharegistro]
                    self.wfile.write(line[2] + "200 OK\r\n\r\n")
                else:
                    self.wfile.write(line[2] + "200 OK\r\n\r\n")
                    if line[1][1] in registro:
                        del registro[line[1][1]]
            self.borrar_caducados(registro)
            self.register2file(registro)

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT ), EchoHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()

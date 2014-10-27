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
    def borrar_caducados(self, registro):
        """
        Borra los usuarios presentes en el registro cuyo fecha
        de caducidad haya llegado
        """
        self.lista_aux = []
        for key in registro:
            if time.time() >= int(registro[key][2]) + int(registro[key][1]):
                self.lista_aux.append(key)
        for key in self.lista_aux:
            del registro[key]

    def register2file(self, registro):
        """
        Imprime en el fichero "registered.txt" el contenido del registro
        de usuarios
        """
        fichero = open("registered.txt", "w")
        fichero.write("User \t IP \t Expires \n")
        for key in registro:
            fichero.write(key + " " + registro[key][0] + " ")
            fecha = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.gmtime(registro[key][2]))
            fichero.write(fecha + "\n")

    def handle(self):
        """
        Recive y procesa todos los mensajes recividos por el servidor del tipo
        REGISTER.

        Introduce en el registro aquellos usuarios cuya petición sea valida y
        borra aquellos que manden una petición con el campo Expires = 0.
        """
        print "Petición recibida del Cliente: ",
        print "IP:" + str(self.client_address[0]),
        print " Puerto: " + str(self.client_address[1])
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente.
            line = self.rfile.read()
            #Si el mensaje esta vacío sale del proceso
            #sin realizar ninguna acción.
            if not line:
                break
            line = line.split()
            # Comprueba si la petición cumple con los requisítos de
            # método ("REGISTER") y de versión
            if line[0] == "REGISTER" and line[2] == "SIP/2.0":
                line[1] = line[1].split(":")
                #Envia el mensaje de que la petición ha llegado correctamente.
                self.wfile.write(line[2] + " 200 OK\r\n\r\n")
                #Comprueba el valor del campo "EXPIRES".
                if line[4] != "0":
                    # Rellena el registro con la información necesaria del
                    # usuario que envia la petición.
                    fecharegistro = time.time()
                    registro[line[1][1]] = [str(self.client_address[0]),
                                            line[4], fecharegistro]
                else:
                    #Ya que el valor de expires es 0, no introduce
                    #al usuario en el registro
                    if line[1][1] in registro:
                        #Si el usuario que envió la petición con expires = 0
                        #estaba en el registro lo borra.
                        del registro[line[1][1]]
            self.borrar_caducados(registro)
            self.register2file(registro)

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", PORT), EchoHandler)
    print "Lanzando servidor UDP de SIP..."
    serv.serve_forever()

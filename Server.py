import socket
from threading import Thread
from tkinter import EXCEPTION
from typing import final

class Server:
    def __init__(self):
        self.HOSTNAME = "127.0.0.1"
        self.PORT = 7
        self.connected = False
        self.STOP_MSG = "DISCONNECT"
        self.SERVER_FULL_MSG = "SERVER_FULL"
        self.CONNECTION_SUCCESFULL_MSG = "CONNECTED"
        self.connectedClientslist = []
        self.MAX_CLIENTS = 3

    def start(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("[SERVER] Binding to: ", (self.HOSTNAME, self.PORT))
            self.s.bind((self.HOSTNAME, self.PORT))
            print("[SERVER] Listening...")
            self.s.listen()
            self.connected = True
            t = Thread(target=self.accept)
            t.start()
        except:
            print("[SERVER] Error when binding!")
    
    def accept(self):
        try:
            while self.connected:
                conn, addr = self.s.accept()
                if len(self.connectedClientslist) == self.MAX_CLIENTS:
                    self.send(conn, addr, self.SERVER_FULL_MSG)
                else:
                    print("[SERVER] ", addr, " connected!")
                    self.connectedClientslist.append((conn,addr))
                    self.send(conn, addr, self.CONNECTION_SUCCESFULL_MSG)
                    t = Thread(target=self.recieve, args=(conn, addr, ))
                    t.start()
        except:
            print("[SERVER] Encountered a problem with server's socket")

    def stop(self):
        if self.connected:
            for conn, addr in self.connectedClientslist:
                self.send(conn, addr, self.STOP_MSG)
                self.connected = False
                self.s.close()
            print("[SERVER] Stopped")
        
        
    def recieve(self, conn, addr):
        try:
            while self.connected:
                data = conn.recv(1024)
                data = data.decode()
                if data == self.STOP_MSG:
                    print("[SERVER] ", addr, " disconnected!")
                    self.connectedClientslist.remove((conn, addr))
                    break
                else:
                    print("[SERVER] ", addr, " says:", data, ". Received bytes: ", len(data))
                    self.send(conn, addr, data)
        except ConnectionResetError:
            print("[SERVER] ", addr, " disconnected!")
        except Exception as e:
            print("Error when recieving data from: ", conn, addr, "   ", e.__class__)
        finally:
            if (conn, addr) in self.connectedClientslist:
                self.connectedClientslist.remove((conn,addr))

    
    def send(self, conn, addr,  data):
            print("[SERVER] Sending data to ", addr)
            conn.send(data.encode())

if __name__ == "__main__":
    server = Server()

    print("[SERVER] Default IP: 127.0.0.1")
    print("[SERVER] Default PORT: 7")
    print("[SERVER] Type 'start' to start server and 'stop' to stop server")
    print("[SERVER] To change IP address or dns hostname type 'ip', to change port type 'port'")
    print("[SERVER] To check how many connectedClientslist connected type 'connectedClientslist'")
    
    while(True):
        string = input()
        if string.lower() == "ip":
            if server.connected:
                print("[SERVER] Can't change IP while connection is up, please stop the connection")
            else:
                server.HOSTNAME = input("Input IP address or hostname: ")
        elif string.lower() == "port":
            if server.connected:
                print("[SERVER] Can't change IP while connection is up, please stop the connection")
            else:
                try:
                    server.PORT = int(input("Input new port: "))
                except:
                    print("[SERVER] Port number must be an integer!")
        elif string.lower() == "start":
            if not server.connected:
                server.start()
            else:
                print("[SERVER] Connection is already up")
        elif string.lower() == "stop":
            if server.connected:
                server.stop()
            else:
                print("[SERVER] Connection is already down")
        elif string.lower() == 'quit':
            if server.connected:
                server.stop()
            exit()
        elif string.lower() == 'connectedClientslist':
            print("[SERVER] Connected connectedClientslist: ", len(server.connectedClientslist))
        else:
            print("[SERVER] Command unknown...")
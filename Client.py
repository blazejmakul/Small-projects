import socket
from threading import Thread

class Client:
    def __init__(self):
        self.HOSTNAME = "127.0.0.1"
        self.PORT = 7
        self.connected = False
        self.stop_msg = "DISCONNECT"

    def connect(self):
        try:
            print("[CLIENT] Connecting to: ", (self.HOSTNAME, self.PORT))
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.HOSTNAME, self.PORT))
            self.connected = True
            t = Thread(target=self.recieve)
            t.start()
        except:
            print("[CLIENT] Server not responding!")
    
    def disconnect(self):
        if self.connected:
            print("[CLIENT] Disconnecting...")
            self.send(self.stop_msg.encode())
            self.connected = False
            self.s.close()
    
    def recieve(self):
        try:
            while self.connected:
                data = self.s.recv(1024)
                data = data.decode()
                if data == "CONNECTED":
                    print("[CLIENT] Connected!")
                elif data == "SERVER_FULL":
                    print("[CLIENT] Failed to connect. Server is full!")
                    self.connected = False
                elif data == self.stop_msg:
                    print("[CLIENT] Server disconnected")
                    self.connected = False
                    break
                else:
                    print("[CLIENT] Server says:", data)
        except ConnectionResetError:
            print("[Client] Server disconnected!")
        except ConnectionAbortedError:
            pass
        except Exception as e:
            print("Error when recieving data: ", e.__class__)
        finally:
            self.connected = False
    
    def send(self, data):
        print("[CLIENT] Sending data to server")
        self.s.send(data.encode())

if __name__ == "__main__":
    client = Client()

    print("[CLIENT] Default IP: 127.0.0.1")
    print("[CLIENT] Default PORT: 7")
    print("[CLIENT] Type 'start' to start connection and 'stop' to stop connection")
    print("[CLIENT] To change IP address or dns hostname type 'ip', to change port type 'port'")

    while(True):
        string = input()
        if string.lower() == "ip":
            if client.connected:
                print("[CLIENT] Can't change IP while connection is up, please stop the connection")
            else:
                client.HOSTNAME = input("[CLIENT] Input IP address or hostname: ")
        elif string.lower() == "port":
            if client.connected:
                print("[CLIENT] Can't change IP while connection is up, please stop the connection")
            else:
                try:
                    client.PORT = int(input("[CLIENT] Input new port: "))
                except:
                    print("[CLIENT] Port number must be an integer!")
        elif string.lower() == "start":
            if not client.connected:
                client.connect()
            else:
                print("[CLIENT] Connection is already up")
        elif string.lower() == "stop":
            if client.connected:
                client.disconnect()
                print("[CLIENT] Connection closed")
            else:
                print("[CLIENT] Connection is already down") 
        elif string.lower() == 'quit':
            if client.connected:
                client.disconnect()
            exit()
        else:
            if client.connected:
                client.send(string)
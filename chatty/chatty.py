import asyncore
import socket

clients = []

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        print(data)
        if data:
            
            # for each connected client
            for i, sock in enumerate(clients):
                try:
                    # send them the response
                    sock.send(data)
                except:
                    print("Socket bad: ", sock)
                    print("Removing clients: {}".format(i))
                    del clients[i]
            
           


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # save their sockets in the clients list
            clients.append(sock)

            print("Incoming connection from {}".format(repr(addr)))
            handler = EchoHandler(sock)

server = EchoServer('localhost', 8080)
asyncore.loop()
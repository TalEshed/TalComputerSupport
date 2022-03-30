import socket
import threading


class Client_communication:
    def __init__(self, server_ip, port, client_q):
        """

        :param server_ip:
        :param server_port:
        :param client_q:
        """
        self.server_ip = server_ip
        self.port = port
        self.client_q = client_q
        self.my_socket = socket.socket()
        self.my_socket = socket.socket()
        # Start the threading - The thread receives messages from the server and insert them to the client_q
        threading.Thread(target=self.recv).start()

    def send_msg(self, msg):
        """
        :param msg: Message to the send to the server
        :return: Sends a message to the server
        """
        if type(msg) == str:
            # The message is string, encode it
            msg = (str(len(msg)).zfill(3) + msg).encode()
        else:
            # The message isn't string need to be encrypted, so encode only the length of the message
            msg = str(len(msg)).zfill(3).encode() + msg
            # send the message
        try:
            self.my_socket.send(msg)
        except:
            # Stop the thread - can't send the message
            self.running = False


    def recv(self):
        """
        :return: Connects to the server, receives messages from the server and inserts them to the client_q
        """
        try:
            # connect to the server
            self.my_socket.connect((self.server_ip, self.port))
            # If the connection succeeded start the threading
            self.running = True
        except:
            # If there was a problem to connect to the server, stop threading
            self.running = False
        # While there is a connection with the server:
        while self.running:
            try:
                #  Receive the length of the data
                data_len = self.my_socket.recv(3).decode()
                # Receive the data from the server
                data = self.my_socket.recv(int(data_len)).decode()
            except:
                # If can't receive from the server, stop threading
                self.running = False
            else:
                # Insert the message to the client_q
                self.client_q.put(data)


    def server_status(self):
        """

        :return: Return the connection status (true - there is connection, false - there is no connection)
        """
        return self.running


    def close_client(self):
        """

        :return:
        """
        self.send_msg("close")
        self.my_socket.close()

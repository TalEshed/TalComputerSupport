import threading
import socket
import select
import screen_shot_funcs

class Server_communication:
    def __init__(self, port, server_q):
        """

        :param port:
        :param server_q:
        """
        self.port = port
        self.server_q = server_q
        self.server_socket = socket.socket()
        self.open_clients = {}
        self.running = True
        # Start the threading - receives messages from the server and insert them to the server_q
        threading.Thread(target=self.recv).start()

    def close_client(self, client_socket):
        """

        :param client_socket:
        :return:
        """
        if client_socket in self.open_clients.keys():
            del self.open_clients[client_socket]
            client_socket.close()


    def send_msg(self, ip, msg):
        """
        the function sends a message to the server
        :param msg: message to the send to the server
        :return: None
        """
        # create message
        msg = (str(len(msg)).zfill(3) + msg).encode()
        # send the message
        for client in self.open_clients.keys():
            if self.open_clients[client] == ip:
                try:
                    client.send(msg)
                except:
                    # if can't send the message, stop the thread
                    self.close_client(client)


    def recv(self):
        """

        :return: Connects to the server and receives messages from clients and inserts them to server_q
        """
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(4)
        while self.running:
            rlist, wlist, xlist = select.select(list(self.open_clients.keys()) + [self.server_socket], list(self.open_clients.keys()), [], 0.3)
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    client, address = self.server_socket.accept()
                    print(f'{address[0]} - connected')
                    self.open_clients[client] = address[0]
                    # The IP of the client to shara with him the screen
                    self.server_q.put([address[0], 'The IP that connected'])
                else:
                    try:
                        # Receive the length of the data
                        data_len = current_socket.recv(3).decode()
                        # Receive the data from the server
                        data = current_socket.recv(int(data_len)).decode()
                    except Exception as e:
                        # If can't receive from the client, close the socket with this client
                        print("1",str(e))
                        self.close_client(current_socket)
                    else:
                        if data == "" or data == "close":
                            self.close_client(current_socket)
                        # Check that the client want to screen sharing
                        elif data == "ok":
                            # start screen sharing
                            threading.Thread(target=self.share_screen, args=(current_socket,)).start()
                        else:
                            # Insert the message to the server_q
                            self.server_q.put([self.open_clients[current_socket], data])


    def close_server(self):
        """

        :return:
        """
        # Sockets of the clients
        clients = list(self.open_clients.keys())
        for client in clients:
            try:
                client.close()
            except:
                pass
        self.running = False
        self.open_clients.clear()
        self.server_socket.close()


    def send_image(self, image, coordinates):
        """

        :param image: Image to send the client
        :param coordinates: Coordinates of the start difference box
        :return: Build message by protocol and return the message (The image and its parameters)
        """
        # Get the size of the image in bytes
        size = image.size
        send = image.tobytes()
        # The X, Y positions that the difference box starts
        x, y = str(coordinates[0]).zfill(4).encode(), str(coordinates[1]).zfill(4).encode()
        # Create the image massage
        send = (str(size[0]).zfill(4) + str(size[1]).zfill(4)).encode() + x + y + str(len(send)).zfill(20).encode() + send
        return send


    def share_screen(self, client):
        """

        :param client: The client to share with him the screen
        :return: While the flag True - keep sharing the screen
        """
        # Takes the first screen shot
        img1 = screen_shot_funcs.image_screen_shot()
        # Build the image message by protocol
        send = self.send_image(img1, (0, 0))
        try:
            # Send the first image to the client
            client.sendall(send)
        except Exception as e:
            print(e)
        # keep sharing screen
        while True:

            # Take screen shot
            img2 = screen_shot_funcs.image_screen_shot()
            # Get the coordinates - the start, end of the difference box between image one to image two
            coordinates = screen_shot_funcs.equal(img1, img2)
            # --- If there is difference between the images ---
            if coordinates != None:
                # Cut the difference box between image one to image two
                cut = img2.crop(coordinates)
                # Build the image message by protocol
                send = self.send_image(cut, coordinates[:2])
                try:
                    # Send image to the client
                    client.sendall(send)
                except Exception as e:
                    print(e)

                # Paste all image 2 on image 1
                img1 = img2
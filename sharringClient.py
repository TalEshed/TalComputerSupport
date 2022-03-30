import socket
import pygame
import pyautogui
from pygame.locals import *
import queue
import select
import threading

class Comm:
    def __init__(self, q):

        self.q = q
        self.socket = socket.socket()
        self.running = True
        pygame.init()
        # The width, height of the full screen
        width, height = pyautogui.size()
        # Open pygame window in the size of the whole screen
        self.screen = pygame.display.set_mode((width, height))
        # Set caption of the screen
        pygame.display.set_caption('screen sharing')
        self.recv()

    def recv_image(self, pic_len):
        '''
        :param my_socket: The socket that connects with the server
        :param pic_len: The length of the picture
        :return: The image from the server as a byte array
        '''
        # the variable that will save the image as a byte array
        file_data = bytearray()
        while len(file_data) < pic_len:
            # put in size the amount of the bytes that has not copied from the image yet
            size = pic_len - len(file_data)
            # try to receive 1024 bytes from the image each time
            try:
                if size > 2048:
                    # if there are 2048 bytes or more that has not copied from the image, copy 1024 bytes
                    file_data.extend(self.socket.recv(2048))
                else:
                    # if there are less than 1024 bytes that has not copied, copy the rest
                    file_data.extend(self.socket.recv(size))
            except Exception as e:
                print(str(e))
                # if there is a problem to receive the image, close the socket
                self.socket.close()
                file_data = None
                break
        return file_data


    def recv(self):
        # --- Connection to the server ---
        self.socket = socket.socket()
        self.socket.connect(("192.168.4.95", 2024))

        data = ""
        try:
            data_len = int(self.socket.recv(3).decode())
            data = self.socket.recv(data_len).decode()
        except Exception as e:
            print(e)
        print(data)
        if data == "start sending":  # ""sending image":
            # Send "ok" to start the sharing

            try:
                self.socket.send((str(len("ok")).zfill(3) + "ok").encode())
            except Exception as e:
                print(e)
        while self.running:
            self.check_events()
            rlist , wlist , xlist = select.select([self.socket], [], [], 0.1)
            if rlist != []:
                try:
                    # Receive the width of the image
                    width_image = int(self.socket.recv(4).decode())
                    # Receive the height of the image
                    height_image = int(self.socket.recv(4).decode())
                    # Receive the coordinates of the image
                    coordinates = (int(self.socket.recv(4).decode()), int(self.socket.recv(4).decode()))
                    # Receive the length (by bytes) of the image
                    len_image = int(self.socket.recv(20).decode())
                    # Receive the image of the screen from the server
                    image = self.recv_image(len_image)
                except Exception as e:
                    print(e)

                else:
                    if self.running:
                        img = pygame.image.frombuffer(image, (width_image, height_image), "RGB")
                        self.screen.blit(img, coordinates)
                        pygame.display.update()


    def check_events(self):
        """

        :return: Check if the client close the pygame window
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.running = False



def handle_msgs(q):
    while True:
        data = msg_q.get()
        print(data)


if __name__ == '__main__':

    msg_q = queue.Queue()
    threading.Thread(target=handle_msgs, args=(msg_q,)).start()
    client = Comm(msg_q)





import socket
import zlib
import pygame
import pyautogui
from pygame.locals import *


import queue

img_q = queue.Queue()

def recv_image(my_socket, pic_len):
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
                file_data.extend(my_socket.recv(2048))
            else:
                # if there are less than 1024 bytes that has not copied, copy the rest
                file_data.extend(my_socket.recv(size))
        except Exception as e:
            print(str(e))
            # if there is a problem to receive the image, close the socket
            my_socket.close()
            file_data = None
            break
    return file_data



def check_events():
    """

    :return: Check if the client close the pygame window
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()



# --- Connection to the server ---
my_socket = socket.socket()
my_socket.connect(("192.168.4.95", 2024))

# --- Check start sharing with the server ---
try:
    data_len = int(my_socket.recv(3).decode())
    data = my_socket.recv(data_len).decode()
except Exception as e:
    print(e)


if data == "start sending": #""sending image":
    # Send "ok" to start the sharing
    try:
        my_socket.send((str(len("ok")).zfill(3) + "ok").encode())
    except Exception as e:
        print(e)

    # Initialize pygame
    pygame.init()
    # The width, height of the full screen
    width, height = pyautogui.size()
    # Open pygame window in the size of the whole screen
    screen = pygame.display.set_mode((width, height))
    # Set caption of the screen
    pygame.display.set_caption('screen sharing')

    count=0

    while True:
        # Check if the client close the pygame window
        check_events()
        try:
            # Receive the width of the image
            width_image = int(my_socket.recv(4).decode())
            # Receive the height of the image
            height_image = int(my_socket.recv(4).decode())
            # Receive the coordinates of the image
            coordinates = (int(my_socket.recv(4).decode()), int(my_socket.recv(4).decode()))
            # Receive the length (by bytes) of the image
            len_image = int(my_socket.recv(20).decode())
            # Receive the image of the screen from the server
            print("before recv")
            image = recv_image(my_socket, len_image)
            print("after recv......")
        except Exception as e:
            print(e)

        else:
            img_q.put((width_image, height_image, coordinates, image))





        if not img_q.empty():
            width_image, height_image, coordinates, image = img_q.get()
            img = pygame.image.frombuffer(image, (width_image, height_image), "RGB")
            screen.blit(img, coordinates)
            pygame.display.update()

        # print("shooting....", count)
        # count+=1
        #
        # # Match the image by size and color
        # img = pygame.image.frombuffer(image, (width_image, height_image), "RGB")
        # # Put the image on the screen
        # screen.blit(img, coordinates)
        # # Update the screen
        # pygame.display.update()








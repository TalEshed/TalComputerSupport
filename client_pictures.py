import client_object
import pygame
import pyautogui
from pygame.locals import *
import setting
import queue
import screen_shot_funcs
import threading


# def recv_from_server():
#     while True:
#         data = client3_q.get()
#         print("\n", data)


# # Initialize pygame
# pygame.init()
# # The width, height of the full screen
# width, height = pyautogui.size()
# # Open pygame window in the size of the whole screen
# screen = pygame.display.set_mode((width, height))
# # Set caption of the screen
# pygame.display.set_caption('screen sharing')

q = queue.Queue()
client3 = client_object.Client_communication(setting.SERVER_IP, setting.SCREEN_PORT, q)


# Initialize pygame
pygame.init()
# The width, height of the full screen
width, height = pyautogui.size()
# Open pygame window in the size of the whole screen
screen = pygame.display.set_mode((width, height))
# Set caption of the screen
pygame.display.set_caption('screen sharing')

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    if not q.empty():
        width_image, height_image, coordinates, image = q.get()
        img = pygame.image.frombuffer(image, (width_image, height_image), "RGB")
        screen.blit(img, coordinates)
        pygame.display.update()






#
# client3.close_client()
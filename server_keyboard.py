import server_object
import keyboard_object
import queue

server_q = queue.Queue()
ser_keyboard = server_object.Server_communication(2023, server_q)
# clear the queue
server_q.get()

while ser_keyboard.running:
    ip, data = server_q.get()
    keyboard_object.keyboard_press(data)

ser_keyboard.close_server()
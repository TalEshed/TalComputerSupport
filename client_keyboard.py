import client_object
import queue
import threading
import keyboard_object



def recv_from_server():
    while True:
        data = client2_q.get()
        print("\n",data)


client2_q = queue.Queue()
client2 = client_object.Client_communication("192.168.4.95", 2023, client2_q)
threading.Thread(target=recv_from_server).start()

keyboard_q = queue.Queue()
keyboard_func = keyboard_object.Keyboard(keyboard_q)
keyboard_func.keyboard_log()

while True:
    event = keyboard_func.keyboard_par()
    client2.send_msg(event)
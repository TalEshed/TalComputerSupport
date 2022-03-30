import client_object
import queue
import threading
import mouse_object



def recv_from_server():
    while True:
        data = client1_q.get()
        print("\n",data)


client1_q = queue.Queue()
client1 = client_object.Client_communication("192.168.4.95", 2022, client1_q)
threading.Thread(target=recv_from_server).start()

mouse_q = queue.Queue()
mouse_func = mouse_object.Mouse(mouse_q)
mouse_func.listener_button_click()

while True:
    event = mouse_func.mouse_click_par()
    x_y_click = str(event[0]).zfill(5) + str(event[1]).zfill(5) + event[2]
    client1.send_msg(x_y_click)
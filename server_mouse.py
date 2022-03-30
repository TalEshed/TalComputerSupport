import server_object
import mouse_object
import queue

server_q = queue.Queue()
ser_mouse = server_object.Server_communication(2022, server_q)
# clear the queue
server_q.get()

while ser_mouse.running:
    ip, data = server_q.get()
    x = (data[:5]).lstrip('0')
    y = (data[5:10]).lstrip('0')
    click = data[10:]
    if x and y != '':
        mouse_object.mouse_click(int(x), int(y), click)

ser_mouse.close_server()

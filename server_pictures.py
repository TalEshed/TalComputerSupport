import server_object
import queue
import threading

def recv_from_client():
    while True:
        data = server_q.get()
        print("\n",data)

server_q = queue.Queue()
ser_pictures = server_object.Server_communication(2024, server_q)
# the IP of the client to shara with him the screen
IP, data = server_q.get()
print(IP, data)
threading.Thread(target=recv_from_client).start()
ser_pictures.send_msg(IP, 'start sending')

while ser_pictures.running:
   pass

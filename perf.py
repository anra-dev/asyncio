import socket
import time
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

n = 0

def monitor():
    global n
    while True:
        time.sleep(1)
        print(f"{n} reqs/sec")
        n = 0


Thread(target=monitor).start()

while True:
    client_socket.send(b'1\n')
    resp = client_socket.recv(4000)
    n += 1

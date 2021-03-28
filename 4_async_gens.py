import socket
from select import select

tasks = []
wait_to_read = {}
wait_to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:

        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()  # read

        print('Connection from', addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4000)  # read

        if not request:
            break
        else:
            response = 'Hello world!\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)  # write

    client_socket.close()


def event_loop():
    while any([tasks, wait_to_read, wait_to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(wait_to_read, wait_to_write, [])

            for sock in ready_to_read:
                tasks.append(wait_to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(wait_to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)
            if reason == 'read':
                wait_to_read[sock] = task
            if reason == 'write':
                wait_to_write[sock] = task

        except:
            print('Done!')


tasks.append(server())
event_loop()

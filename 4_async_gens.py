import socket
import time
from select import select

tasks = []
wait_to_read = {}
wait_to_write = {}


def decorator(fn):
    def iner(*args):
        time.sleep(2)
        fn(*args)
        fn()
    return iner
print = decorator(print)


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        print('Заходим в цикл сервера')
        print('Возвращаем серверный сокет: ', server_socket)
        yield 'read', server_socket
        print('Получаем ответ от клиента')
        client_socket, addr = server_socket.accept()  # read
        print('Connection from', addr)
        tasks.append(client(client_socket))
        print('Заносим сокет клиента в очередь заданий tasks:', tasks)


def client(client_socket):
    while True:
        print('Заходим в цикл клиента')
        print('Возвращаем клиентский сокет для чтения: ', client_socket)
        yield 'read', client_socket
        request = client_socket.recv(4000)  # read
        print('Получен ответ от клиента :', request)

        print('Подготовили ответ для клиента')
        if not request:
            break
        else:
            response = 'Hello world!\n'.encode()
            print('Возвращаем клиентский сокет для записи: ', client_socket)
            yield 'write', client_socket
            print('Отправляем ответ клиенту: ', response)
            client_socket.send(response)  # write
    print('Закрываем клиентский сокет')
    client_socket.close()


def event_loop():
    while any([tasks, wait_to_read, wait_to_write]):
        print('Заходим в основной цикл event_loop')
        print('Данные на входе: tasks - ', tasks)
        print('Данные на входе: wait_to_read - ', wait_to_read)
        print('Данные на входе: wait_to_write - ', wait_to_write)
        while not tasks:
            print('Заходим во вложенный цикл event_loop')
            print('Ожидаем данные от select')
            ready_to_read, ready_to_write, _ = select(wait_to_read, wait_to_write, [])

            for sock in ready_to_read:
                print('Получили от селект сокет готовый для чтения: ', sock)
                tasks.append(wait_to_read.pop(sock))
                print('Добавили его в очередь заданий: ', tasks)

            for sock in ready_to_write:
                print('Получили от селект сокет готовый для записи: ', sock)
                tasks.append(wait_to_write.pop(sock))
                print('Добавили его в очередь заданий: ', tasks)

        try:
            print('Заходим в блок try')
            print('Данные на входе: tasks - ', tasks)
            print('Данные на входе: wait_to_read - ', wait_to_read)
            print('Данные на входе: wait_to_write - ', wait_to_write)
            task = tasks.pop(0)
            print('Забираем задание сверху списка: ', task)
            reason, sock = next(task)
            print(f'Активируем генератор на один цикл и получаем из него данные : тип - {reason} и сокет - {sock}')

            if reason == 'read':
                wait_to_read[sock] = task
                print('Добавляем задание в очередь wait_to_read: ', wait_to_read)
            if reason == 'write':
                wait_to_write[sock] = task
                print('Добавляем задание в очередь wait_to_read: ', wait_to_read)

        except BaseException as ex:
            print('Done!', ex)
            print(tasks, wait_to_read, wait_to_write)


tasks.append(server())
event_loop()

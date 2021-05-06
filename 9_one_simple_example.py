from time import sleep

queue = []

def counter():
    count = 0
    while True:
        print(count)
        count += 1
        yield


def printer():
    count = 0
    while True:
        if count % 3 == 0:
            print('Bang!!!')
        count += 1
        yield


def main():
    while True:
        gen = queue.pop(0)
        next(gen)
        queue.append(gen)
        sleep(0.3)


if __name__ == '__main__':
    gen1 = counter()
    queue.append(gen1)
    gen2 = printer()
    queue.append(gen2)
    main()
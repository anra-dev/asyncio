from time import time


def gen(s):
    for i in s:
        yield i


def gen_filename():
    while True:
        pattern = 'file-{}.jpg'
        t = int(time() * 1000)
        yield pattern.format(t)


def gen1(n):
    for i in range(n):
        yield i


def gen2(s):
    for i in s:
        yield i


g1 = gen1(8)
g2 = gen2('roma')

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)
    try:
        s = next(task)
        print(s)
        tasks.append(task)
    except StopIteration:
        pass


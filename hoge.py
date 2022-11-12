from multiprocessing import Process, Lock
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(l,num):
    l.acquire()
    try:
        a = 0
        for i in range(100000):
            a += (num+num)/num/5
        print(a)
    finally:
        l.release()

def g(num):
    b = num*num
    print(b)

if __name__ == '__main__':
    lock = Lock()
    info('main line')
    #parent_conn,child_conn = Pipe()
    for num in range(1,11):
        p1 = Process(target=f, args=(lock,num,))
        p1.start()
        p1.join()
    p2 = Process(target=g, args=(2,))
    p2.start()
    p2.join()
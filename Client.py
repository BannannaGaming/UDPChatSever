import socket
import threading
import time

thread_lock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            thread_lock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print (str(data))
        except:
            pass
        finally:
            thread_lock.release()

server = ('127.0.0.1', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(0)

recive_Thread = threading.Thread(target=receving, args=("RecvThread", s))
recive_Thread.start()

alias = raw_input('Name: ')
message = raw_input(alias + '->')
while message != 'q':
    if message != '':
        s.sendto(alias + ': ' + message, server)
    thread_lock.acquire()
    message = raw_input(alias + '->')
    thread_lock.release()
    time.sleep(0.2)

shutdown = True
recive_Thread.join()
s.close()

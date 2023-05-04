import socket
import threading

def thread_function(c,addr):
    # while True:
    print(f"{addr}::{str(c.recv(1024).decode())}")
    print(f"New: {str(c.recv(1024).decode())}")
    c.close()


s = socket.socket()
print("Socket created")

s.bind((socket.gethostbyname(socket.gethostname()),8000))
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
s.listen(1)

print("Waiting for connection")

while True:
    c,addr = s.accept()
    print("Connection made with ",addr)
    c.send(bytes("Hello connected with me","utf-8"))
    # print(str(c.recv(1024).decode()))
    threading._start_new_thread(thread_function,(c,addr))

s.close()
    
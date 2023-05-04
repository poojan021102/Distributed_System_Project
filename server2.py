import socket
import threading
import Pyro4

def check_fault(c,addr):
    c = Pyro4.Proxy("PYRO:obj_3a4e94dfd4fc4e12bdcbd22a09a68858@192.168.31.233:59356")  
    print(c.Factorial(5))


ip = []
port = []
s = socket.socket()

print("Socket created")
s.bind((socket.gethostbyname(socket.gethostname()),8000))
print(f"IP: {socket.gethostbyname(socket.gethostname())}\nPORT: 8000")
s.listen(1)
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
n = int(input("Enter the number of slaves: "))
for i in range(n):
    h = input("IP: ")
    ip.append(h)
    p = input("PORT: ")
    port.append(p)

while True:
    c,addr = s.accept()
    print("Connection made with ",addr)
    # multiprocessing.Process(target=check_fault).start()
    threading._start_new_thread(check_fault,(c,addr))
    # print(str(c.recv(1024).decode()))

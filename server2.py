import socket
import threading
import Pyro4

def check_fault(c,addr):
    for n in name:
        print(n)
        try:
            slave = Pyro4.Proxy(n)
            print(slave.Factorial(5))
            break
        except Exception:
            print("Error")
    c.close()
            

name = []
s = socket.socket()

print("Socket created")
s.bind((socket.gethostbyname(socket.gethostname()),8000))
print(f"IP: {socket.gethostbyname(socket.gethostname())}\nPORT: 8000")
s.listen(1)
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
n = int(input("Enter the number of slaves: "))
for i in range(n):
    h = input("NAME: ")
    name.append("PYRONAME:" + h)
print("Ready for connection...")
while True:
    c,addr = s.accept()
    print("Connection made with ",addr)
    # multiprocessing.Process(target=check_fault).start()
    threading._start_new_thread(check_fault,(c,addr))
    # print(str(c.recv(1024).decode()))

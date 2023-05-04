import socket
import threading
import Pyro4

def thread_function(c):
    for n in name:
        print(n)
        try:
            slave = Pyro4.Proxy(n)
            print(slave.Factorial(5))
            break
        except Exception as e:
            print(e)
    c.close()
    pass



s = socket.socket()
print("Socket created")



name = []
n = int(input("Enter the number of slaves: "))
for i in range(n):
    h = input("Name:")
    name.append(h)




s.bind((socket.gethostbyname(socket.gethostname()),8000))
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
s.listen(1)

print("Waiting for connection")

while True:
    c,addr = s.accept()
    print("Connection made with ",addr)
    # print(str(c.recv(1024).decode()))
    threading._start_new_thread(thread_function,(c,))

s.close()
    
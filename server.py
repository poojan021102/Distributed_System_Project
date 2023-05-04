import socket

s = socket.socket()
print("Socket created")

s.bind((socket.gethostbyname(socket.gethostname()),8000))
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
s.listen(3)

print("Waiting for connection")

while True:
    c,addr = s.accept()
    print("Connection made with ",addr)
    c.send(bytes("Hello connected with me","utf-8"))
    print(str(c.recv(1024).decode()))
    
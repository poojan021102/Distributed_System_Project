# importing library for socket programming
import socket
import time
import psutil

IP_ADD = '192.168.31.57'
PORT = 8000


def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# method to create socket
try:
    # default parameters of socket
    # socket.AF_INET: It refers to the address-family ipv4.
    # socket.SOCK_STREAM: It refers to connection-oriented TCP protocol.
    c=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error:",e)

# methot to connect client with server
try:
    # paremeters 
    # IP Address: IP address of  the server.
    # Port Number: Port Number on which we have to connect.
    c.connect((IP_ADD,PORT))
except socket.error as e:
    print("Error:",e)
    
print(c.recv(1024).decode())
msg=psutil.sensors_battery()
msg1=convertTime(msg.secsleft)
msg2=msg.percent
msg3=msg.power_plugged
c.send(bytes(str(str(msg1)+" "+str(msg2)+" "+str(msg3)),'utf-8'))
time.sleep(15)
c.send(bytes("close",'utf-8'))

# Pyro enables code to call methods on objects even if that object is running on a remote machine
import Pyro4
import psutil
import socket

def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

# Exposing classes, methods and properties is done using the @Pyro4.expose decorator
@Pyro4.expose
class Calculator(object):
    # This is a normal Python object but it is registered with Pyro so that you can access it remotely. 
    # Pyro objects are written just as any other object but the fact that Pyro knows something about them makes them special, 
    # in the way that you can call methods on them from other programs. A class can also be a Pyro object, 
    # but then you will also have to tell Pyro about how it should create actual objects from that class when handling remote calls.

    def getStatus(self):
        msg=psutil.sensors_battery()
        msg1=convertTime(msg.secsleft)
        msg2=msg.percent
        msg3=msg.power_plugged
        msg4=str(str(msg1)+" "+str(msg2)+" "+str(msg3))
        return msg4
    
    def getMap(self, words):
        dic={}
        for i in words:
            if i in dic:
                dic[i.lower()]+=1
            else:
                dic[i.lower()]=1
        st = ""
        for key, val in dic.items():
            st=st+str(str(key)+":"+str(val))+" "
        return st

    def matmul(self, a, b):
        result = [0] * len(b[0])
        for i in range(len(a)):
            for k in range(len(b[0])):
                result[k] += a[i] * b[i][k]
        str1 = ""
        for i in range(len(result)):
            str1 += str(result[i])
            if i != len(result) - 1:
                str1 += " "
        return str1

    # implementation of division method
    def Division(self, a, b):
        if b==0:
            return "Denominator can not be zero !"
        else:
            return "{0} / {1} = {2}".format(a, b, a/b)

    # implementation of modulo method
    def Modulo(self, a, b):
        if b==0:
            return "Denominator can not be zero !"
        else:
            return "{0} mod {1} = {2}".format(a, b, a%b)

    # implementation of power method
    def Power(self, a, b):
        return "{0} * {1} = {2}".format(a, b, a*b)

    # implementation of factorial method
    def Factorial(self, a):
        if a==0 or a==1:
            return "{0}! = {1}".format(a, 1)
        pro = 1
        for i in range(2,a+1,1):
            pro = pro * i
        return "{0}! = {1}".format(a, pro)

# This is the part of Pyro that listens for remote method calls, dispatches them to the appropriate actual objects, 
# and returns the results to the caller. All Pyro objects are registered in one or more daemons.
daemon = Pyro4.Daemon.serveSimple({
        Calculator:'slave1'
    },
    host=socket.gethostbyname(socket.gethostname()),
    ns=True
)   

# The name server is a utility that provides a phone book for Pyro applications: you use it to look up a “number” by a “name”. 
# The name in Pyro’s case is the logical name of a remote object. The number is the exact location where Pyro can contact the object. 
# Usually there is just one name server running in your network.
# ns = Pyro4.locateNS()   

# For enabling the client to properly locate the server, it needs to  be named  
# and registered  with  the localhost, similar to registering with 
# the RMI registry in Java. It is done by using the following instructions: 

print(daemon)

print("Calculator is on service now")
# Usually you run the daemon’s to handle incoming requests.
# to combine several daemons into one, so that you only have to call the requestLoop of that “master daemon”. 
# Basically Pyro will run an integrated multiplexed event loop for you. You can combine normal Daemon objects, 
# the NameServerDaemon and also the name server’s BroadcastServer.
daemon.requestLoop()
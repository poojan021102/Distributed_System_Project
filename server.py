import socket
import Pyro4
import multiprocessing

def get_all_words(w):
    w1 = w.split("\n")
    ans = []
    for lines in w1:
        l = lines.split()
        for l1 in l:
            a = l1.split('?')
            for a1 in a:
                b = a1.split('!')
                for b1 in b:
                    c = b1.split('|')
                    for c1 in c:
                        d = c1.split(';')
                        for d1 in d:
                            ans.append(d1)
    return ans



def send_for_word_count(slave,l,queue):
    ans = slave.getMap(l)
    queue.put(ans)



def user_function(c,name):
    # w = c.recv()
    w = "This is this a\nmulti-line?spaces!text\nwith with;spaces."
    words = get_all_words(w)
    n = len(name)
    each_words_count = int(len(words)/n)
    st = 0
    i = 0
    en = 0
    queue = multiprocessing.Queue()
    processes = []
    while en < len(words):
        try:
            print(name[i])
            slave = Pyro4.Proxy(name[i])
            print(f"Slave {i}: {slave.getStatus()}")
            i = ((i + 1)%len(name))
            if each_words_count == 0:
                en = min(en + 1,len(words))
            else:
                en = min(st + each_words_count - 1, len(words))
            if en >= len(words):break
            l = []
            # print(words)
            # print(st)
            # print(en)
            j = st
            st = en + 1
            while j <= en:
                # print(j)
                l.append(words[j])
                j = j + 1
            p = multiprocessing.Process(target=send_for_word_count, args=(slave,l,queue))
            p.start()
            processes.append(p)
        except Exception as e:
            print("error")
            break
    
    for p in processes:
        p.join()
    
    d = {}
    while not queue.empty():
        s = queue.get()
        print(s)
        u = s.split(" ")
        for y in u:
            t = y.split(":")
            if len(t) == 1:
                break
            
            d[t[0]]=d.get(t[0],0) + int(t[1])
    for k in d.keys():
        print(f"{k}: {d[k]}")
    c.close()


if __name__ == "__main__":
    s = socket.socket()
    print("Socket created")

    name = []

    n = int(input("Enter the number of slaves: "))
    for i in range(n):
        h = input(f"URI {i+1}:")
        name.append(h)


    s.bind((socket.gethostbyname(socket.gethostname()),8000))
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    s.listen(1)

    print("Waiting for connection")

    while True:
        c,addr = s.accept()
        print("Connection made with ",addr)
        # print(str(c.recv(1024).decode()))
        # threading._start_new_thread(thread_function,(c,))
        multiprocessing.Process(target=user_function, args=(c,name)).start()

    s.close()
        
from __future__ import print_function
import socket
import Pyro4
import multiprocessing
import re
import os
import pickle
import os.path
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
def get_all_words(w):
    words = []
    delimiters = ", !.?;"
    for line in w.split('\n'):
        words.extend(re.split(f"[{re.escape(delimiters)}]", line))
    words.remove('')
    l = []
    for a in words:
        if a != '':
            l.append(a)
    return l

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service


    
def FileDownload(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False

    try:
        while not done:
            done = downloader.next_chunk()

        fh.seek(0)
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)

        print("File Downloaded")
        return True
    except:
        print("Something went wrong.")
        return False



def send_for_word_count(slave,l,queue):
    ans = slave.getMap(l)
    queue.put(ans)

def goInfinite(c,name):
    while True:
        op = c.recv(1024).decode()
        if op == "1":
            WordCountFunction(c,name)
        else:
            MatrixMultiplicationFunction(c,name)

def WordCountFunction(c,name):
    service = get_gdrive_service()
    allSlaves = []
    ns = Pyro4.locateNS('192.168.29.58')
    for n in name:
        try:
            uri = ns.lookup(n)
            try:
                s = Pyro4.Proxy(uri)
                print(f"{n}: {s.getStatus()}")
                allSlaves.append(s)
            except Exception as e:
                continue
        except Exception as e:
            print(e)
            continue
    id = str(c.recv(1024).decode())
    # print(allSlaves)
    FileDownload(service, id, f"{id}.txt") 
    f = open(f"{id}.txt",encoding='utf8')
    w = ""
    for line in f:
        w = w + line
    f.close()
    os.remove(f"{id}.txt")
    words = get_all_words(w)
    n = len(name)
    each_words_count = int(len(words)/n)
    st = 0
    i = 0
    queue = multiprocessing.Queue()
    processes = []
    while st < len(words):
        try:
            slave = allSlaves[i]
            if each_words_count == 0:
                en = st
            else:
                en = min(st + each_words_count - 1, len(words)-1)
            if en >= len(words):break
            l = []
            j = st
            st = en + 1
            while j <= en:
                l.append(words[j])
                j = j + 1
            p = multiprocessing.Process(target=send_for_word_count, args=(slave,l,queue))
            p.start()
            processes.append(p)
        except Exception as e:
            print(f"Slave {i+1}:error")
        
        i = ((i + 1)%len(allSlaves))

    for p in processes:
        p.join()
    
    d = {}
    while not queue.empty():
        s = queue.get()
        u = s.split(" ")
        for y in u:
            t = y.split(":")
            if len(t) == 1:
                break 
            d[t[0]]=d.get(t[0],0) + int(t[1])
    s = ""
    for k in d.keys():
        print(f"{k}: {d[k]}")
        s = s + k + ":" + str(d[k]) + " "
    c.send(bytes(s,'utf-8'))

def send_for_matrix(slave,i,m1,matrix,queue):
    ans = slave.matmul(m1,matrix)
    l = ans.split(" ")
    l1 = [i]
    for h in l:
        l1.append(int(h))
    queue.put(l1)


def MatrixMultiplicationFunction(c,name):
    matrix = b''
    allSlaves = []
    matrix += c.recv(1024)
    ns = Pyro4.locateNS('192.168.29.58')
    for n in name:
        try:
            uri = ns.lookup(n)
            try:
                s = Pyro4.Proxy(uri)
                print(f"{n}: {s.getStatus()}")
                allSlaves.append(s)
            except Exception as e:
                continue
        except Exception as e:
            print(e)
            continue
    matrix = pickle.loads(matrix)
    queue = multiprocessing.Queue()
    c.send(bytes("ack",'utf-8'))
    matrix1 = b''
    matrix1 += c.recv(1024)
    matrix1 = pickle.loads(matrix1)
    process = []
    n = 0
    i = 0
    while True:
        if i == len(matrix):
            break
        try:
            slave = allSlaves[n]
            print(f"Connected with Slave {n + 1}: {slave.getStatus()}")
            p = multiprocessing.Process(target=send_for_matrix, args=(slave,i,matrix[i],matrix1,queue))
            p.start()
            process.append(p)
            i = i + 1
        except Exception as e:
            print(f"Error while connecting Slave {n + 1}")
            pass
        n = (n + 1)%len(allSlaves)
    
    for p in process:
        p.join()
    ans = [[0]*len(matrix1[0])]*len(matrix)
    while not queue.empty():
        l = queue.get()
        l1=[]
        for i in range(1,len(l)):
            l1.append(l[i])
        ans[l[0]] = l1
    print(ans)
    msg=pickle.dumps(ans)
    c.send(msg)


if __name__ == "__main__":
    s = socket.socket()
    print("Socket created")

    name = ["slave1","slave2","slave3"]

    s.bind((socket.gethostbyname(socket.gethostname()),8000))
    print(f"IP: {socket.gethostbyname(socket.gethostname())}")
    s.listen(1)

    print("Waiting for connection")

    while True:
        c,addr = s.accept()
        print("Connection made with ",addr)
        multiprocessing.Process(target = goInfinite,args=(c,name)).start()

    s.close()
        
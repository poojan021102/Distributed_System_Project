# importing library for socket programming
import socket
import time
# import the required libraries
# from __future__ import print_function
import pickle
import os.path
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
# import psutil

IP_ADD = '192.168.29.62'
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
    


# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_gdrive_service():
    
    # Variable self.creds will
    # store the user access token.
    # If no valid token found
    # we will create one.
    creds = None

    # The file token.pickle stores the
    # user's access and refresh tokens. It is
    # created automatically when the authorization
    # flow completes for the first time.

    # Check if file token.pickle exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and
        # store it in the variable self.creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available,
    # request the user to log in.
    if not creds or not creds.valid:

        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the access token in token.pickle
        # file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)
    return service

def FileUpload(service, filepath):
    
    # Extract the file name out of the file path
    name = filepath.split('/')[-1]
    
    # Find the MimeType of the file
    mimetype = MimeTypes().guess_type(name)[0]
    
    # create file metadata
    file_metadata = {'name': name, "parents": ["19OaUa4opOlfYxHiEeDvQSrcTd9kXwwYJ"]}

    try:
        media = MediaFileUpload(filepath, mimetype=mimetype)
        
        # Create a new file in the Drive storage
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        print("File Uploaded.")
        return file.get("id")
    
    except Exception as e:
        # if file is not uploaded.
        print("Can't Upload File.")
        print(e)
        return ""
    
while True:
    inp = int(input("Enter choice: "))
    if inp == 1:
        c.send(bytes('1',"utf-8"))
        service = get_gdrive_service()
        f_path = input("Enter full file path: ")
        name = f_path.split('/')[-1]
        id = FileUpload(service,f_path)
        c.send(bytes(id,'utf-8'))
        ans = c.recv(4096).decode()
        print(ans)
        ans = ans.split(" ")
        for y in ans:
            if ":" not in y:
                t = y.split(":")
                if len(t) == 2:
                    print(f"{t[0]}: {t[1]}")
    else:
        c.send(bytes('2','utf-8'))
        n = int(input("Enter the number of rows:"))
        m = int(input("Enter the number of columns:"))
        
        # Initialize matrix
        matrix = []
        print("Enter the entries rowwise:")
        
        # For user input
        for i in range(n):          # A for loop for row entries
            a =[]
            for j in range(m):      # A for loop for column entries
                a.append(int(input()))
            matrix.append(a)
        print(matrix)

        n1 = int(input("Enter the number of rows:"))
        m1 = int(input("Enter the number of columns:"))
        
        # Initialize matrix
        matrix2 = []
        print("Enter the entries rowwise:")
        
        # For user input
        for i in range(n1):          # A for loop for row entries
            a =[]
            for j in range(m1):      # A for loop for column entries
                a.append(int(input()))
            matrix2.append(a)
        # print(matrix2)
        msg=pickle.dumps(matrix)
        msg1=pickle.dumps(matrix2)
        # c.send(bytes(str(2),'utf-8'))
        c.send(msg)
        c.recv(4096).decode()
        c.send(msg1)
        ans = c.recv(4096)
        print(ans)
        ans = pickle.loads(ans)
        print(ans)


import tkinter as tk
from tkinter import filedialog
import pickle
import os
import socket
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
def performWordCount():
    c.send(bytes("1","utf-8"))

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

        # Connect to the API service
        service = build('drive', 'v3', credentials=creds)
        return service

    def open_file():
        file = filedialog.askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
        filepath = 1
        if file:
            filepath = os.path.abspath(file.name)
            service = get_gdrive_service()
            name = filepath.split('/')[-1]
            id = FileUpload(service,filepath)
            c.send(bytes(id,'utf-8'))
            ans = c.recv(4096).decode()
            ans = ans.split(" ")
            s = ""
            v=tk.Scrollbar(root1, orient='vertical',width=25)
            v.pack(side="right", fill='y')
            text=tk.Text(root1, font=("Georgia, 16"), yscrollcommand=v.set)
            v.config(command=text.yview)
            text.pack()
            for y in ans:
                # print(y)
                if ":" in y:
                    t = y.split(":")
                    # s = s + 
                    # print(s)
                    text.insert("end", f"{t[0]}: {t[1]}\n")
            btn.destroy()
    def FileUpload(service, filepath):
        name = filepath.split('/')[-1]
        mimetype = MimeTypes().guess_type(name)[0]
        file_metadata = {'name': name, "parents": ["19OaUa4opOlfYxHiEeDvQSrcTd9kXwwYJ"]}

        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            
            print("File Uploaded.")
            return file.get("id")
        
        except Exception as e:
            print("Can't Upload File.")
            print(e)
            return ""
    
    root1 = tk.Toplevel()
    root1.geometry("500x500")
    btn = tk.Button(root1,text = "Browse",command=open_file)
    btn.pack(pady=20)
    


def performMatrixMultiplication():
    c.send(bytes("2",'utf-8'))
    class MatrixInput(tk.Frame):
        def __init__(self, parent, rows=2, cols=2):
            super().__init__(parent)
            self.rows = rows
            self.cols = cols
            self.entries = [[tk.Entry(self) for j in range(cols)] for i in range(rows)]
            self.create_widgets()

        def create_widgets(self):
            for i in range(self.rows):
                for j in range(self.cols):
                    self.entries[i][j].grid(row=i, column=j)

        def get_matrix(self):
            matrix = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    value = self.entries[i][j].get()
                    try:
                        row.append(int(value))
                    except ValueError:
                        row.append(0)
                matrix.append(row)
            return matrix
        

    root1 = tk.Toplevel()
    root1.title("Matrix Multiplication")
    root1.geometry("500x500")
    
    

    def create_matrix1():
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        # global matrix1
        matrix_input = MatrixInput(root1, rows=rows, cols=cols)
        matrix_input.pack()

        def print_matrix1():
            # c.send(bytes("2",'utf-8'))
            matrix = matrix_input.get_matrix()
            
            c.send(pickle.dumps(matrix))
            c.recv(4096)
        button = tk.Button(root1, text="Submit First Matrix", command=print_matrix1)
        button.pack(pady=10)

    rows_entry = tk.Entry(root1)
    rows_entry.pack()

    cols_entry = tk.Entry(root1)
    cols_entry.pack()

    create_matrix_button = tk.Button(root1, text="Create First Matrix", command=create_matrix1)
    create_matrix_button.pack(pady=10)


    def create_matrix2():
        rows = int(rows_entry2.get())
        cols = int(cols_entry2.get())
        matrix_input = MatrixInput(root1, rows=rows, cols=cols)
        matrix_input.pack()

        def print_matrix2():
            matrix = matrix_input.get_matrix()
            c.send(pickle.dumps(matrix))
            ans = pickle.loads(c.recv(4096))
            
            root1.destroy()
            root3 = tk.Toplevel()
            s = ""
            s = '\n'.join([' '.join([str(i) for i in row]) for row in ans])
            tk.Label(root3,text=s,font=("Georgia, 16")).pack(pady=50)

        # matrix2 = 1
        button = tk.Button(root1, text="Submit Second Matrix", command=print_matrix2)
        button.pack(pady=10)
    rows_entry2 = tk.Entry(root1)
    rows_entry2.pack()

    cols_entry2 = tk.Entry(root1)
    cols_entry2.pack()
    create_matrix_button = tk.Button(root1, text="Create Second Matrix", command=create_matrix2)
    create_matrix_button.pack(pady=10)

root = tk.Tk()
root.geometry("500x500")

ip = ["192.168.29.73","192.168.29.62"]
i = 0
c = 1
PORT = 8000
while True:
    try:
        c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c.connect((ip[i],PORT))
        break
    except Exception as e:
        print("Error in connecting the socekt")
    i = (i + 1)%len(ip)

root.title("DISTRIBUTED SYSTEM")

label = tk.Label(root,text = "Client",font = ('Arial',18))
label.pack(pady=18)

matrixMultiplication = tk.Button(root,text = "Matrix Multiplication",font=("Arial",16),command = performMatrixMultiplication)
wordCount = tk.Button(root,text = "Word Count",font=("Arial",16),command=performWordCount)

matrixMultiplication.pack(pady=10)
wordCount.pack(pady=10)


root.mainloop()


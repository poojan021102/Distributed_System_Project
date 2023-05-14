# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

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
    
def FileDownload(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    
    # Initialise a downloader object to download the file
    downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
    done = False

    try:
        # Download the data in chunks
        while not done:
            done = downloader.next_chunk()

        fh.seek(0)
        
        # Write the received data to the file
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f)

        print("File Downloaded")
        # Return True if file Downloaded successfully
        return True
    except:
        
        # Return False if something went wrong
        print("Something went wrong.")
        return False

if __name__ == "__main__":
    service = get_gdrive_service()
    f_path = input("Enter full file path: ")
    name = f_path.split('/')[-1]
    id = FileUpload(service,f_path)
    if id != "":
        FileDownload(service, id, "demo.txt")  
    
# import pickle
# import os.path
# import email
# from email.mime.text import MIMEText
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import base64
# from googleapiclient import errors
# import json

# #Handles email fetching from Gmail and saves the data in inputs.json

# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# def search_message(service, user_id, search_string, max_results=13):
#     """
#     Search the inbox for emails using standard gmail search parameters
#     and return a list of email IDs for each result

#     PARAMS:
#         service: the google api service object already instantiated
#         user_id: user id for google api service ('me' works here if
#         already authenticated)
#         search_string: search operators you can use with Gmail
#         (see https://support.google.com/mail/answer/7190?hl=en for a list)

#     RETURNS:
#         List containing email IDs of search query
#     """
#     try:
#         # initiate the list for returning
#         list_ids = []

#         # get the id of all messages that are in the search string
#         search_ids = service.users().messages().list(
#             userId=user_id,
#             q=search_string,
#             maxResults=max_results
#         ).execute()
        
#         # if there were no results, print warning and return empty string
#         try:
#             ids = search_ids['messages']

#         except KeyError:
#             print("WARNING: the search query returned 0 results")
#             return []

#         for msg in ids:
#             if isinstance(msg, dict) and 'id' in msg:
#                 list_ids.append(msg['id'])

#         return list_ids

#     except errors.HttpError as error:
#         print(f"An error occurred during Gmail search: {error}")
#         return []
        


# def get_messages(service, user_id, msg_id):
#     """
#     Search the inbox for specific message by ID and return it back as a 
#     clean string. String may contain Python escape characters for newline
#     and return line. 
    
#     PARAMS
#         service: the google api service object already instantiated
#         user_id: user id for google api service ('me' works here if
#         already authenticated)
#         msg_id: the unique id of the email you need

#     RETURNS
#         A string of encoded text containing the message body
#     """
#     try:
#         # grab the message instance
#         message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
#         payload = message.get('payload')
#         headers = payload.get('headers')

#         subject = None
#         sender = None
#         for header in headers:
#             if header['name'] == 'Subject':
#                 subject = header['value']
#             if header['name'] == 'From':
#                 sender = header['value']

#         body = get_email_body(payload)

#         return {
#             'id': msg_id,
#             'subject': subject,
#             'sender': sender,
#             'body': body
#         }
#     except Exception as error:
#         print(f"An error occurred: {error}")
#         return {}

# def get_email_body(payload):
#     body = ""
#     if 'parts' in payload:
#         for part in payload['parts']:
#             if part['mimeType'] == 'text/plain':
#                 body += part['body']['data']
#             elif part['mimeType'] == 'text/html':
#                 body += part['body']['data']
#     else:
#         body = payload['body']['data']
    
#     body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8')
#     return body


# def get_service():
#     """
#     Authenticate the google api client and return the service object 
#     to make further calls

#     PARAMS
#         None

#     RETURNS
#         service api object from gmail for making calls
#     """
#     creds = None

#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)


#     service = build('gmail', 'v1', credentials=creds)

#     return service


# def main():
#     service = get_service()
#     user_id = 'me'
#     search_string = 'subject:Thank you'  
#     max_results = 20
#     email_ids = search_message(service, user_id, search_string, max_results)
#     emails = []
#     for email_id in email_ids:
#         email_data = get_messages(service, user_id, email_id)
#         if email_data:
#             emails.append(email_data)
    
#     inputs = []
#     for email in emails:
#         full_email = f"Email ID: {email['id']} Subject: {email['subject']} Sender: {email['sender']} Body: {email['body']}"
#         inputs.append(full_email)
    
#     with open('backend/inputs.json', 'w') as json_file:
#         json.dump(inputs, json_file, indent=4)

#     print(emails)
#     print(f"Emails have been converted to inputs.json")

# if __name__ == '__main__':
#     main()


import pandas as pd

train = pd.read_csv("train.csv")
valid = pd.read_csv("valid.csv")

print("Train labels:", sorted(train["label"].unique()))
print("Valid labels:", sorted(valid["label"].unique()))


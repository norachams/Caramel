import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


load_dotenv()




def main():
    """Shows basic usage of the Gmail API. Lists the user's Gmail messages.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        # Define your search query using the 'q' parameter
        # This will search for messages containing any of the terms in the subject or body
        search_query = '"thank you" OR "thank you applying" OR "thanks for your interest" OR "application" OR "interview" OR "Invitation"'

        results = (
            service.users()
            .messages()
            .list(userId="me", q=search_query) # Use the 'q' parameter for searching
            .execute()
        )
        messages = results.get("messages", [])

      
        for message in messages:

            msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
            body = extract_body(msg["payload"])
            print(f"Message ID: {message['id']}\n{body}\n")

            # msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
            # payload = msg["payload"]
            # body_data = payload["parts"][0]["body"]["data"] if "parts" in payload else payload["body"]["data"]
            # body = base64.urlsafe_b64decode(body_data).decode("utf-8")
            # print(f"Message ID: {message['id']}\n{body}\n")
            # # print(f' Subject: {msg["snippet"]}') 

    except HttpError as error:
        print(f"An error occurred: {error}")

    

def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
            elif part["mimeType"] == "text/html":
                html = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                return BeautifulSoup(html, "html.parser").get_text(separator="\n", strip=True)
            elif part["mimeType"].startswith("multipart/"):
                return extract_body(part)
    elif "body" in payload and "data" in payload["body"]:
        data = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        if payload.get("mimeType") == "text/html":
            return BeautifulSoup(data, "html.parser").get_text(separator="\n", strip=True)
        return data
    return ""




if __name__ == "__main__":
    main()


# import os
# import requests

# API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
# headers = {
#     "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
# }

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# output = query({
#     "inputs": "Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!",
#     "parameters": {"candidate_labels": ["refund", "legal", "faq"]},
# })
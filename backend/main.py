import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spacy
from datetime import datetime
nlp = spacy.load("en_core_web_trf")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


load_dotenv()

from transformers import pipeline
import json

MODEL_PATH = "/Users/norach/Documents/Projects/job-tracker/backend/email-classifier"


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

        email_data_list = []

        for i, message in enumerate(messages):
            msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
            body = extract_body(msg["payload"])
            company = get_company(body) or "Unknown"
            print(f"\n📩 Email {i+1}: {company}\n{body[:200]}...\n")
            date = get_email_date(msg)

            email_data_list.append({
                "id": message["id"],
                "body": body,
                "company": company,
                "date": date,
            })

        # Now classify just the bodies
        email_texts = [email["body"] for email in email_data_list]
        classifications = classify_emails(email_texts)

        # Merge the classification results back into each record
        for i, classification in enumerate(classifications):
            email_data_list[i].update({
                "predicted_label": classification["predicted_label"],
                "score": classification["score"]
            })

        # Save or print the final output
        # with open("classified_emails.json", "w", encoding="utf-8") as f:
        #     json.dump(email_data_list, f, ensure_ascii=False, indent=2)
        # print("\n Classified emails with company names saved to classified_emails.json")

        return email_data_list  
        
        
    except HttpError as error:
        print(f"An error occurred: {error}")



def classify_emails(email_texts, model_path=MODEL_PATH):
    classifier = pipeline(
        "text-classification",
        model=model_path,
        tokenizer=model_path,
        truncation=True,
        max_length=512
    )
    results = []

    for i, text in enumerate(email_texts): 
        prediction = classifier(text[:2000])[0]  
        results.append({
            "id": i + 1,
            "predicted_label": prediction["label"],
            "score": prediction["score"],
            "text": text
        })

    return results

    
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



def get_company(email_text):
    """Extracts company name from an email's text using Named Entity Recognition."""
    doc = nlp(email_text)
    for ent in doc.ents:
        if ent.label_ == "ORG":  
            return ent.text.strip()
    return None

def get_email_date(msg):
    for header in msg["payload"].get("headers", []):
        if header["name"].lower() == "date":
            return header["value"]
    if "internalDate" in msg:
        ts = int(msg["internalDate"]) / 1000
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    return None



if __name__ == "__main__":
    main()



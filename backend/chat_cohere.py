# backend/chat_cohere.py

import os
import re
import json
import pathlib
import email.utils
from dotenv import load_dotenv
import cohere

# load .env (COHERE_API_KEY)
load_dotenv()

# your fine‐tuned model ID
FT_MODEL_ID = "cc21b29a-ec70-40a5-8e50-16b54aab292f-ft"

# init client
co = cohere.Client(os.getenv("COHERE_API_KEY"))


def extract_company(email_data):
    """
    Try to pull a company name out of the subject/body; otherwise
    fall back to the sender’s domain.
    """
    subj = email_data.get("subject", "") or ""
    body = email_data.get("body", "") or ""

    # 1) Common subject‐line patterns
    subject_patterns = [
        r"application to\s+([^,–\|!]+)",
        r"applying to\s+([^,–\|!]+)",
        r"interest in\s+([^,–\|!]+)",
        r"interview (?:with|invitation with)\s+([^,–\|!]+)",
        r"thank you[, ]+(?:for your )?(?:application|interest|submission)[^–]*–\s*([^,–\|!]+)",
    ]
    for pat in subject_patterns:
        m = re.search(pat, subj, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    # 2) Common body‐text patterns
    body_patterns = [
        r"position (?:at|with)\s+([A-Z][A-Za-z& ]+)",
        r"thank you for (?:your|applying to)\s+([A-Z][A-Za-z& ]+)",
    ]
    for pat in body_patterns:
        m = re.search(pat, body, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    # 3) Fallback: parse the sender’s domain
    _, addr = email.utils.parseaddr(email_data.get("sender", ""))
    if "@" in addr:
        dom = addr.split("@", 1)[1].split(".")[0]
        return dom.replace("-", " ").title()

    return "Unknown"


def classify_emails(emails):
    """
    emails: list of dicts, each with keys 'id', 'subject', 'sender', 'body'

    Returns cleaned list with:
      email_id, subject, classification, confidence, company
    """

    # build the raw text inputs the same way you did for inputs.json
    inputs = [
        f"Email ID: {e['id']} Subject: {e['subject']} Sender: {e['sender']} Body: {e['body']}"
        for e in emails
    ]
    if not inputs:
        raise ValueError("No emails provided for classification.")

    print(f"[DEBUG] Prepared {len(inputs)} inputs")

    # call your fine‐tuned Cohere model
    try:
        resp = co.classify(model=FT_MODEL_ID, inputs=inputs)
    except Exception as e:
        print("[ERROR] Cohere classify failed:", e)
        raise

    print(f"[DEBUG] Received {len(resp.classifications)} classifications")

    # post‐process into your cleaned output
    cleaned = []
    for email_data, cls in zip(emails, resp.classifications):
        cleaned.append({
            "email_id":       email_data["id"],
            "subject":        email_data["subject"],
            "classification": cls.prediction,
            "confidence":     cls.confidence,
            "company":        extract_company(email_data)
        })

    # write out for debugging / frontend use
    out_path = pathlib.Path("backend/cleaned_classifications.json")
    out_path.write_text(json.dumps(cleaned, indent=2))
    print(f"[INFO] Wrote {len(cleaned)} records → {out_path.resolve()}")

    return cleaned

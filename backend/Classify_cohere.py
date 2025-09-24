import email.utils
import json
import os
import re
from typing import Dict, List, Optional

import cohere
from cohere import ClassifyExample
from dotenv import load_dotenv

load_dotenv()


def extract_company(email_data):
    """Best-effort company extraction from subject/body/sender."""
    subject = (email_data.get('subject') or '').strip()
    body = (email_data.get('body') or '').strip()
    sender = (email_data.get('sender') or '').strip()

    subject_patterns = [
        r"application to\s+([^,–\|!]+)",
        r"applying to\s+([^,–\|!]+)",
        r"interview (?:with|invitation with)\s+([^,–\|!]+)",
        r"thank you[, ]+(?:for your )?(?:application|interest|submission)[^–]*–\s*([^,–\|!]+)",
        r"thank you for your application to\s+([^,–\|!]+)",
    ]
    for pattern in subject_patterns:
        match = re.search(pattern, subject, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    body_patterns = [
        r"thank you for (?:your|applying to)\s+([A-Z][A-Za-z& ]+)",
        r"position (?:at|with)\s+([A-Z][A-Za-z& ]+)",
        r"interview (?:with|at)\s+([A-Z][A-Za-z& ]+)",
    ]
    for pattern in body_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    _, addr = email.utils.parseaddr(sender)
    if '@' in addr:
        domain = addr.split('@', 1)[1].split('.', 1)[0]
        return domain.replace('-', ' ').title()

    return "Unknown"


def classify_emails(emails):
    if not emails:
        return []

    with open('backend/examples.json', 'r') as f:
        examples_data = json.load(f)
    examples = [ClassifyExample(text=example['text'], label=example['label']) for example in examples_data]

    inputs = [
        f"Email ID: {email.get('id')} Subject: {email.get('subject')} Sender: {email.get('sender')} Body: {email.get('body')}"
        for email in emails
    ]

    # Persist raw inputs for debugging/inspection.
    with open('backend/inputs.json', 'w') as f:
        json.dump(inputs, f, indent=4)

    cohere_api_key = os.getenv('COHERE_API_KEY')
    co = cohere.Client(cohere_api_key)

    try:
        response = co.classify(
            model='embed-english-v2.0',
            inputs=inputs,
            examples=examples
        )
        print("Classification request successful. Processing response...")

        cleaned_output: List[Dict[str, Optional[str]]] = []
        for email_data, classification in zip(emails, response.classifications):
            confidence: Optional[float] = None
            if getattr(classification, 'confidence', None) is not None:
                confidence = classification.confidence
            elif getattr(classification, 'labels', None):
                predicted = classification.prediction
                label_info = classification.labels.get(predicted)
                if isinstance(label_info, dict):
                    confidence = label_info.get('confidence')
                else:
                    confidence = getattr(label_info, 'confidence', None)

            cleaned_output.append({
                'email_id': email_data.get('id'),
                'subject': email_data.get('subject'),
                'classification': classification.prediction,
                'confidence': confidence,
                'company': extract_company(email_data)
            })

        with open('backend/cleaned_classifications.json', 'w') as f:
            json.dump(cleaned_output, f, indent=4)

        print(cleaned_output)
        return cleaned_output

    except Exception as e:
        print(f"Error during classification: {e}")
        return []


if __name__ == '__main__':
    classify_emails([])

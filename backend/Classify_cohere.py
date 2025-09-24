import email.utils
import json
import os
import cohere
from dotenv import load_dotenv
import spacy



nlp = spacy.load("en_core_web_sm")

load_dotenv()

_LABELS = {"application received", "interview", "rejected"}


def extract_company(email_entry):
    body = (email_entry.get('body') or '').strip()
    subject = (email_entry.get('subject') or '').strip()
    sender = (email_entry.get('sender') or '').strip()

    text = body or subject
    if text:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_.upper() == 'ORG':
                return ent.text.strip()

    _, addr = email.utils.parseaddr(sender)
    if '@' in addr:
        domain = addr.split('@', 1)[1].split('.', 1)[0]
        return domain.replace('-', ' ').title()

    return 'Unknown'


def _build_prompt(email_entry):
    subject = email_entry.get('subject') or ''
    sender = email_entry.get('sender') or ''
    body = email_entry.get('body') or ''
    return (
        "You label job application emails into exactly one class from this set: "
        "Application Received, Interview, Rejected.\n"
        "Reply with only the class name, nothing else.\n"
        f"Subject: {subject}\n"
        f"Sender: {sender}\n"
        "Body:\n"
        f"{body}\n"
    )


def _fallback_label(email_entry):
    text = ' '.join(
        filter(None, [email_entry.get('subject'), email_entry.get('body')])
    ).lower()

    interview_cues = [
        'interview',
        'schedule a call',
        'looking forward to speaking',
        'invite you to interview',
    ]
    rejection_cues = [
        'unfortunately',
        'regret to inform',
        'move forward with other candidates',
        'not selected',
        'will not be proceeding',
    ]
    received_cues = [
        'thank you for your application',
        'we have received your application',
        'your application has been received',
    ]

    if any(phrase in text for phrase in interview_cues):
        return 'Interview'
    if any(phrase in text for phrase in rejection_cues):
        return 'Rejected'
    if any(phrase in text for phrase in received_cues):
        return 'Application Received'

    return 'Unknown'


def _parse_label(raw_text, email_entry):
    cleaned = (raw_text or '').strip().lower()
    for label in _LABELS:
        if label in cleaned:
            return label.title()
    fallback = _fallback_label(email_entry)
    return fallback


def classify_emails(emails):
    if not emails:
        return []

    inputs = [
        f"Email ID: {email.get('id')} Subject: {email.get('subject')} Sender: {email.get('sender')} Body: {email.get('body')}"
        for email in emails
    ]
    with open('backend/inputs.json', 'w') as f:
        json.dump(inputs, f, indent=4)

    cohere_api_key = os.getenv('COHERE_API_KEY')
    ft_model_id = os.getenv('FT_MODEL_ID')
    if not cohere_api_key:
        raise RuntimeError('COHERE_API_KEY not configured')
    if not ft_model_id:
        raise RuntimeError('FT_MODEL_ID not configured')

    client = cohere.Client(cohere_api_key)

    cleaned_output = []

    for email_entry in emails:
        prompt = _build_prompt(email_entry)
        try:
            generation = client.generate(
                model=ft_model_id,
                prompt=prompt,
                max_tokens=16,
                temperature=0.0,
                stop_sequences=['\n']
            )
            raw_text = generation.generations[0].text if generation.generations else ''
        except Exception as error:
            print(f"Error during classification generate call: {error}")
            raw_text = ''

        label = _parse_label(raw_text, email_entry)

        cleaned_output.append({
            'email_id': email_entry.get('id'),
            'subject': email_entry.get('subject'),
            'classification': label,
            'confidence': None,
            'company': extract_company(email_entry)
        })

    with open('backend/cleaned_classifications.json', 'w') as f:
        json.dump(cleaned_output, f, indent=4)

    print(cleaned_output)
    return cleaned_output


if __name__ == '__main__':
    classify_emails([])

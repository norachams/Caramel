import os
from flask import Flask, jsonify
from flask_cors import CORS
import get_messages
from chat_cohere import classify_emails
import traceback


# The main Flask application that serves the API endpoints
#it connects to both Gmail and Firebase.
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "JobJourney Backend API"

@app.route('/tracker', methods=['GET'])
def get_classifications():
    try:
        service = get_messages.get_service()
        user_id = 'me'
        search_string = 'subject:Thank you' 
        email_ids = get_messages.search_message(service, user_id, search_string)
        emails = []
        print("→ fetched email IDs:", email_ids)
        for email_id in email_ids:
            email_data = get_messages.get_messages(service, user_id, email_id)
            if email_data:
                emails.append(email_data)
        print("→ built emails payload, count:", len(emails))
        classifications = classify_emails(emails)
        return jsonify(classifications)
    except Exception as e:
        traceback.print_exc()
        app.logger.error("Error in /tracker", exc_info=e)
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)),  debug=True)


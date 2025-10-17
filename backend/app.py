import os
from flask import Flask, jsonify
from flask_cors import CORS
import traceback
from main import main 


# The main Flask application that serves the API endpoints
#it connects to both Gmail and Firebase.
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Caramel Backend API"

@app.route('/tracker', methods=['GET'])
def get_classifications():
    try:
        print("→ Fetching and classifying emails...")
        data = main()  
        print(f"→ {len(data)} emails processed.")
        return jsonify(data)  
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)),  debug=True)

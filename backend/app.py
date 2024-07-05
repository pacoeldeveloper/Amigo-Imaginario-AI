# Import libraries
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app # type: ignore
from dotenv import load_dotenv #type: ignore
from gemini import GeminiController

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

# Initialize object
gemini_controller = GeminiController()

@app.route('/ping')
def ping():
    return jsonify({"message":"pong"}),200

@app.route('/test_gemini', methods=['GET'])
def test_gemini():
    return jsonify({"message": gemini_controller.generate_text("What is the meaning of life")}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8082)
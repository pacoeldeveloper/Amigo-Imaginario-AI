# Import libraries
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app # type: ignore

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route('/ping')
def ping():
    return jsonify({"message":"pong"}),200

if __name__ == "__main__":
    app.run(debug=True, port=8082)
# app.py
# Required Imports

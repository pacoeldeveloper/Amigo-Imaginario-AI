# Import libraries
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app  # type: ignore
from dotenv import load_dotenv  # type: ignore
from gemini import GeminiController

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
users = db.collection("users")  # The collection has to be created in the Firestore DB
forms = db.collection("forms")  # The collection has to be created in the Firestore DB
friends = db.collection(
    "friends"
)  # The collection has to be created in the Firestore DB

# Initialize gemini controller object
gemini_controller = GeminiController()


@app.route("/ping")
def ping():
    return jsonify({"message": "pong"}), 200


@app.route("/get_all_users", methods=["GET"])
def get_all_users():
    all_users = [{**doc.to_dict(), "user_id": doc.id} for doc in users.stream()]
    return jsonify(all_users), 200


@app.route("/get_user", methods=["GET"])
def get_user():
    user_id = request.args.get("user_id")
    user = users.document(user_id).get()
    return jsonify(user.to_dict()), 200


@app.route("/create_user", methods=["POST"])
def create_user():
    user_data = request.json
    user_id = user_data.get("user_id")  # Assuming the client sends a 'user_id'
    if not user_id:
        return jsonify({"message": "Missing user_id"}), 400  # Bad request if no user_id

    # Remove the user_id from the data to be stored
    user_data.pop("user_id", None)

    # Create or overwrite the document with the specified user_id
    users.document(user_id).set(user_data)

    return jsonify({"message": "User created"}), 200


@app.route("/update_user", methods=["PUT"])
def update_user():
    user = request.json
    user_id = user["user_id"]
    user.pop("user_id", None)
    users.document(user_id).update(user)
    return jsonify({"message": "User updated"}), 200


@app.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_id = request.args.get("user_id")
    users.document(user_id).delete()
    return jsonify({"message": "User deleted"}), 200


@app.route("/test_gemini", methods=["GET"])
def test_gemini():
    return (
        jsonify(
            {"message": gemini_controller.generate_text("What is the meaning of life")}
        ),
        200,
    )


@app.route("/get_all_forms", methods=["GET"])
def get_all_forms():
    all_forms = [{**doc.to_dict(), "form_id": doc.id} for doc in forms.stream()]
    return jsonify(all_forms), 200


@app.route("/save_friend_form", methods=["POST"])
def save_form_response_in_user():
    data = request.json  # Answers
    answers = data["answers"]
    user_id = data["user_id"]
    friend_name = data["friend_name"]
    # Create friend
    friend = friends.document()
    friend.set({"name": friend_name, "answers": answers})
    # Register friend_id in user
    user = users.document(user_id).get().to_dict()
    user["friends"] = user.get("friends", [])
    user["friends"].append(friend.id)
    users.document(user_id).set(user)
    return jsonify({"message": "Friend created"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8082)

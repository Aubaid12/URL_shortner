from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import re
import hashlib
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)


MONGO_URI = "mongodb+srv://Aubaid:12345@cluster0.7a1d5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB connection string
DB_NAME = "URL_shortner"
COLLECTION_NAME = "url"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()  # Exit the application if MongoDB connection fails


def create_code(url):
    code = hashlib.blake2b(str(url).encode(), key="1234".encode(), digest_size=4).hexdigest()
    collection.insert_one({"original_url": url, "shortened_url": code})
    return code


def check_url(url):
    existing_url = collection.find_one({"original_url": url})
    if existing_url:
        return existing_url["shortened_url"]
    else:
        return create_code(url)


def code_to_url(code):
    url_data = collection.find_one({"shortened_url": code})
    if url_data:
        return url_data["original_url"]
    else:
        return "Invalid URL"


@app.route("/url_shortner", methods=["GET"])
def generate_url():
    url = request.args.get("url")
    if not url:
        return jsonify("Please Enter an URL")
    pattern = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'
    match_pattern = re.match(pattern, url) is not None
    if not match_pattern:
        return jsonify("Please enter a valid URL")
    shortened_url = check_url(url)
    return jsonify("https://urlsht.onrender.com/" + shortened_url), 200


@app.route("/<code>", methods=["GET"])
def redirect_url(code):
    original_url = code_to_url(code)
    if original_url == "Invalid URL":  # Direct string comparison
        return f"<h1>{original_url}</h1>", 200
    return redirect(original_url)  # No need for indexing


if __name__ == "__main__":
    app.run(debug=False)

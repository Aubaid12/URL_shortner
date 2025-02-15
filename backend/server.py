from flask import Flask, request, jsonify, redirect
from flask_cors import CORS 
import string
import sqlite3
import re
import hashlib

app = Flask(__name__)

CORS(app)
db_name = "sql_url.db"
   
def connected_db():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS URL_TABLE(ORIGINAL_URL TEXT NOT NULL, SHORTENED_URL TEXT NOT NULL)")
    connection.commit()
    return connection

def create_code(url):
    #code = "".join(random.choices(string.ascii_letters+string.digits,k=7))
    connection = connected_db()
    code = hashlib.blake2b(str(url).encode(),key="1234".encode(),digest_size=4).hexdigest()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO URL_TABLE(ORIGINAL_URL, SHORTENED_URL) values(?,?)", (url,code))
    connection.commit()
    connection.close()
    return code
    

def check_url(url):
    connection = connected_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM URL_TABLE WHERE ORIGINAL_URL = ? ", (url,))
    row = cursor.fetchall()
    if len(row) == 0:
        connection.close()
        return create_code(url)   
    else:
        connection.close()
        return row[0][1]
    
def code_to_url(code):
    connection = connected_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM URL_TABLE WHERE SHORTENED_URL = ? ", (code,))
    row = cursor.fetchall()
    connection.commit()
    connection.close()
    if row:
        return row
    else:
        return "Invalid URL"
    

@app.route("/url_shortner" , methods = ["GET"] )
def generate_url():
    url = request.args.get("url")
    if not url: 
        return jsonify("Please Enter an URL")
    pattern = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'
    match_pattern = re.match(pattern, url) is not None
    if not match_pattern:
        return jsonify("Please enter a valid URL")
    shortned_url = check_url(url)
    return jsonify("https://url-shortner-4eg5.onrender.com/"+shortned_url) , 200




@app.route("/<code>", methods = ["GET"])
def redirect_url(code):
    original_url = code_to_url(code)
    if type(original_url) is string:
        return f"<h1>{original_url}</h1>", 200
    return redirect(original_url[0][0])


if __name__ == "__main__":
    app.run(debug = False)



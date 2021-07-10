# Python Library
from flask import Flask, url_for, redirect, render_template, request

# Our Custom Database Module
from database.score import scoreDB
from database.user import userDB

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
import os

from flask import Flask, flash, redirect, render_template, request, sessions
from flask_session import Session

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return render_template("login.html")
    else:
        return render_template("login.html")
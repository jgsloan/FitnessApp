import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, sessions
from flask_session import Session

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite Database
try:
    sqliteConnection = sqlite3.connect('moveforward.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Home screen and route
@app.route("/")
@login_required
def index():
    return render_template("login.html")


# Login screen and route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return render_template("login.html")
    else:
        return render_template("login.html")


# Register screen and route
@app.route("/register", methods=["GET", "POST"])
def register():
    
    error = None

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Check for blank username or password and return and apology
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("passwordcheck") :
            error = 'Please enter a username & password'
            return render_template("register.html", error=error)

        # Query database for username
        if cursor.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        ):
            error = 'Username already exists please choose another'
            return render_template("register.html", error=error)

        # Check password and password confirmation match
        if request.form.get("password") != request.form.get("passwordcheck"):
            error = 'Passwords do not match'
            return render_template("register.html", error=error)

        # Store username and hased password
            

        # Store username and password in moveforward.db database
            

        # Add username to a variable
            

        # Remember user
            

            # Redirect user to homepage
    
    else:  
        # Load registration page 
        return render_template("register.html")
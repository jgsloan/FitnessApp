import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create an events array for use with calendar
events = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Welcome Screen"""
    return render_template("index.html", events=events) 


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in """

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Connect to database
        try:
            con = sqlite3.connect("moveforward.db")
            cursor = con.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Please enter a username & password"
            return render_template("login.html", error=error)

        # Ensure password was submitted
        if not request.form.get("password"):
            error = "Please enter a username & password"
            return render_template("login.html", error=error)
           
        # Query database for username
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        )
        rows = cursor.fetchall()
        print(rows)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][2], request.form.get("password")
        ):
            error = "Incorrect username and/or password"
            return render_template("login.html", error=error)
    
        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Close database
        con.close()

        # Redirect to home page
        return render_template("index.html")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
    # Logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Register screen and route
@app.route("/register", methods=["GET", "POST"])
def register():
    
    error = None

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Connect to database
        try:
            sqliteConnection = sqlite3.connect('moveforward.db')
            cursor = sqliteConnection.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

        # Check for blank username or password and return and apology
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("passwordcheck") :
            error = 'Please enter a username & password'
            return render_template("register.html", error=error)

        # Query database for username
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM users WHERE username = ? LIMIT 1)", (request.form.get("username"),))
        record = cursor.fetchone()
        
        if record[0] == 1:
            error = 'Username already exists please choose another'
            return render_template("register.html", error=error)

        # Check password and password confirmation match
        if request.form.get('password') != request.form.get('passwordcheck'):
            error = 'Passwords do not match'
            return render_template("register.html", error=error)

        # Store username and hased password
        username = request.form.get("username")
        hashed_password = generate_password_hash(request.form.get("password"))    

        # Store username and password in moveforward.db database
        cursor.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", (username, hashed_password)
        )   
        sqliteConnection.commit()

        # Add username to a variable
        cursor.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        )   
        id = cursor.fetchone()

        # Remember user
        session["user_id"] = id

        # Close database
        sqliteConnection.close()

        # Redirect user to homepage
        return redirect("/")
    
    else:  
        # Load registration page 
        return render_template("register.html")

@app.route("/calendar", methods=["POST", "GET"])
@login_required
def calendar():
    
    # Get current user
    user = session["user_id"]

    # Access Move Forward database
    try:
        con = sqlite3.connect('moveforward.db')
        cursor = con.cursor()
    except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    # Read database
    cursor.execute(
        "SELECT * FROM workouts WHERE id = ?", (user,)
    )
    row = cursor.fetchone()

    #empty array
    events.clear()

    # Populate array with workouts from workouts table in MF database.
    while row:
        events_dict = {
                'id' : row[0],
                'title' : row[2],
                'start' : row[4],
                'extendedProps' : {
                    'description' : row[3]
                }
            }
        events.append(events_dict)
        row = cursor.fetchone()

    return render_template("calendar.html", events=events)


@app.route("/add", methods=["POST",])
@login_required
def add():
    
    error = None
    user = session["user_id"]
    
    # Check if form submitted via post
    if request.method == 'POST':
        
         # add form entries into variables
        print(user)
        title = request.form.get("title")
        print(title)
        description = request.form.get("description")
        print(description)
        date = request.form.get("workoutDate")
        print(date)   
        
        # Connect to database
        try:
            con = sqlite3.connect('moveforward.db')
            cursor = con.cursor()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        
        print(user)
        try:
            # Add title, description and date into workout table
            cursor.execute(
                "INSERT INTO workouts (id, title, workoutDescription, date) VALUES (?, ?, ?, ?)", (user, title, description, date)
            )
            con.commit()
            
        except Exception as e:
            print("Error: ", e)    
        
        return redirect("/calendar")
        
    else:
        return render_template("calendar.html")
    

@app.route("/deleteWorkout", methods=["POST"])
@login_required
def deleteWorkout():
    
    if request.method == "POST":
        
        eventID = request.form.get("eventID")
        eventTitle = request.form.get("eventTitle")
        print(eventID)
        print(eventTitle)
     
        try:
            con = sqlite3.connect('moveforward.db')
            cursor = con.cursor()
        
            cursor.execute(
                "DELETE FROM workouts WHERE eventID = ?", (eventID,)
            )
            con.commit()        
        
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
    
        return redirect("/calendar")
        
    else:
        return redirect("/calendar")
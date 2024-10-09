import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

from functools import wraps

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
    
    # store user id
    user = session["user_id"]
    
    # Connect to database
    try:
            sqliteConnection = sqlite3.connect('moveforward.db')
            cursor = sqliteConnection.cursor()
    except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
            
            # Fetch Add username to a variable
    cursor.execute(
            "SELECT username FROM users WHERE id = ?", (user,)
        )   
    result = cursor.fetchone()
    
    # Unpack the username from the tuple if the result is not None
    if result:
        username = result[0]
    else:
        username = "Guest"  # or handle the case where the user is not found
    
    return render_template("index.html", events=events, username=username) 


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
    print(user)
    cursor.execute(
        "SELECT * FROM workouts WHERE id = ?", (user,)
    )
    row = cursor.fetchone()

    #empty array
    events.clear()

    # Populate array with workouts from workouts table in MF database.
    while row:
        events_dict = {
                'id' : row[1],
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
    
    # Check if 'user' is a tuple and unpack it if necessary
    if isinstance(user, tuple):
        user = user[0]  # Unpack the first element
    
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
        
        # close database connection
        con.close()
        
        # redirect to the calendar page to reload events
        return redirect("/calendar")
        
    else:
        return render_template("calendar.html")
    

@app.route("/deleteWorkout", methods=["POST"])
@login_required
def deleteWorkout():
    
    if request.method == "POST":
        
        # Get id from hidden form in calendar HTML 
        id = request.form.get('workoutID')
    
        # Connect to database
        try:
            con = sqlite3.connect('moveforward.db')
            cursor = con.cursor()

            # delete event from database using id to identify correct workout to delete
            cursor.execute(
                "DELETE FROM workouts WHERE eventID = ?", (id,)
            )
            con.commit()        
        
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
    

        # close database connection
        con.close()

        # redirect to the calendar page
        return redirect("/calendar")
        
    else: 
        return redirect("/calendar")

# TODO: make calendar events editable    
@app.route("/editWorkout", methods =["POST"])
@login_required
def editWorkout():
    return redirect("/calendar")

@app.route("/exercises", methods=["GET", "POST"])
@login_required
def exercises():
    return render_template("exercises.html")

@app.route("/workouts", methods=["GET", "POST"])
@login_required
def workouts():
        
    # Connect to database
    try:
        con = sqlite3.connect('moveforward.db')
        cursor = con.cursor()

        if request.method =='POST':

        # Store name and description into variabkes
            name = request.form.get("name")
            description = request.form.get("description")

        # Store in hero_wods database
            cursor.execute(
                "INSERT INTO hero_wods (name, description) VALUES (?,?)", (name, description)
            )
            con.commit()

        # Store hero_wod table into array
        cursor.execute("SELECT * FROM hero_wods")
        rows = cursor.fetchall()  # Fetch all rows
        
        # Get column names only after executing the query
        column_names = [description[0] for description in cursor.description]

        # Convert rows to a list of dictionaries
        hero_wods = [dict(zip(column_names, row)) for row in rows]
    
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return("Database Error")

    # Add ID to array
    wodID = []
    for i in hero_wods:
        wodID.append(i["wodID"])

    # Add name to array 
    wodName = []
    for i in hero_wods:
        wodName.append(i["name"])

    # Add description to array
    wodDescription = []
    for i in hero_wods:
        wodDescription.append(i["description"])

    return render_template("workouts.html", wodID=wodID, wodName=wodName, wodDescription=wodDescription)

@app.route("/favourites", methods=["GET", "POST"])
@login_required
def favourites():
    # TODO: Create a favourites library
    return render_template("favourites.html")

@app.route("/favourite", methods=["GET","POST"])
@login_required
def favourite():

    if request.method == "POST":

        # Retrieve checkbox values
        is_favorite = 'favourite' in request.form  # Will be True if the checkbox is checked
        if is_favorite:
            print("Checkbox is checked!")
        else:
            print("Checkbox is unchecked!")


# ChatGPT used to assist with fucntion of this route specifically how to check for data in table before writing to it
@app.route("/profile", methods=["GET", "POST"])
@login_required
def barbells(): 
    # Get current user
    user = session["user_id"]

    # Initialize variables to store current values
    current_values = {
        "Deadlift 1RM": None,
        "Clean 1RM": None,
        "Snatch 1RM": None,
        "Push Press 1RM": None,
        "Push Jerk 1RM": None,
        "Squat Clean and Jerk 1RM": None,
    }

    # Connect to the database
    try:
        con = sqlite3.connect('moveforward.db')
        cursor = con.cursor()

        # Fetch current values for all movements
        for movement_name in current_values.keys():
            cursor.execute(
                "SELECT one_rep_max FROM barbel_movement WHERE user_id = ? AND bb_movement_name = ?",
                (user, movement_name)
            )
            result = cursor.fetchone()
            current_values[movement_name] = result[0] if result else None

        if request.method == "POST":
            # Retrieve form values
            form_data = {
                "Deadlift 1RM": request.form.get("1rep_max_deadlift"),
                "Clean 1RM": request.form.get("1rep_max_clean"),
                "Snatch 1RM": request.form.get("1rep_max_snatch"),
                "Push Press 1RM": request.form.get("1rep_max_pushpress"),
                "Push Jerk 1RM": request.form.get("1rep_max_pushjerk"),
                "Squat Clean and Jerk 1RM": request.form.get("1rep_max_squat_clean_and_jerk"),
            }

            # Update or insert values in the database
            for movement_name, one_rep_max in form_data.items():
                if one_rep_max:
                    # Check if an entry already exists for the user
                    cursor.execute(
                        "SELECT COUNT(*) FROM barbel_movement WHERE user_id = ? AND bb_movement_name = ?",
                        (user, movement_name)
                    )
                    exists = cursor.fetchone()[0]

                    if exists:
                        # Update existing record
                        cursor.execute(
                            "UPDATE barbel_movement SET one_rep_max = ? WHERE user_id = ? AND bb_movement_name = ?",
                            (one_rep_max, user, movement_name)
                        )
                    else:
                        # Insert new record
                        cursor.execute(
                            "INSERT INTO barbel_movement (bb_movement_name, one_rep_max, user_id) "
                            "VALUES (?, ?, ?)",
                            (movement_name, one_rep_max, user)
                        )
                    con.commit()

                    # Update current values dictionary with the new data
                    current_values[movement_name] = one_rep_max

    except sqlite3.Error as error:
        print("Database error:", error)
        return f"Database Error: {error}"
    finally:
        if con:
            con.close()

    # Render the profile page with the current values
    return render_template("profile.html", current_values=current_values)




# MOVEFORWARD FITNESS TRACKER APP
#### Video Demo https://youtu.be/qcNtY-lDOIc
#### Description:
Fitness Tracker app that stores details of a users workouts in a personal calendar and also providses a resource for workout videos and exercises.

### Languages and libraries:

Pyhton
HTML
CSS
Bootstrap
Calendar.io
Javascript
Flask

### App.py:

The application file is a Python file that contains all the web application routes. The first few routes handle the registration of new users and also also allowing users to login into their own personalised account. These routes handle the necessary validations to ensure each user is unique so they can store their own workouts and profile information. All information is stored and access via a sqlite database and specific queries.

The calendar routes allow the users to record, delete and access their workouts on the calendar/homepage

The exercises and workout routes handle database queries to store and then read data. The information from the database is then passed to the relevant webpage to be shown visually on the page.

Profile route handles the database queries for storing and reading personal information on biometrics and personal bests on certain barbell movements. This was an essential part of the design as ther Crossfit methodology relies on good record keeping to track progress on yout fitness levels

The favourites route is unfinished and was originally going to be a key part of the programme. Unfortunately time did not allow the section to be completed but the code does have the beginnings of a possible future feature of marking and storing your favourite workouts.

### moveforward.db:

A sqlite database was used in this design as the most logical and efficient way to store user data e.g username, user id, hased password and biometrics. It was also ideal for storing exercises and personal bests and for creating connections using foreign keys for the specific user that is logged-in.

### Calendar.html:

This file contains all the HTML, jinja and javascript to display the calendar/homescreen of the fitness app. I utilised an API connection to FullCalendar.io for this part of the project as it provided a great solution for an interactive calendar that works well with the languages I used in for this project. It was a challenging to get the formatting write at the start but once I had got a good grasp of bootstraps features it proved to be a great solution. The javascript was the hardest part and I did have to utilise the readme documents quite alot when writing this page.

### Exercises.html:

From the start of the project I was very keen to include some sort of video library for the user to reference. I had an idea in my head the videos would pop-up on the page so you didn't have to leave the page to watch them. Bootstraps modals were a great solution here and I had learnt how to use them when writing the calendar feature of the app. Once I had got a nice layout I simply linked each image on the page to the video url on youtube so that the videos autopplayed on click using a modal and then stopped once you clicked out of the area. This proved to be quite tricky to begin with as the autoplay didn't work at first but with the help of some code review in ChatGPT I was able to get it working.

### Favourites.html:

This page remains unfinished and is an opportunity for the future state of the app. I really wanted a way to keep track of favourite workouts and this page would then show a consolidated list for quick reference of a workout.

### index.html

Originally this was the homepage and should still be the case. Late in the design I opted to use the calendar page as the homepage and this file was abandoned. A refactoring project would involve moving the calendar code to the index file to improve the file and code structure.

### layout.html:

This page is the master template for the layout of the entire web app and uses Bootstrap and jinja to create a clean layout template that all other pages in the app extend and build upon. The vertical navbar was always in my mind from the start of the project and the idea that each section wopuld be listed here and would change colour or highlight when clicked. This was implemented successfully in the project.

### login.html

This is the first page you see on the app and allowd the user to login with their credentials.

### register.html

This is the registration page for the app and allows a new user to create an account.

### profile.html

This page displays using a table structure the users biometrics e.g. age, height, weight and a calulated BMI aswell as PBs on certain lifts. This page can be extended in a future state as the disign expands to include more PBs and it would make sense to move thes eonto separate pages as more data is added.

### workouts.html

This page shows image references and vido links for the foundationla movements in Crossfit. This page uses the modal feature in bootstap along with some Javascript to popup the relevant video and autoplay it for the user. This page was always in my mind from the beginning of the project.

### helper.py

Stores the session information locally so as not to reply on cookies.

## static folder
Stores the CSS stylesheeta and Assets e.g. images used in the app

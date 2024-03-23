# Documentaion for CS50 final project.

# Name: Sport Meetings
#### Video Demo:https://youtu.be/nud-pWdbkG8

## Introduction
- This flask application is designed for people who wants to participate in a team sport, to help them find a new team in the city there currently at. The application also helps teams in the same way by helping them to find people who wants to play for teams. This application works by taking inputs from users and saving it and configured in a way to make those information available to those who are in need of that information. This application is made by using different programming languges and frameworks. The list of laguges and frameworks that are used are:-
- Sqlite
- Python (flask) 
- Html
- CSS (Bootstraps)
- Installation and set up for this is based on the seminar videos by cs50 about Setting Up Your Local Development Environment.
- Programming languges and frame works that are used in this application are HTML, CSS, PYTHON and FLASK(python framework).

## Files used to make this application
- app.py
- templates/
  - layout.html
  - index.html
  - register.html
  - login.html
  - logout.html
  - teamlist.html
  - playerlist.html
  - set_appointment.html
  - appointments.html
- instance/
- data_meetings.db

## Database schema

The application uses an SQLITE database with the following schema:
- Users: This table has 6 attributes and stores users information like id as the primary key, name, phone, city , hashed password and the type of user.
Relationships:
One-to-Many with Players: One user can have multiple player roles.
One-to-Many with Teams: One user can lead multiple teams.

- Sports: This table stores name of sports
Relationships:
One-to-Many with Players: One sport can have multiple players.
One-to-Many with Teams: One sport can be associated with multiple teams.

- Positons: This table stores names of playing positions.
Relationships:
One-to-Many with Players: One position can have multiple players.
One-to-Many with Teams: One position can be held by multiple teams.

- Players: This table associate user types that Players to their respective sports and positions.
Relationships:
Many-to-One with Users: Many players can belong to one user.
Many-to-One with Sports: Many players can participate in one sport.
Many-to-One with Positions: Many players can occupy one position.

- Teams:  This table associate user types that Teams to their respective sports and positions.
Relationships:
Many-to-One with Users: Many teams can be led by one user.
Many-to-One with Sports: Many teams can participate in one sport.
Many-to-One with Positions: Many teams can have one position.

- Appointments: Stores appointmenst between players and teams.
Relationships:
Many-to-One with Players: Many appointments can involve one player.
Many-to-One with Teams: Many appointments can involve one team.

- PlayerTeam: Represents the association between players and teams in appointments.
Relationships:
Many-to-Many with Players and Teams: Many players can belong to many teams in appointments.

## HTML Files
- index.html

This HTML template file represents the homepage of the application:

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Index".
It contains a paragraph with a welcome message.
The content of this page is inserted into the "main" block of the layout.html template.

- register.html

This is an HTML template file for the registration form.

It extends a base layout file called "layout.html".
It defines a block named "title" where the title of the page is set to "Register".
Within the "main" block, it contains a form for user registration.
The form includes fields for user type, name, phone number, city, password, and password confirmation.
It utilizes Bootstrap classes for styling the form elements.
The form submits data to the "/register" route using the POST method.
Upon submission, it triggers the registration process in the backend.

- login.html

This is an HTML template file for the login form.

It extends a base layout file called "layout.html".
It defines a block named "title" where the title of the page is set to "Login".
Within the "main" block, it contains a form for user login.
The form includes fields for phone number and password.
It utilizes Bootstrap classes for styling the form elements.
The form submits data to the "/login" route using the POST method.
Upon submission, it triggers the login process in the backend.


- sport_position.html

This is an HTML template file for the "sport_position" page.

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Sport_Position".
It contains a form with input fields for "Position" and "Sport".
Users can enter the position and sport details in the respective input fields.
The form is submitted to the "/sport_position" route using the POST method.
Upon submission, the form data is sent to the server for processing.
It includes a "Done" button for submitting the form.
The content of this page is inserted into the "main" block of the layout.html template.

- layout.html

This is an HTML template file for the layout of the web application.

It defines the structure of the HTML document with appropriate tags.
It includes Bootstrap CSS framework for styling.
The title of the page is dynamically set using a block named "title".
It contains a navigation bar with links to various pages based on user authentication status.
If a user is logged in, the navigation bar displays links to different sections like Teams, Players, and Appointments, along with a logout option.
If no user is logged in, the navigation bar displays links to login and registration pages.
Flash messages are displayed at the top of the page if there are any.
The main content of each page is inserted into a block named "main".
The content of the main block varies depending on the specific page being rendered.

- teamlist.html

This is an HTML template file for displaying a list of teams.

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Teams List".
It contains a table with three columns: "Teams", "City", and "Position".
Each row in the table corresponds to a team.
It iterates over the teams data passed from the server and populates the table rows accordingly.
For each team, it displays the team name, city, and position.
It includes a button in each row to set up an appointment with the team.
The form sends a GET request to the "/set_appointment" route with the team name as a parameter when the button is clicked.
The content of this page is inserted into the "main" block of the layout.html template.

- playerlist.html


This HTML template file displays a list of players.

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Player List".
It contains a table with three columns: "Player", "City", and "Position".
Each row in the table corresponds to a player.
It iterates over the players data passed from the server and populates the table rows accordingly.
For each player, it displays the player's name, city, and position.
It includes a button in each row to set up an appointment with the player.
The form sends a GET request to the "/set_appointment" route with the player's name as a parameter when the button is clicked.
The content of this page is inserted into the "main" block of the layout.html template.

- set_appointments.html

This HTML template file is used to set up appointments.

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Setup Appointments".
It contains a form with fields to input the name of the person to meet, the date of the appointment, and the address.
Each field is required and has placeholder text to guide the user.
Upon submission, the form sends a POST request to the "/set_appointment" route.
The content of this page is inserted into the "main" block of the layout.html template.

- appointmentlist.html

This HTML template file displays a list of appointments.

It extends the layout.html file, inheriting its structure and styles.
The title of the page is set to "Appointment List".
It contains a table with columns for the date, address, user name, and user phone for each appointment.
The appointments are iterated through using a for loop, displaying the details of each appointment along with the corresponding user name and phone number.
The content of this page is inserted into the "main" block of the layout.html template.

## app.py

- This Python code imports several modules and libraries needed for building a web application using Flask and SQLAlchemy. Here's a breakdown of each import statement:

os: This module provides a portable way of using operating system-dependent functionality, such as accessing the file system.

SQL: This is likely a module or class from the cs50 library, which provides tools for working with SQL databases.

Flask, flash, redirect, render_template, request, session, url_for: These are various components of the Flask framework used for creating web applications. They include the main Flask class (Flask), functions for flashing messages to the user (flash), redirecting to other routes (redirect), rendering HTML templates (render_template), handling HTTP requests (request), managing user sessions (session), and generating URLs for routes (url_for).

Session: This is likely a class or module from the flask_session library, which provides session management support for Flask applications.

check_password_hash, generate_password_hash: These functions are from the werkzeug.security module and are used for hashing and checking passwords securely.

wraps: This is a decorator from the functools module used for creating decorators that preserve function metadata.

SQLAlchemy: This is an ORM (Object-Relational Mapping) library for Python that provides a high-level interface for interacting with databases using Python objects. The Flask-SQLAlchemy extension integrates SQLAlchemy with Flask, making it easy to use SQLAlchemy within Flask applications.

- This Python code initializes a Flask application (app) and configures it to use SQLAlchemy, an ORM (Object-Relational Mapping) library for interacting with databases.

Flask Application Initialization:

app = Flask(__name__): This creates a Flask application instance. The __name__ variable is a special Python variable that represents the name of the current module. Flask uses this to determine the root path of the application.
Configuration:

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data_meetings.db": This line configures the URI (Uniform Resource Identifier) for the database to be used by SQLAlchemy. In this case, it specifies a SQLite database named data_meetings.db. SQLite is a lightweight, file-based database that does not require a separate server process.
app.config["DEBUG"] = True: This enables debug mode for the Flask application. When debug mode is enabled, the application provides more detailed error messages and automatically reloads when code changes are detected.
SQLAlchemy Initialization:

db = SQLAlchemy(app): This creates an SQLAlchemy object (db) and binds it to the Flask application (app). This allows the application to interact with the database using SQLAlchemy's ORM features.
## Routes and Function with thier Features

### Registration
 - The Flask route "/register" facilitates user registration within the application. 

 GET Method: Renders the "register.html" template, displaying the registration form.
POST Method: Retrieves user input from the registration form.

Validates the input fields:
Checks if all required fields are filled.
Ensures the phone number contains only digits.
Checks if passwords match.
Checks if a user with the provided phone number already exists.
If validation passes:
Hashes the password using generate_password_hash.
Creates a new user object with the provided details.
Adds the new user to the database session.
Commits the session to the database.
Sets session variables for the user ID and user type.
Flashes a success message.
Redirects the user to the "/sport_position" route.
If an error occurs during registration:
Prints the error to the console.
Flashes an error message.
Redirects the user to the homepage ("/").
 
 - User registration form is through registration.html 

 ### Login
 - The code defines a Flask route ("/login") for user authentication.

GET Method: Renders the login form.
POST Method:
Validates form data.
Checks user credentials against the database.
Sets session variables upon successful login.
Redirects users accordingly.
It ensures secure login functionality with input validation and password hashing.

 - User login form is through login.html 

### Logut
- The Flask route "/logout" handles user logout functionality. Upon accessing this route, it clears the session data to log the user out and then redirects them to the homepage ("/"). It provides a simple and effective way for users to securely logout from the application.
 
 ### Sport_Positions

 This Flask route /sport_position allows users to add a new sport and position. Here's a brief explanation of how it works:

Request Method Check: The function first checks if the request method is GET or POST. If it's GET, it renders the "sport_position.html" template, which likely contains a form for users to input the sport and position names.
Form Data Retrieval: If the request method is POST (which means the form has been submitted), the function retrieves the sportname and positionname from the form data submitted by the user.
Input Validation: It checks if both sportname and positionname are provided. If either of them is missing, it flashes a message indicating that all fields are required and redirects the user back to the same page.
Database Operations: It then checks if the provided sport and position already exist in the database. If they don't exist, new entries for the sport and position are created and added to the database.
Relationship Handling: After creating or retrieving the sport and position, the function checks the user's type. If the user is a player, a new entry is created in the "Players" table with the user's ID, sport ID, and position ID. If the user is a team, a new entry is created in the "Teams" table with similar information.
Committing Changes: All changes made to the database are committed using db.session.commit() to ensure they are saved permanently.
Flash Messages: Flash messages are used to provide feedback to the user, indicating whether the operation was successful or if there was an error.
Redirection: Finally, regardless of whether the operation was successful or not, the function redirects the user back to the homepage ("/").

 - sport_position.html provides form to get information from user.

 ### Playerlist and Teamlist

 - Before this funtions are used session is checked and if user type is player layout.html displays option to click on the team and if user type is Team layout.html displays option to click on the player list.

 - layout.html is the file that contains the basic structures of all the other html files. it also display application logo, option to see either team or player list and check appointments and aslo contains link to login ,logout and register.

 - The Flask route ("/playerlist") displays a list of players in the application.

GET Method: Retrieves player data from the database by joining the Users, Players, and Positions tables based on user type ('Player').
POST Method: N/A (Unused in this route).
The @login_required decorator ensures that only authenticated users can access this route.
It first queries the database to retrieve the sport_id of the current user from the "Teams" table table to show lists of players with related sport
Players' information is fetched and stored in the 'players' variable.
If players are found, they are printed to the console; otherwise, a message stating "No results found" is printed.
Renders the "playerlist.html" template, passing the players' data to be displayed.

- The Flask route ("/teamlist") retrieves and displays a list of teams in the application.

GET Method: Fetches team data from the database by joining the Users, Teams, and Positions tables based on user type ('Team').
POST Method: Not utilized in this route.
The @login_required decorator ensures only authenticated users can access this route.
It first queries the database to retrieve the sport_id of the current user from the "Players" table to show lists of teams with related sport
Teams' information is fetched and stored in the 'teams' variable.
If teams are found, they are printed to the console; otherwise, a message stating "No results found" is printed.
Renders the "teamlist.html" template, passing the teams' data to be displayed.

### Set_appointment

- The Flask route ("/set_appointment") allows users to set appointments.

GET Method: Renders the "set_appointment.html" template to display a form for setting appointments.
POST Method: Processes the form data submitted by the user.
Extracts data such as date, address, and name from the form.
Validates the required fields (date and address).
Retrieves the user's type from the session data.
Depending on the user type:
If the user is a player, it creates a new appointment between the player and a team.
If the user is a team, it creates a new appointment between the team and a player.
Commits the changes to the database.
Redirects the user to the homepage ("/").
Utilizes the @login_required decorator to ensure only authenticated users can access this route.
Displays flash messages to provide feedback to the user about the success or failure of the appointment setting process.

### Appointmentlist

- The Flask route ("/appointmentlist") displays a list of appointments.

It is accessible via both GET and POST methods.
Utilizes the @login_required decorator to ensure only authenticated users can access this route.
Depending on the user type stored in the session data:
If the user is a player, it retrieves appointments where the player is involved.
If the user is a team, it retrieves appointments involving the team.
Retrieves the relevant appointments from the database using SQLAlchemy queries.
Joins the Appointments table with the Users table to get additional information about the users involved in the appointments.
Renders the "appointmentlist.html" template, passing the retrieved appointments data to be displayed.

### delete_appointment

Route Definition: This function is mapped to the "/delete_appointment" route and accepts POST requests.
Login Required: The @login_required decorator ensures that the user must be logged in to access this endpoint.
Request Data: It retrieves the date and address of the appointment to be deleted from the form data submitted with the request.
Query Appointment: It queries the database to find the appointment with the specified date and address using the Appointments.query.filter_by(date=date, address=address).first() method.
Check Existence: If no appointment is found with the given date and address, it flashes a message indicating that the appointment was not found and redirects the user to the appointment list page.
Delete Appointment: If the appointment is found, it is deleted from the database using db.session.delete(appointment).
Commit Changes: The changes made (deleting the appointment) are committed to the database using db.session.commit().
Flash Message: A message indicating the successful deletion of the appointment is flashed.
Redirect: Finally, the user is redirected to the appointment list page.

### login_required

The login_required decorator is a function that takes another function (f) as its argument and returns a new function (decorated_function). This decorator is commonly used in web applications to restrict access to certain routes or views only to authenticated users.

The wraps function from the functools module is used to preserve the metadata of the original function (f), such as its name and docstring.
Inside the decorated_function, it checks if the user is logged in by verifying if the "user_id" key exists in the session. If it does not exist (i.e., the user is not logged in), the user is redirected to the login page ("/login").
If the user is logged in (i.e., the "user_id" key exists in the session), the original function (f) is called with the provided arguments and keyword arguments (*args and **kwargs).
The decorated_function is then returned, which effectively replaces the original function (f) wherever the login_required decorator is used.

### after_request

The after_request function is a callback function in Flask that allows you to modify the response object after it has been constructed but before it is sent to the client. In this case, it is used to ensure that responses from the server are not cached by the client's browser or any intermediary caches.

It takes a response object as input.
It modifies the response headers to include directives that instruct the client's browser not to cache the response.
Specifically, it sets the following headers:
"Cache-Control": Specifies caching directives that must be obeyed by all caches along the request/response chain.
"Expires": Sets an expiration date of 0, indicating that the response should not be considered fresh.
"Pragma": Specifies additional cache-control directives for clients and proxies.
Finally, it returns the modified response object.

## I have used Chat gpt and github copilot as a helping tools. 
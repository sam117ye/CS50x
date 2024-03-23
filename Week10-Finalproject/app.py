import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data_meetings.db"
app.config["DEBUG"] = True


db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)

class Sports(db.Model):
    __tablename__ = 'Sports'
    id = db.Column(db.Integer, primary_key=True)
    sportname = db.Column(db.String, nullable=False)

class Positions(db.Model):
    __tablename__ = 'Positions'
    id = db.Column(db.Integer, primary_key=True)
    positionname = db.Column(db.String, nullable=False)

class Players(db.Model):
    __tablename__ = 'Players'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('Sports.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('Positions.id'))

class Teams(db.Model):
    __tablename__ = 'Teams'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('Sports.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('Positions.id'))

class Appointments(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('Players.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.id'))
    date = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

class PlayerTeam(db.Model):
    __tablename__ = 'PlayerTeam'
    player_id = db.Column(db.Integer, db.ForeignKey('Players.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Teams.id'), primary_key=True)

with app.app_context():
        db.create_all()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html") 
    else:

        name = request.form.get("name")
        phone = request.form.get("phone")
        city = request.form.get("city")
        user_type = request.form.get("user_type")


        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not name or not phone or not city or not user_type or not password or not confirmation:
            flash("All fields are required")
            return redirect("/register")
        
        if phone.isdigit() == False:
            flash("Phone number should contain only digits")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords do not match")
            return redirect("/register")
        
        existing_user = Users.query.filter_by(phone=phone).first()
        if existing_user:
            flash("User with this phone number already exists")
            return redirect("/register")
        
        hash = generate_password_hash(password)

        try:
            new_user = Users(name=name, phone=phone, city=city, hash=hash, user_type=user_type)
            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            session["user_type"] = user_type

            flash("Registered successfully")

            return redirect("/sport_position")

        except Exception as e:
            print(e)
            flash("error: " + str(e))
        
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")

        if not phone or not password:
            flash("All fields are required")
            return redirect("/login")

        user = Users.query.filter_by(phone=phone).first()

        if not user or not check_password_hash(user.hash, password):
            flash("Invalid phone number and/or password")
            return redirect("/login")

        session["user_id"] = user.id
        session["user_type"] = user.user_type

        flash("Logged in successfully")

        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/sport_position", methods=["GET", "POST"])
@login_required
def sport_position():
    if request.method == "GET":
        return render_template("sport_position.html")
    else:
        sportname = request.form.get("sportname")
        positionname = request.form.get("positionname")
        
        if not sportname or not positionname:
            flash("All fields are required")
            return redirect("/sport_position")

        try:
            # Check if sport and position already exist
            sport = Sports.query.filter_by(sportname=sportname).first()
            position = Positions.query.filter_by(positionname=positionname).first()

            # If they don't exist, create new ones
            if not sport:
                sport = Sports(sportname=sportname)
                db.session.add(sport)
            if not position:
                position = Positions(positionname=positionname)
                db.session.add(position)

            db.session.commit()

            # After creating or getting the sport and position, check the user_type
            if session["user_type"] == "Player":
                # Create a new Player entry with the user's id, sport id, and position id
                new_player = Players(user_id=session["user_id"], sport_id=sport.id, position_id=position.id)
                db.session.add(new_player)
            elif session["user_type"] == "Team":
                # Create a new Team entry with the user's id, sport id, and position id
                new_team = Teams(user_id=session["user_id"], sport_id=sport.id, position_id=position.id)
                db.session.add(new_team)

            db.session.commit()

            flash("Sport and position added successfully")

        except Exception as e:
            print(e)
            flash("error: " + str(e))

        return redirect("/")
    
@app.route("/playerlist", methods=["GET", "POST"])
@login_required
def playerlist():

    # Query the database for sport_id same as the current user's sport_id
    sportid = db.session.query(Teams.sport_id).filter(Teams.user_id == session['user_id']).first()
    city = db.session.query(Users.city).filter(Users.id == session['user_id']).first()

    if sportid or city:
        sportid = sportid[0]
        city = city[0]
        # Query the database for all name, city and positionname of users with the same sport id as the current user and user_type = 'Player'
        players = db.session.query(Users.name, Users.city).\
            join(Players, Users.id == Players.user_id).\
            filter(Players.sport_id == sportid, Users.city == city, Users.user_type == 'Player').all()

        if players:
            print(players)  # print players to the console
        else:
            print("No results found")

        return render_template("playerlist.html", players=players)
    else:
        flash("No sport found for the current user")
        return redirect("/")

@app.route("/teamlist", methods=["GET", "POST"])
@login_required
def teamlist():
    # Get the sport id of the current user
    current_user_sport_id = db.session.query(Players.sport_id).filter(Players.user_id == session['user_id']).first()
    city = db.session.query(Users.city).filter(Users.id == session['user_id']).first()

    if current_user_sport_id or city:
        current_user_sport_id = current_user_sport_id[0]
        city = city[0]

        # Query the database for all name, city of users with the same sport id as the current user and user_type = 'Team'
        teams = db.session.query(Users.name, Users.city).\
           join(Teams, Users.id == Teams.user_id).\
           filter(Teams.sport_id == current_user_sport_id, Users.city == city, Users.user_type == 'Team').all()
        
        if teams:
            print(teams)  # print teams to the console
        else:
            print("No results found")

        return render_template("teamlist.html", teams=teams)
    else:
        flash("No sport found for the current user")
        return redirect("/")

@app.route("/set_appointment", methods=["GET", "POST"])
@login_required
def set_appointment():
    if request.method == "GET":
        return render_template("set_appointment.html")
    else:
        date = request.form.get("date")
        address = request.form.get("address")
        name = request.form.get("name")

        if not date or not address:
            flash("All fields are required")
            return redirect("/set_appointment")
        
        try:
            if session["user_type"] == "Player":
                player = Players.query.filter_by(user_id=session["user_id"]).first()
                user = Users.query.filter_by(name=name).first()
                if user:
                    team = Teams.query.filter_by(user_id=user.id).first()
                    if team:
                        new_player_appointment = Appointments(player_id=player.id, team_id=team.id, date=date, address=address)
                        db.session.add(new_player_appointment)
                        flash("Appointment set successfully")
                    else:
                        flash("Team not found")
                else:
                    flash("User not found")
                    
            elif session["user_type"] == "Team":
                team = Teams.query.filter_by(user_id=session["user_id"]).first()
                user = Users.query.filter_by(name=name).first()
                if user:
                    player = Players.query.filter_by(user_id=user.id).first()
                    if player:
                        new_team_appointment = Appointments(team_id=team.id, player_id=player.id, date=date, address=address)
                        db.session.add(new_team_appointment)
                        flash("Appointment set successfully")
                    else:
                        flash("Player not found")
                else:
                    flash("User not found")

            db.session.commit()
        except Exception as e:
            print(e)
            flash("error: " + str(e))

        return redirect("/appointmentlist")

@app.route("/appointmentlist", methods=["GET", "POST"])
@login_required
def appointmentlist():
    if session["user_type"] == "Player":
        player = Players.query.filter_by(user_id=session["user_id"]).first()
        appointments = db.session.query(Appointments, Users.name, Users.phone).\
            join(Teams, Teams.id == Appointments.team_id).\
            join(Users, Users.id == Teams.user_id).\
            filter(Appointments.player_id == player.id).all()
    elif session["user_type"] == "Team":
        team = Teams.query.filter_by(user_id=session["user_id"]).first()
        appointments = db.session.query(Appointments, Users.name, Users.phone).\
            join(Players, Players.id == Appointments.player_id).\
            join(Users, Users.id == Players.user_id).\
            filter(Appointments.team_id == team.id).all()
    return render_template("appointmentlist.html", appointments=appointments)

@app.route('/delete_appointment', methods=['POST'])
@login_required
def delete_appointment():
    # Get the name and date from the form data
    date = request.form.get('date')
    address = request.form.get('address')

    # Query the appointment you want to delete
    appointment = Appointments.query.filter_by(date=date, address=address).first()

    if not appointment:
        flash("Appointment not found")
        return redirect(url_for('appointmentlist'))

    # Delete the appointment
    db.session.delete(appointment)

    # Commit the changes to the database
    db.session.commit()

    flash("Appointment deleted successfully")
    return redirect('/appointmentlist')
        
    
if __name__ == "__main__":
    app.run(debug=True)

#I have used the help of chat gpt and github copilot to write the code.
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from flask import request

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    data_db = db.execute("select symbol, sum(shares) as shares, price from transactions where user_id = ? group by symbol", user_id)
    cash_db = db.execute("select cash from users where id = ?", user_id)
    cash = cash_db[0]["cash"]

    total = cash

    for row in data_db:
        stock_info = lookup(row["symbol"])
        if stock_info:
            row["price"] = stock_info["price"]
            row["total_value"] = row["shares"] * stock_info["price"]
            total += row["total_value"]
        else:
            return apology("symbol doesn't exist")

    return render_template('index.html', data=data_db, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method =="GET":
        return render_template("buy.html")

    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must give symbol")

        shares = int(request.form.get("shares"))
        if shares < 0:
            return apology("invalid shares")

        stock = lookup(symbol.upper())
        if stock == None:
            return apology("symbol doesn't exsist")

        transaction_cost = int(shares) * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("select cash from users where id= :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_cost:
            return apology("account insufficient")

        updated_cash = user_cash - transaction_cost

        db.execute("update users set cash = ? where id = ?",updated_cash, user_id )

        date = datetime.datetime.now()

        db.execute("insert into transactions (user_id, symbol, shares, price, date) values (?, ?, ?, ?, ?)",
                    user_id, stock["symbol"], int(shares), stock["price"], date)

        flash("Success!")
        return redirect("/")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    data_db = db.execute("select * from transactions where user_id = :id", id=user_id)

    return render_template('history.html', data=data_db,)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")

    symbol = request.form.get("symbol")

    if not symbol:
        return apology("Must give symbol")

    quoted_stock = lookup(symbol.upper())

    if quoted_stock == None:
        return apology("symbol not found:(")

    return render_template("quoted.html",price = quoted_stock["price"], symbol = quoted_stock["symbol"])

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:

        username = request.form.get("username")
        if not username:
            return apology("Provide username")

        password = request.form.get("password")
        if not password:
            return apology("Provide password")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("rewrite password")
        if password != confirmation:
            return apology("password dont match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("insert into users (username, hash) values (?, ?)", username, hash)
        except:
            return apology("username already exists")

        session["user_id"] = new_user

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute("select symbol from transactions where user_id = :id group by symbol having sum(shares) > 0", id=user_id)
        return render_template ("sell.html", symbols = [row["symbol"] for row in symbols_user])

    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must give symbol")

        shares = int(request.form.get("shares"))
        if shares <= 0:
            return apology("invalid shares")


        stock = lookup(symbol.upper())
        if stock == None:
            return apology("symbol doesn't exsist")

        transaction_cost = int(shares) * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("select cash from users where id= :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute("select shares from transactions where user_id= :id and symbol = :symbol group by symbol", id=user_id, symbol=symbol)
        user_shares_real = user_shares[0]["shares"]

        if shares > user_shares_real:
            return apology("you dont have enough")

        updated_cash = user_cash + transaction_cost

        db.execute("update users set cash = ? where id = ?",updated_cash, user_id )

        date = datetime.datetime.now()

        db.execute("insert into transactions (user_id, symbol, shares, price, date) values (?, ?, ?, ?, ?)",
                    user_id, stock["symbol"], (-1) * shares, stock["price"], date)

        flash("Success!")
        return redirect("/")


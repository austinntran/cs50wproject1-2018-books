import os, re, requests
from flask import Flask, session, render_template, jsonify, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return redirect("/home")


@app.route("/home")
def index():
    if session.get("user_id") is None:
        loggedIn = False
    else:
        loggedIn = True
    return render_template("index.html", loggedIn=loggedIn)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("login.html")
        else:
            return redirect("/search")
    elif request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        # password_hash = generate_password_hash(password)
        # check if user exists
        user_sql = db.execute("SELECT * FROM users WHERE username = :user", {"user": user}).fetchone()
        if user_sql is None:
            # eliminate race condition if user doesn't exist
            fake_hash = generate_password_hash("thisisafakehash")
            test = check_password_hash(fake_hash, password)
            return render_template("login.html", type="error", message="The username or password you have entered is invalid.")
        else:
            # validate password

            test = check_password_hash(user_sql[2], password)
            if test:
                session["user_id"] = user_sql[0]
                session["username"] = user_sql[1]
                return redirect("/search")
            else:
                return render_template("login.html", type="error", message="The username or password you have entered is invalid.")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        if session.get("user_id") is None:
            return render_template("register.html")
        else:
            return redirect("/search")
    elif request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")
        if not(re.match("^[a-zA-Z0-9_.-]+$", user) and re.match(r'[A-Za-z0-9@#$%^&+=\!]{8,}', password)):
            return render_template("register.html", type="error", message="Username or password is invalid")
        user_exist = db.execute("SELECT * FROM users WHERE username = :user", {"user": user}).fetchone()
        if user_exist is None:
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)", {"username": user, "password_hash": password_hash})
            db.commit()
            return render_template("login.html", type="success", message="Account was successfully created!")
        else:
            return render_template("register.html", type="error", message="Username or password you have entered is invalid or taken.")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")


@app.route("/search", methods=["GET","POST"])
def search():
    if session.get("user_id") is None:
        return redirect("/login")
    if request.method == "GET":
        return render_template("search.html", loggedIn=True)
    elif request.method == "POST":
        post = request.form.get("item")
        item = '%' + post.capitalize() + '%'
        rows = db.execute("SELECT * FROM books WHERE isbn LIKE :item or title LIKE :item or author LIKE :item", {"item": item}).fetchall()
        # res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "Z9EerpBcRErsobbjgfc9g", "q": "Betrayal", "search[field]": "all"})
        # if res.status_code != 200:
        #     raise Exception("ERROR: API request unsuccessful.")
        # return res.content# render_template("search.html", loggedIn=True)
        return render_template("search.html", loggedIn=True, books=rows)


@app.route("/book/<title>")
def book(title):
    return title

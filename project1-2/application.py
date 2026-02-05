import os

from flask import Flask, session, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker

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
def index():
    if "user_id" in session:
        return "You are logged in as {}".format(session["user_id"])
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # POST request
    username = request.form.get("username")
    password = request.form.get("password")

    # Insert user into database
    db.execute(
        text("INSERT INTO users (username, password) VALUES (:u, :p)"),
        {"u": username, "p": password}
    )
    db.commit()

    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    user = db.execute(
        text("SELECT id, password FROM users WHERE username = :u"),
        {"u": username}
    ).fetchone()

    if user is None or user.password != password:
        return "Invalid username or password"

    session["user_id"] = username
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


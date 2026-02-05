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
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("search"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = db.execute(
            text("SELECT id FROM users WHERE username = :u"),
            {"u": username}
        ).fetchone()

        if existing_user:
            error = "Username already exists"
        else:
            db.execute(
                text("INSERT INTO users (username, password) VALUES (:u, :p)"),
                {"u": username, "p": password}
            )
            db.commit()

            user = db.execute(
                text("SELECT id FROM users WHERE username = :u"),
                {"u": username}
            ).fetchone()

            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.execute(
            text("SELECT id, password FROM users WHERE username = :u"),
            {"u": username}
        ).fetchone()

        if user is None or user.password != password:
            error = "Invalid username or password"
        else:
            session["user_id"] = user.id
            return redirect(url_for("index"))

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.execute(
        text("SELECT username FROM users WHERE id = :id"),
        {"id": session["user_id"]}
    ).fetchone()

    if request.method == "GET":
        return render_template("search.html", books=None, username=user.username)

    query = request.form.get("query")

    books = db.execute(
        text("""
            SELECT * FROM books
            WHERE isbn ILIKE :q
               OR title ILIKE :q
               OR author ILIKE :q
        """),
        {"q": f"%{query}%"}
    ).fetchall()

    return render_template("search.html", books=books, username=user.username)

@app.route("/book/<string:isbn>")
def book(isbn):
    if "user_id" not in session:
        return redirect(url_for("login"))

    book = db.execute(
        text("SELECT * FROM books WHERE isbn = :isbn"),
        {"isbn": isbn}
    ).fetchone()

    if book is None:
        return "Book not found", 404

    user = db.execute(
        text("SELECT username FROM users WHERE id = :id"),
        {"id": session["user_id"]}
    ).fetchone()

    return render_template(
        "book.html",
        book=book,
        username=user.username
    )


import os
import requests
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

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get book info
    book = db.execute(
        text("SELECT * FROM books WHERE isbn = :isbn"),
        {"isbn": isbn}
    ).fetchone()

    if book is None:
        return "Book not found", 404

    google_data = None
    google_average = None
    google_count = None
    google_description = None

    res = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": f"isbn:{isbn}"}
    )

    if res.status_code == 200:
        data = res.json()

        if data["totalItems"] > 0:
            volume_info = data["items"][0]["volumeInfo"]

            google_average = volume_info.get("averageRating")
            google_count = volume_info.get("ratingsCount")
            google_description = volume_info.get("description")

    gemini_summary = None

    gemini_summary = None

    if google_description:
        api_key = os.getenv("GEMINI_API_KEY")

        # Use the correct Gemini model URL
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

        # Payload for summarization
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Summarize this text using less than 50 words:\n\n{google_description}"
                }]
            }]
        }

        try:
            # Send POST request with API key as a query parameter
            response = requests.post(
                gemini_url,
                params={"key": api_key},  # <-- API key goes here
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            print("Gemini status:", response.status_code)
            print("Gemini response:", response.text)

            if response.status_code == 200:
                result = response.json()
                gemini_summary = result["candidates"][0]["content"]["parts"][0]["text"]

            else:
                gemini_summary = "No summary available."
                print("Gemini API error:", response.text)

        except Exception as e:
            gemini_summary = "No summary available."
            print("Exception calling Gemini API:", str(e))

    reviews = db.execute(
        text("""
                    SELECT users.username, reviews.rating, reviews.review
                    FROM reviews
                    JOIN users ON reviews.user_id = users.id
                    WHERE reviews. book_isbn = :isbn
                    ORDER BY reviews.id DESC
                """),
        {"isbn": isbn}
    ).fetchall()

    user_review = db.execute(
        text("""
            SELECT id FROM reviews
            WHERE user_id = :user_id AND book_isbn = :isbn
        """),
        {"user_id": session["user_id"], "isbn": isbn}
    ).fetchone()

    already_reviewed = user_review is not None

    # Handle review submission
    if request.method == "POST":
        rating = request.form.get("rating")
        review_text = request.form.get("review")
        user_id = session["user_id"]

        # Check if user already reviewed this book
        existing = db.execute(
            text("SELECT * FROM reviews WHERE user_id = :user_id AND book_isbn = :isbn"),
            {"user_id": user_id, "isbn": isbn}
        ).fetchone()

        if existing:
            error = "You have already submitted a review for this book."
            user = db.execute(
                text("SELECT username FROM users WHERE id = :id"),
                {"id": session["user_id"]}
            ).fetchone()

            return render_template(
                "book.html",
                book=book,
                username=user.username,
                error=error,
                success = None,
                reviews = reviews,
                already_reviewed = already_reviewed,
                google_average = google_average,
                google_count = google_count,
                google_description = google_description,
                gemini_summary=gemini_summary
            )

        # Insert review
        db.execute(
            text("""
                INSERT INTO reviews (user_id, book_isbn, rating, review)
                VALUES (:user_id, :isbn, :rating, :review)
            """),
            {
                "user_id": user_id,
                "isbn": isbn,
                "rating": rating,
                "review": review_text
            }
        )
        db.commit()

        return redirect(url_for("book", isbn=isbn, success=1))

    # Get username
    user = db.execute(
        text("SELECT username FROM users WHERE id = :id"),
        {"id": session["user_id"]}
    ).fetchone()

    success = None
    if request.args.get("success"):
        success = "Your review has been submitted successfully."


    return render_template(
        "book.html",
        book=book,
        username=user.username,
        error=None,
        success=success,
        reviews=reviews,
        already_reviewed=already_reviewed,
        google_average = google_average,
        google_count = google_count,
        google_description = google_description,
        gemini_summary=gemini_summary

    )

from flask import jsonify

@app.route("/api/<string:isbn>", methods=["GET"])
def api_book(isbn):
    # Get book from database
    book = db.execute(
        text("SELECT * FROM books WHERE isbn = :isbn"),
        {"isbn": isbn}
    ).fetchone()

    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Get reviews count and average rating from database
    review_data = db.execute(
        text("""
            SELECT COUNT(*) AS review_count, 
                   AVG(rating) AS average_rating
            FROM reviews
            WHERE book_isbn = :isbn
        """),
        {"isbn": isbn}
    ).fetchone()

    review_count = review_data.review_count if review_data.review_count else 0
    avg_rating_db = float(review_data.average_rating) if review_data.average_rating else None

    # Fetch Google Books API data
    google_average = None
    google_description = None
    res = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": f"isbn:{isbn}"}
    )
    if res.status_code == 200:
        data = res.json()
        if data["totalItems"] > 0:
            volume_info = data["items"][0]["volumeInfo"]
            google_average = volume_info.get("averageRating")
            google_description = volume_info.get("description")

    # Fetch Gemini summary if description exists
    gemini_summary = None
    if google_description:
        api_key = os.getenv("GEMINI_API_KEY")
        gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        payload = {
            "contents": [{"parts":[{"text": f"Summarize this text using less than 50 words:\n\n{google_description}"}]}]
        }
        response = requests.post(
            gemini_url,
            params={"key": api_key},
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
            gemini_summary = result["candidates"][0]["content"]["parts"][0].get("text")

    # Build JSON response
    json_data = {
        "title": book.title or None,
        "author": book.author or None,
        "publishedDate": book.year or None,
        "ISBN_10": book.isbn or None,
        "ISBN_13": None,  # Add logic if you have ISBN13 in DB
        "reviewCount": review_count,
        "averageRating": google_average if google_average is not None else avg_rating_db,
        "summarizedDescription": gemini_summary
    }

    return jsonify(json_data)

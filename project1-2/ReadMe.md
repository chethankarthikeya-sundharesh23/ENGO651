# ENGO 651 -- Project 1: Books Web Application

This project is a Flask-based web application developed for ENGO 651.

The application allows users to: - Register and log in - Search for
books - View detailed book information - Submit reviews (1--5 rating +
text) - View Google Books data - View AI-generated book summaries
(Google Gemini) - Access book data through a JSON API endpoint

The application uses PostgreSQL for data storage and raw SQL queries via
SQLAlchemy Core (no ORM used).

------------------------------------------------------------------------

## Features

### User Authentication

-   User registration (unique usernames enforced)
-   Login and logout functionality
-   Session management using Flask

### Book Search

-   Search by ISBN, title, or author
-   Partial and case-insensitive search
-   Clickable results linking to detailed book pages

### Book Detail Page

Each book page displays: - Title - Author - Publication year - ISBN -
All user reviews - Average rating and total rating count from Google
Books API (if available) - Full description from Google Books API (if
available) - AI-generated summarized description (less than 50 words)
using Google Gemini API

### Review Submission

-   Users can submit:
    -   Rating (1--5 scale)
    -   Text review
-   Users cannot submit multiple reviews for the same book
-   Review count and average rating are calculated using raw SQL queries

### API Access

A GET request to:

/api/`<isbn>`{=html}

Returns a JSON response containing:

{ "title": "...", "author": "...", "publishedDate": "...", "ISBN_10":
"...", "ISBN_13": "...", "reviewCount": 0, "averageRating": 0,
"summarizedDescription": "..." }

-   If a field is unavailable, null is returned.
-   If the ISBN is not found in the database, the route returns 404.
-   The route uses raw SQL for database queries.

------------------------------------------------------------------------

## Technologies Used

-   Python 3
-   Flask
-   PostgreSQL
-   SQLAlchemy Core (raw SQL only)
-   Requests
-   HTML & CSS
-   Google Books API
-   Google Gemini API

------------------------------------------------------------------------

## File Descriptions

### input.py

Used for initial database population. - Connects to PostgreSQL - Reads
books from a CSV file - Inserts records into the books table

### application.py

Main Flask application file. - App configuration - Session handling -
Database connection - All routing logic - Google Books API integration -
Gemini API summarization - JSON API route (/api/`<isbn>`{=html})

All database queries use raw SQL via db.execute().

### templates/

-   layout.html -- Base template
-   login.html -- Login page
-   register.html -- Registration page
-   search.html -- Search page
-   book.html -- Book detail page with reviews and summary

------------------------------------------------------------------------

## Environment Variables

Before running the app, set:

Windows (PowerShell):

\$env:DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
\$env:FLASK_APP="application.py" \$env:FLASK_DEBUG="1"
\$env:GEMINI_API_KEY="your_api_key_here"

macOS/Linux:

export
DATABASE_URL="postgresql://username:password@localhost:5432/dbname"
export FLASK_APP="application.py" export FLASK_DEBUG=1 export
GEMINI_API_KEY="your_api_key_here"

------------------------------------------------------------------------

## Running the Application

1.  Install dependencies: pip install -r requirements.txt

2.  Run the app: flask run

3.  Open: http://127.0.0.1:5000

------------------------------------------------------------------------

## Notes

-   Google Books data may not be available for all ISBNs.
-   Gemini summaries are generated dynamically.
-   All project requirements are implemented using raw SQL as required.

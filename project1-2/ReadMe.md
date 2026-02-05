# ENGO 651 – Project 1: Books Web Application

This project is a Flask-based web application developed for **ENGO 651**.  
It allows users to register, log in, search for books, and view detailed information about each book.  
The application uses **PostgreSQL** for data storage and **raw SQL queries** via SQLAlchemy.

---

## Features

- User registration with username and password
- User login and logout using Flask sessions
- Import books from a CSV file into the database
- Search for books by **ISBN, title, or author** (partial and case-insensitive)
- Clickable search results that lead to a **book detail page**
- Clean and modern user interface using HTML and CSS
- PostgreSQL database connection using `DATABASE_URL`

---

## Technologies Used

- Python 3
- Flask
- PostgreSQL
- SQLAlchemy (Core / raw SQL, not ORM)
- HTML & CSS

---

## File Descriptions
### `input.py`
The `input.py` script is responsible for **initial database population**.  
It reads book data (from a CSV file) and inserts it into the `books` table in PostgreSQL.

This file is **run once**, before launching the Flask application, to ensure the database contains book records that users can search.

**Responsibilities of `input.py`:**
- Connects to the PostgreSQL database
- Reads book data from a CSV file
- Inserts records into the `books` table
- Ensures data integrity during import

**Why this file is important:**
- Separates **data ingestion** from **web application logic**
- Keeps `application.py` focused on routing and user interaction
- Demonstrates proper backend data handling

### `application.py`
The main Flask application file. It:
- Initializes the Flask app
- Configures session handling
- Connects to the PostgreSQL database
- Defines all routes and application logic

**Main routes:**
- `/register` – Register a new user
- `/login` – User login
- `/logout` – User logout
- `/search` – Book search page
- `/book/<isbn>` – Book detail page

---

### `templates/layout.html`
Defines the base HTML layout using **Jinja2 template inheritance**.  
All other pages extend this file to ensure:
- Consistent navigation bar
- Shared styling
- Cleaner and more maintainable code

Includes:
- Navigation bar
- Page container
- Embedded CSS styles
- `{% block title %}` and `{% block content %}`

---

### `templates/login.html`
- Extends `layout.html`
- Displays login form
- Shows error messages for invalid credentials
- Redirects authenticated users to the search page

---

### `templates/register.html`
- Extends `layout.html`
- Allows users to create an account
- Prevents duplicate usernames
- Automatically logs the user in after registration

---

### `templates/search.html`
- Extends `layout.html`
- Displays a book search form
- Shows search results dynamically
- Links each result to its book detail page

---

### `templates/book.html`
- Extends `layout.html`
- Displays detailed information for a selected book
- Provides navigation back to the search page






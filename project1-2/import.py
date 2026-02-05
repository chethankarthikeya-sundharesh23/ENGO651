import csv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

with open('pass.txt') as f:
    password = f.readline().strip()
# Set up database connection
DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/ENGO651"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("books.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row

        for isbn, title, author, year in reader:
            db.execute(
                text(
                    "INSERT INTO books (isbn, title, author, year) "
                    "VALUES (:isbn, :title, :author, :year)"
                ),
                {
                    "isbn": isbn,
                    "title": title,
                    "author": author,
                    "year": int(year)
                }
            )

        db.commit()
        print("Books imported successfully.")

if __name__ == "__main__":
    main()


from flask import Flask, render_template, request
import mysql.connector
import settings

app = Flask(__name__)


# DB Connection
def get_db_connection():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )

# DB Create
def create_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
    connection.commit()
    cursor.close()
    connection.close()

# Table Create
def create_books_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"USE {settings.DB_NAME}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            pages INT NOT NULL,
            published_year INT NOT NULL
        )
    """)
    connection.commit()

    cursor.close()
    connection.close()


def insert_book(title, author, pages, published_year):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"USE {settings.DB_NAME}")
    cursor.execute("""
        INSERT INTO books (title, author, pages, published_year)
        VALUES (%s, %s, %s, %s)
    """, (title, author, pages, published_year))
    connection.commit()

    cursor.close()
    connection.close()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Add Book Page
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        form = request.form
        
        title = form.get('title')
        author = form.get('author')
        pages = int(form.get('pages', 0))
        published_year = int(form.get('published_year', 2000))

        insert_book(
            title,
            author,
            pages,
            published_year
        )

    return render_template('add_book.html')

if __name__ == '__main__':
    # Dastur ishga tushishidan oldin database va table yaratish
    create_database()
    create_books_table()

    # Flask serverni ishga tushirish
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )

import mysql.connector
import settings

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


def get_books():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(f"USE {settings.DB_NAME}")
    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    cursor.close()
    connection.close()

    return books
    
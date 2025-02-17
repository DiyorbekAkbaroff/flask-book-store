
from flask import Flask, render_template, request
import settings
from db import create_database, create_books_table, insert_book, get_books

app = Flask(__name__)

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

# Get all books
@app.route('/books')
def books_page():
    books = get_books()

    return render_template('books.html', books=books)

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

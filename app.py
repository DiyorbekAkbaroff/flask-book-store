
import hashlib

from flask import Flask, render_template, request, redirect, url_for, flash
import settings
from db import create_database, create_books_table, insert_book, get_books, create_users_table, insert_user, get_user


app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        form = request.form 
        
        username = form['username']
        email = form['email']
        password = form['password']
        confirm_password = form['confirm_password']

        if password != confirm_password:
            flash('Password xato.')
            return render_template('register.html')


        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        insert_user(username, email, hashed_password)

        return redirect(url_for('login'))


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        form = request.form 
        
        email = form['email']
        password = form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = get_user(email, hashed_password)

        if not user:
            flash("User topilmadi.")
            return redirect(url_for('login'))

        return redirect(url_for('home'))


if __name__ == '__main__':
    # Dastur ishga tushishidan oldin database va table yaratish
    create_database()
    create_books_table()
    create_users_table()


    # Flask serverni ishga tushirish
    app.run(
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG
    )

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="bookreviewsdb",
        user="postgres",
        password="Ashu123",
        host="localhost",
        port = "5433"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM books ORDER BY id DESC')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cur.fetchone()

    cur.execute('SELECT * FROM reviews WHERE book_id = %s ORDER BY id DESC', (book_id,))
    reviews = cur.fetchall()

    cur.close()
    conn.close()

    if book is None:
        return "Book not found", 404

    return render_template('book_detail.html', book=book, reviews=reviews)

@app.route('/add_book', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        if not title or not author:
            return "Title and Author are required!", 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (title, author))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/add_review/<int:book_id>', methods=('POST',))
def add_review(book_id):
    review_text = request.form['review_text']

    if not review_text:
        return "Review text is required!", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO reviews (book_id, review_text) VALUES (%s, %s)', (book_id, review_text))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('book_detail', book_id=book_id))

if __name__ == '__main__':
    app.run(debug=True)

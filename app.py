from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

DATABASE = 'library.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create books table
        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                category TEXT,
                description TEXT,
                available INTEGER DEFAULT 1
            )
        ''')

        # Create reservations table
        cursor.execute('''
            CREATE TABLE reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                reservation_date TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')

        # Insert sample books
        sample_books = [
            ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 'A gripping tale of racial injustice and childhood innocence.', 1),
            ('1984', 'George Orwell', '978-0-452-28423-4', 'Fiction', 'A dystopian social science fiction novel.', 1),
            ('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 'Romance', 'A romantic novel of manners.', 1),
            ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 'A story of the Jazz Age.', 1),
            ('Moby-Dick', 'Herman Melville', '978-0-14-243724-7', 'Adventure', 'The saga of Captain Ahab.', 1),
            ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', '978-0-7475-3269-9', 'Fantasy', 'A young wizard\'s journey begins.', 1),
            ('The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 'A fantasy adventure of Bilbo Baggins.', 1),
            ('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 'Fiction', 'The story of teenage rebellion.', 1),
            ('The Lord of the Rings', 'J.R.R. Tolkien', '978-0-618-57498-4', 'Fantasy', 'An epic high-fantasy novel.', 1),
            ('Animal Farm', 'George Orwell', '978-0-452-28424-1', 'Fiction', 'A satirical allegorical novella.', 1),
            ('Brave New World', 'Aldous Huxley', '978-0-06-085052-4', 'Science Fiction', 'A dystopian novel set in a futuristic society.', 1),
            ('The Chronicles of Narnia', 'C.S. Lewis', '978-0-06-023481-4', 'Fantasy', 'A series of seven fantasy novels.', 1)
        ]

        cursor.executemany('''
            INSERT INTO books (title, author, isbn, category, description, available)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_books)

        conn.commit()
        conn.close()
        print("Database initialized with sample books!")

# Initialize database on startup
init_db()

# Serve the main HTML page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# API Routes
@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book:
        return jsonify(dict(book))
    return jsonify({'error': 'Book not found'}), 404

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    conn = get_db_connection()
    reservations = conn.execute('''
        SELECT r.*, b.title, b.author
        FROM reservations r
        JOIN books b ON r.book_id = b.id
        ORDER BY r.reservation_date DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(res) for res in reservations])

@app.route('/api/reserve', methods=['POST'])
def reserve_book():
    data = request.json
    book_id = data.get('book_id')
    user_name = data.get('user_name')
    user_email = data.get('user_email')

    if not all([book_id, user_name, user_email]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()

    # Check if book is available
    book = conn.execute('SELECT * FROM books WHERE id = ? AND available = 1', (book_id,)).fetchone()
    if not book:
        conn.close()
        return jsonify({'error': 'Book not available'}), 400

    # Create reservation
    reservation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute('''
        INSERT INTO reservations (book_id, user_name, user_email, reservation_date)
        VALUES (?, ?, ?, ?)
    ''', (book_id, user_name, user_email, reservation_date))

    # Mark book as unavailable
    conn.execute('UPDATE books SET available = 0 WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Book reserved successfully', 'reservation_date': reservation_date}), 201

@app.route('/api/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    conn = get_db_connection()

    # Delete reservation
    conn.execute('DELETE FROM reservations WHERE book_id = ?', (book_id,))

    # Mark book as available
    conn.execute('UPDATE books SET available = 1 WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Book returned successfully'}), 200

if __name__ == '__main__':
    print("Starting Library Book Reservation System...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

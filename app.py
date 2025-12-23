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
                age_group TEXT,
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
            ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 'Adults', 'A gripping tale of racial injustice and childhood innocence.', 1),
            ('1984', 'George Orwell', '978-0-452-28423-4', 'Fiction', 'Adults', 'A dystopian social science fiction novel.', 1),
            ('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 'Romance', 'Adults', 'A romantic novel of manners.', 1),
            ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 'Adults', 'A story of the Jazz Age.', 1),
            ('Moby-Dick', 'Herman Melville', '978-0-14-243724-7', 'Adventure', 'Adults', 'The saga of Captain Ahab.', 1),
            ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', '978-0-7475-3269-9', 'Fantasy', 'Kids', 'A young wizard\'s journey begins.', 1),
            ('The Hobbit', 'J.R.R. Tolkien', '978-0-547-92822-7', 'Fantasy', 'Kids', 'A fantasy adventure of Bilbo Baggins.', 1),
            ('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 'Fiction', 'Adults', 'The story of teenage rebellion.', 1),
            ('The Lord of the Rings', 'J.R.R. Tolkien', '978-0-618-57498-4', 'Fantasy', 'Adults', 'An epic high-fantasy novel.', 1),
            ('Animal Farm', 'George Orwell', '978-0-452-28424-1', 'Fiction', 'Adults', 'A satirical allegorical novella.', 1),
            ('Brave New World', 'Aldous Huxley', '978-0-06-085052-4', 'Science Fiction', 'Adults', 'A dystopian novel set in a futuristic society.', 1),
            ('The Chronicles of Narnia', 'C.S. Lewis', '978-0-06-023481-4', 'Fantasy', 'Kids', 'A series of seven fantasy novels.', 1),
            ('Jane Eyre', 'Charlotte Bronte', '978-0-14-144114-6', 'Romance', 'Adults', 'A compelling tale of love and independence.', 1),
            ('Wuthering Heights', 'Emily Bronte', '978-0-14-143955-6', 'Romance', 'Adults', 'A passionate story of love and revenge.', 1),
            ('The Odyssey', 'Homer', '978-0-14-026886-7', 'Adventure', 'Adults', 'The epic journey of Odysseus.', 1),
            ('Frankenstein', 'Mary Shelley', '978-0-14-143947-1', 'Science Fiction', 'Adults', 'The modern Prometheus and his creation.', 1),
            ('Dracula', 'Bram Stoker', '978-0-14-143984-6', 'Fiction', 'Adults', 'The timeless vampire tale.', 1),
            ('The Picture of Dorian Gray', 'Oscar Wilde', '978-0-14-143957-0', 'Fiction', 'Adults', 'A philosophical novel about beauty and morality.', 1),
            ('Alice in Wonderland', 'Lewis Carroll', '978-0-14-143761-3', 'Fantasy', 'Kids', 'Alice\'s magical journey down the rabbit hole.', 1),
            ('The Secret Garden', 'Frances Hodgson Burnett', '978-0-14-136633-2', 'Fiction', 'Kids', 'A transformative tale of healing and growth.', 1),
            ('Little Women', 'Louisa May Alcott', '978-0-14-143966-2', 'Fiction', 'Kids', 'The lives and loves of the March sisters.', 1),
            ('The Count of Monte Cristo', 'Alexandre Dumas', '978-0-14-044926-6', 'Adventure', 'Adults', 'An epic tale of betrayal and revenge.', 1),
            ('The Three Musketeers', 'Alexandre Dumas', '978-0-14-044925-9', 'Adventure', 'Adults', 'All for one and one for all!', 1),
            ('Treasure Island', 'Robert Louis Stevenson', '978-0-14-143696-8', 'Adventure', 'Kids', 'A thrilling pirate adventure.', 1),
            ('Robinson Crusoe', 'Daniel Defoe', '978-0-14-143982-2', 'Adventure', 'Adults', 'A tale of survival on a deserted island.', 1),
            ('Dune', 'Frank Herbert', '978-0-44-117271-9', 'Science Fiction', 'Adults', 'An epic science fiction masterpiece.', 1),
            ('Foundation', 'Isaac Asimov', '978-0-55-338256-3', 'Science Fiction', 'Adults', 'The beginning of a galactic empire.', 1),
            ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', '978-0-34-539180-3', 'Science Fiction', 'Adults', 'A hilarious journey through space.', 1),
            ('Ender\'s Game', 'Orson Scott Card', '978-0-81-256751-9', 'Science Fiction', 'Kids', 'A young genius battles alien invaders.', 1),
            ('The Martian', 'Andy Weir', '978-0-55-341802-6', 'Science Fiction', 'Adults', 'Surviving alone on Mars.', 1),
            ('A Game of Thrones', 'George R.R. Martin', '978-0-55-357340-4', 'Fantasy', 'Adults', 'The beginning of an epic fantasy saga.', 1),
            ('The Name of the Wind', 'Patrick Rothfuss', '978-0-75-640407-9', 'Fantasy', 'Adults', 'A tale of magic and adventure.', 1),
            ('The Way of Kings', 'Brandon Sanderson', '978-0-76-532635-5', 'Fantasy', 'Adults', 'Epic fantasy at its finest.', 1),
            ('Mistborn', 'Brandon Sanderson', '978-0-76-531178-8', 'Fantasy', 'Adults', 'A world of ash and mist.', 1),
            ('The Dark Tower', 'Stephen King', '978-1-50-112213-8', 'Fantasy', 'Adults', 'A gunslinger\'s quest across worlds.', 1),
            ('The Handmaid\'s Tale', 'Margaret Atwood', '978-0-38-549081-8', 'Fiction', 'Adults', 'A chilling dystopian vision.', 1),
            ('The Alchemist', 'Paulo Coelho', '978-0-06-112241-5', 'Fiction', 'Adults', 'Following your dreams and personal legend.', 1),
            ('Life of Pi', 'Yann Martel', '978-0-15-602732-1', 'Adventure', 'Kids', 'A boy, a tiger, and an unforgettable journey.', 1),
            ('The Kite Runner', 'Khaled Hosseini', '978-1-59-448000-3', 'Fiction', 'Adults', 'A powerful story of friendship and redemption.', 1),
            ('Gone with the Wind', 'Margaret Mitchell', '978-1-41-652670-1', 'Romance', 'Adults', 'Love and survival during the Civil War.', 1)
        ]

        cursor.executemany('''
            INSERT INTO books (title, author, isbn, category, age_group, description, available)
            VALUES (?, ?, ?, ?, ?, ?, ?)
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

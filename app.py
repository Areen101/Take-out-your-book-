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
            ('Gone with the Wind', 'Margaret Mitchell', '978-1-41-652670-1', 'Romance', 'Adults', 'Love and survival during the Civil War.', 1),
            ('Charlotte\'s Web', 'E.B. White', '978-0-06-440055-8', 'Fiction', 'Kids', 'A heartwarming story of friendship between a pig and a spider.', 1),
            ('Matilda', 'Roald Dahl', '978-0-14-241037-0', 'Fiction', 'Kids', 'A brilliant girl with magical powers stands up to adults.', 1),
            ('The BFG', 'Roald Dahl', '978-0-14-240314-3', 'Fantasy', 'Kids', 'A Big Friendly Giant and a little girl save the world.', 1),
            ('Charlie and the Chocolate Factory', 'Roald Dahl', '978-0-14-241030-1', 'Fantasy', 'Kids', 'A magical tour through Willy Wonka\'s chocolate factory.', 1),
            ('Percy Jackson and the Lightning Thief', 'Rick Riordan', '978-0-78-838029-1', 'Fantasy', 'Kids', 'A boy discovers he\'s the son of a Greek god.', 1),
            ('The Lion, the Witch and the Wardrobe', 'C.S. Lewis', '978-0-06-076577-6', 'Fantasy', 'Kids', 'Four children discover a magical land through a wardrobe.', 1),
            ('Where the Wild Things Are', 'Maurice Sendak', '978-0-06-025492-6', 'Fiction', 'Kids', 'Max\'s wild imagination takes him on an adventure.', 1),
            ('A Wrinkle in Time', 'Madeleine L\'Engle', '978-0-31-238761-1', 'Science Fiction', 'Kids', 'A journey through time and space to rescue a father.', 1),
            ('The Giving Tree', 'Shel Silverstein', '978-0-06-025665-4', 'Fiction', 'Kids', 'A tree\'s unconditional love for a boy.', 1),
            ('Anne of Green Gables', 'L.M. Montgomery', '978-0-14-036748-0', 'Fiction', 'Kids', 'An imaginative orphan girl finds her home.', 1),
            ('The Tale of Peter Rabbit', 'Beatrix Potter', '978-0-72-326144-1', 'Fiction', 'Kids', 'A mischievous rabbit\'s adventure in Mr. McGregor\'s garden.', 1),
            ('The Wind in the Willows', 'Kenneth Grahame', '978-0-14-036250-8', 'Adventure', 'Kids', 'Adventures of Mole, Rat, Toad, and Badger.', 1),
            ('Bridge to Terabithia', 'Katherine Paterson', '978-0-06-073401-7', 'Fiction', 'Kids', 'Two friends create a magical kingdom in the woods.', 1),
            ('The Phantom Tollbooth', 'Norton Juster', '978-0-39-480670-1', 'Fantasy', 'Kids', 'A bored boy embarks on an adventure in a magical land.', 1),
            ('Holes', 'Louis Sachar', '978-0-44-042865-9', 'Adventure', 'Kids', 'A boy sent to a desert detention center uncovers a mystery.', 1),
            ('The Shining', 'Stephen King', '978-0-38-512167-5', 'Fiction', 'Adults', 'A family\'s stay at an isolated hotel turns terrifying.', 1),
            ('It', 'Stephen King', '978-1-50-116114-2', 'Fiction', 'Adults', 'A group of friends battle an ancient evil entity.', 1),
            ('The Stand', 'Stephen King', '978-0-30-774365-5', 'Fiction', 'Adults', 'Survivors of a plague face the ultimate battle of good vs evil.', 1),
            ('The Road', 'Cormac McCarthy', '978-0-30-738789-9', 'Fiction', 'Adults', 'A father and son journey through a post-apocalyptic world.', 1),
            ('Catch-22', 'Joseph Heller', '978-1-45-165348-3', 'Fiction', 'Adults', 'A satirical novel about World War II.', 1),
            ('Slaughterhouse-Five', 'Kurt Vonnegut', '978-0-38-533384-9', 'Science Fiction', 'Adults', 'A soldier becomes unstuck in time.', 1),
            ('The Bell Jar', 'Sylvia Plath', '978-0-06-083701-6', 'Fiction', 'Adults', 'A young woman\'s descent into mental illness.', 1),
            ('One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '978-0-06-088328-7', 'Fiction', 'Adults', 'The multi-generational story of the Buendia family.', 1),
            ('The Grapes of Wrath', 'John Steinbeck', '978-0-14-303943-3', 'Fiction', 'Adults', 'A family\'s struggle during the Great Depression.', 1),
            ('East of Eden', 'John Steinbeck', '978-0-14-018639-3', 'Fiction', 'Adults', 'A modern retelling of the Cain and Abel story.', 1),
            ('The Stranger', 'Albert Camus', '978-0-67-972020-3', 'Fiction', 'Adults', 'A man\'s indifference to society and life.', 1),
            ('Crime and Punishment', 'Fyodor Dostoevsky', '978-0-14-044913-6', 'Fiction', 'Adults', 'A man struggles with guilt after committing murder.', 1),
            ('The Brothers Karamazov', 'Fyodor Dostoevsky', '978-0-37-450558-6', 'Fiction', 'Adults', 'A philosophical novel about faith, doubt, and morality.', 1),
            ('War and Peace', 'Leo Tolstoy', '978-0-14-303999-0', 'Fiction', 'Adults', 'An epic tale of Russian society during the Napoleonic era.', 1),
            ('Anna Karenina', 'Leo Tolstoy', '978-0-14-303500-8', 'Romance', 'Adults', 'A tragic love story in Russian high society.', 1),
            ('The Book Thief', 'Markus Zusak', '978-0-37-584263-6', 'Fiction', 'Adults', 'Death narrates the story of a girl in Nazi Germany.', 1),
            ('The Curious Incident of the Dog in the Night-Time', 'Mark Haddon', '978-1-40-003271-7', 'Fiction', 'Kids', 'A brilliant boy investigates a mysterious dog\'s death.', 1),
            ('Room', 'Emma Donoghue', '978-0-31-609833-0', 'Fiction', 'Adults', 'A young boy and his mother escape captivity.', 1),
            ('The Help', 'Kathryn Stockett', '978-0-42-523220-8', 'Fiction', 'Adults', 'African American maids in 1960s Mississippi tell their stories.', 1),
            ('A Little Princess', 'Frances Hodgson Burnett', '978-0-14-036675-9', 'Fiction', 'Kids', 'A wealthy girl faces hardship with grace and imagination.', 1),
            ('The Fault in Our Stars', 'John Green', '978-0-14-242417-9', 'Fiction', 'Kids', 'Two teens with cancer fall in love.', 1),
            ('The Lovely Bones', 'Alice Sebold', '978-0-31-636881-7', 'Fiction', 'Adults', 'A murdered girl watches over her family from heaven.', 1),
            ('Wonder', 'R.J. Palacio', '978-0-37-586902-2', 'Fiction', 'Kids', 'A boy with facial differences starts mainstream school.', 1),
            ('The Color Purple', 'Alice Walker', '978-0-15-619235-5', 'Fiction', 'Adults', 'An African American woman\'s journey to self-discovery.', 1),
            ('Tuck Everlasting', 'Natalie Babbitt', '978-0-31-236981-2', 'Fiction', 'Kids', 'A girl discovers a family who will live forever.', 1),
            ('Eragon', 'Christopher Paolini', '978-0-37-582670-4', 'Fantasy', 'Kids', 'A farm boy becomes a dragon rider.', 1),
            ('The Witcher: The Last Wish', 'Andrzej Sapkowski', '978-0-31-637580-8', 'Fantasy', 'Adults', 'A monster hunter navigates a world of magic.', 1),
            ('The Magicians', 'Lev Grossman', '978-0-45-249413-7', 'Fantasy', 'Adults', 'A young man discovers magic is real and dangerous.', 1),
            ('Coraline', 'Neil Gaiman', '978-0-38-074690-6', 'Fantasy', 'Kids', 'A girl discovers a sinister parallel world.', 1),
            ('American Gods', 'Neil Gaiman', '978-0-38-072241-2', 'Fantasy', 'Adults', 'Old gods battle new in modern America.', 1),
            ('The Neverending Story', 'Michael Ende', '978-0-14-038632-9', 'Fantasy', 'Kids', 'A boy enters a magical book and becomes part of the story.', 1),
            ('Good Omens', 'Terry Pratchett & Neil Gaiman', '978-0-06-085398-3', 'Fantasy', 'Adults', 'An angel and demon try to prevent the apocalypse.', 1),
            ('Stardust', 'Neil Gaiman', '978-0-06-114726-4', 'Fantasy', 'Adults', 'A young man crosses into a magical realm for a fallen star.', 1),
            ('The Graveyard Book', 'Neil Gaiman', '978-0-06-053092-1', 'Fantasy', 'Kids', 'A boy raised by ghosts in a graveyard.', 1),
            ('Jonathan Strange & Mr Norrell', 'Susanna Clarke', '978-1-58-234416-0', 'Fantasy', 'Adults', 'Two magicians bring magic back to England.', 1),
            ('Ready Player One', 'Ernest Cline', '978-0-30-788743-6', 'Science Fiction', 'Adults', 'A virtual reality treasure hunt in a dystopian future.', 1),
            ('The Giver', 'Lois Lowry', '978-0-54-405798-8', 'Science Fiction', 'Kids', 'A boy discovers the dark truth of his perfect society.', 1),
            ('Neuromancer', 'William Gibson', '978-0-44-100384-1', 'Science Fiction', 'Adults', 'A hacker navigates cyberspace in a dystopian future.', 1),
            ('Snow Crash', 'Neal Stephenson', '978-0-55-308853-3', 'Science Fiction', 'Adults', 'A hacker fights a computer virus in virtual reality.', 1),
            ('The Hunger Games', 'Suzanne Collins', '978-0-43-902348-9', 'Science Fiction', 'Kids', 'Teens fight to the death in a televised spectacle.', 1),
            ('Fahrenheit 451', 'Ray Bradbury', '978-1-45-113251-1', 'Science Fiction', 'Adults', 'A fireman burns books in a future where reading is illegal.', 1),
            ('The Time Machine', 'H.G. Wells', '978-0-48-128472-4', 'Science Fiction', 'Adults', 'A man travels to the distant future.', 1),
            ('Divergent', 'Veronica Roth', '978-0-06-202402-2', 'Science Fiction', 'Kids', 'A girl defies her faction-based society.', 1),
            ('The War of the Worlds', 'H.G. Wells', '978-0-48-129506-5', 'Science Fiction', 'Adults', 'Martians invade Earth with devastating technology.', 1),
            ('Do Androids Dream of Electric Sheep?', 'Philip K. Dick', '978-0-34-540852-0', 'Science Fiction', 'Adults', 'A bounty hunter tracks rogue androids.', 1),
            ('Outlander', 'Diana Gabaldon', '978-0-44-022256-8', 'Romance', 'Adults', 'A WWII nurse travels back to 18th century Scotland.', 1),
            ('The Notebook', 'Nicholas Sparks', '978-0-44-623686-3', 'Romance', 'Adults', 'An elderly man reads to his wife about their love story.', 1),
            ('Me Before You', 'Jojo Moyes', '978-0-14-312454-9', 'Romance', 'Adults', 'A caregiver falls for her paralyzed employer.', 1),
            ('The Time Traveler\'s Wife', 'Audrey Niffenegger', '978-0-15-602943-1', 'Romance', 'Adults', 'A love story complicated by involuntary time travel.', 1),
            ('Emma', 'Jane Austen', '978-0-14-143951-0', 'Romance', 'Adults', 'A matchmaker meddles in others\' romances.', 1),
            ('Sense and Sensibility', 'Jane Austen', '978-0-14-143969-5', 'Romance', 'Adults', 'Two sisters navigate love and heartbreak.', 1),
            ('Persuasion', 'Jane Austen', '978-0-14-143965-7', 'Romance', 'Adults', 'A second chance at love years after a broken engagement.', 1),
            ('Rebecca', 'Daphne du Maurier', '978-0-38-000390-8', 'Romance', 'Adults', 'A new bride haunted by her husband\'s first wife.', 1),
            ('The Thorn Birds', 'Colleen McCullough', '978-0-38-024817-9', 'Romance', 'Adults', 'A forbidden love spanning decades in Australia.', 1),
            ('A Walk to Remember', 'Nicholas Sparks', '978-0-44-623796-9', 'Romance', 'Adults', 'A bad boy falls for the minister\'s daughter.', 1),
            ('The Call of the Wild', 'Jack London', '978-0-48-626472-6', 'Adventure', 'Kids', 'A dog\'s journey from domestication to the wild.', 1),
            ('White Fang', 'Jack London', '978-0-14-032417-7', 'Adventure', 'Kids', 'A wolf-dog\'s journey from the wild to civilization.', 1),
            ('Into the Wild', 'Jon Krakauer', '978-0-38-572178-7', 'Adventure', 'Adults', 'A young man\'s fatal journey into the Alaskan wilderness.', 1),
            ('Hatchet', 'Gary Paulsen', '978-1-41-690647-2', 'Adventure', 'Kids', 'A boy survives alone in the wilderness after a plane crash.', 1),
            ('Around the World in Eighty Days', 'Jules Verne', '978-0-14-044906-8', 'Adventure', 'Adults', 'A gentleman races around the globe on a wager.', 1),
            ('Journey to the Center of the Earth', 'Jules Verne', '978-0-14-062126-5', 'Adventure', 'Kids', 'Explorers descend into a volcanic crater.', 1),
            ('The Adventures of Tom Sawyer', 'Mark Twain', '978-0-14-036771-8', 'Adventure', 'Kids', 'A mischievous boy\'s adventures along the Mississippi.', 1),
            ('The Beach', 'Alex Garland', '978-1-57-322831-4', 'Adventure', 'Adults', 'Backpackers discover a hidden beach paradise.', 1),
            ('The Swiss Family Robinson', 'Johann David Wyss', '978-0-14-036671-1', 'Adventure', 'Kids', 'A shipwrecked family builds a new life on a deserted island.', 1),
            ('Kon-Tiki', 'Thor Heyerdahl', '978-0-67-172565-9', 'Adventure', 'Adults', 'A daring ocean voyage on a primitive raft.', 1)
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

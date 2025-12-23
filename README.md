# Library Book Reservation System

A modern web application for browsing and reserving library books. Built with Flask (Python) backend and vanilla JavaScript frontend.

## Features

- Browse available books in the library
- Search books by title, author, or category
- Filter books by category (Fiction, Fantasy, Science Fiction, etc.)
- Reserve books with your name and email
- View all current reservations
- Return reserved books
- Responsive design for mobile and desktop

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone or navigate to the repository:
```bash
cd Take-out-your-book-
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

The application will automatically create a SQLite database (`library.db`) with 12 sample books on first run.

## Usage

### Browsing Books
- The home page displays all available books in a grid layout
- Use the search bar to find books by title, author, or category
- Click on category buttons to filter books by genre

### Reserving a Book
1. Click the "Reserve Book" button on any available book
2. Enter your name and email in the modal form
3. Click "Confirm Reservation"
4. The book will be marked as reserved

### Viewing Reservations
1. Click on the "My Reservations" tab
2. See all currently reserved books with reservation details
3. Click "Return Book" to make a book available again

## Project Structure

```
Take-out-your-book-/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── library.db            # SQLite database (auto-generated)
├── static/
│   ├── index.html        # Main HTML page
│   ├── styles.css        # CSS styling
│   └── script.js         # Frontend JavaScript
└── README.md             # This file
```

## API Endpoints

- `GET /api/books` - Get all books
- `GET /api/books/<id>` - Get a specific book
- `GET /api/reservations` - Get all reservations
- `POST /api/reserve` - Reserve a book
- `POST /api/return/<id>` - Return a book

## Technologies Used

- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with gradient backgrounds and animations

## Sample Books Included

The database is pre-populated with 12 classic books including:
- To Kill a Mockingbird
- 1984
- Pride and Prejudice
- The Great Gatsby
- Harry Potter and the Philosopher's Stone
- The Hobbit
- And more!

## Development

To modify the sample books, edit the `sample_books` list in `app.py` before first run, or delete `library.db` and restart the application.

## License

This project is open source and available under the MIT License.

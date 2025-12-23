# Library Book Reservation System

A modern web application for browsing and reserving library books.

## Live Demo - Preview in Your Browser

**You can use the app directly in your browser without any installation!**

Once GitHub Pages is enabled for this repository, you can access the app at:
```
https://Areen101.github.io/Take-out-your-book-/
```

Or simply open `index.html` directly in any web browser on your iPad, phone, or computer.

The standalone version uses browser localStorage to save your data - no server needed!

## Two Versions Available

1. **Standalone Version** (`index.html`) - Works directly in browser, perfect for iPad/mobile
2. **Server Version** - Full Flask backend with Python (see installation instructions below)

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

## Enabling GitHub Pages

To enable the live preview through GitHub Pages:

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **Deploy from a branch**
5. Select **branch: claude/add-book-reservations-tjlKu** and **/ (root)**
6. Click **Save**
7. Wait a few minutes, then visit: `https://Areen101.github.io/Take-out-your-book-/`

Your app will be live and accessible from any browser, including Safari on iPad!

## License

This project is open source and available under the MIT License.

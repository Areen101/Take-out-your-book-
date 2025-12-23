const API_BASE = '/api';
let allBooks = [];
let currentFilter = 'all';
let selectedBookId = null;

// Load books on page load
document.addEventListener('DOMContentLoaded', () => {
    loadBooks();
    loadReservations();
});

// Tab switching
function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');

    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    buttons.forEach(button => {
        button.classList.remove('active');
    });

    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');

    if (tabName === 'reservations') {
        loadReservations();
    }
}

// Load all books
async function loadBooks() {
    try {
        const response = await fetch(`${API_BASE}/books`);
        allBooks = await response.json();
        displayBooks(allBooks);
    } catch (error) {
        console.error('Error loading books:', error);
        alert('Failed to load books. Please refresh the page.');
    }
}

// Display books
function displayBooks(books) {
    const booksGrid = document.getElementById('books-grid');

    if (books.length === 0) {
        booksGrid.innerHTML = '<div class="empty-message">No books found</div>';
        return;
    }

    booksGrid.innerHTML = books.map(book => `
        <div class="book-card" data-category="${book.category}">
            <h3>${book.title}</h3>
            <p class="author">by ${book.author}</p>
            <span class="category">${book.category}</span>
            <p class="description">${book.description}</p>
            <div class="status">
                <span class="status-badge ${book.available ? 'available' : 'reserved'}">
                    ${book.available ? '✓ Available' : '✗ Reserved'}
                </span>
            </div>
            ${book.available ?
                `<button class="btn btn-primary" onclick="openReservationModal(${book.id}, '${book.title}', '${book.author}')">
                    Reserve Book
                </button>` :
                `<button class="btn" disabled>Not Available</button>`
            }
        </div>
    `).join('');
}

// Filter books by search
function filterBooks() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    let filtered = allBooks;

    if (currentFilter !== 'all') {
        filtered = filtered.filter(book => book.category === currentFilter);
    }

    if (searchTerm) {
        filtered = filtered.filter(book =>
            book.title.toLowerCase().includes(searchTerm) ||
            book.author.toLowerCase().includes(searchTerm) ||
            book.category.toLowerCase().includes(searchTerm)
        );
    }

    displayBooks(filtered);
}

// Filter by category
function filterByCategory(category) {
    currentFilter = category;

    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    let filtered = allBooks;
    if (category !== 'all') {
        filtered = allBooks.filter(book => book.category === category);
    }

    displayBooks(filtered);
}

// Open reservation modal
function openReservationModal(bookId, title, author) {
    selectedBookId = bookId;
    const modal = document.getElementById('reservation-modal');
    const modalInfo = document.getElementById('modal-book-info');

    modalInfo.innerHTML = `
        <div style="background: #f9f9f9; padding: 1rem; border-radius: 5px; margin-bottom: 1.5rem;">
            <h3 style="color: #667eea; margin-bottom: 0.5rem;">${title}</h3>
            <p style="color: #666;">by ${author}</p>
        </div>
    `;

    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('reservation-modal');
    modal.style.display = 'none';
    document.getElementById('reservation-form').reset();
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('reservation-modal');
    if (event.target === modal) {
        closeModal();
    }
}

// Submit reservation
async function submitReservation(event) {
    event.preventDefault();

    const userName = document.getElementById('user-name').value;
    const userEmail = document.getElementById('user-email').value;

    try {
        const response = await fetch(`${API_BASE}/reserve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                book_id: selectedBookId,
                user_name: userName,
                user_email: userEmail
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Book reserved successfully!');
            closeModal();
            loadBooks();
            loadReservations();
        } else {
            alert(data.error || 'Failed to reserve book');
        }
    } catch (error) {
        console.error('Error reserving book:', error);
        alert('Failed to reserve book. Please try again.');
    }
}

// Load reservations
async function loadReservations() {
    try {
        const response = await fetch(`${API_BASE}/reservations`);
        const reservations = await response.json();
        displayReservations(reservations);
    } catch (error) {
        console.error('Error loading reservations:', error);
    }
}

// Display reservations
function displayReservations(reservations) {
    const reservationsList = document.getElementById('reservations-list');

    if (reservations.length === 0) {
        reservationsList.innerHTML = '<div class="empty-message">No reservations yet</div>';
        return;
    }

    reservationsList.innerHTML = reservations.map(res => `
        <div class="reservation-card">
            <div class="reservation-info">
                <h3>${res.title}</h3>
                <p><strong>Author:</strong> ${res.author}</p>
                <p><strong>Reserved by:</strong> ${res.user_name} (${res.user_email})</p>
                <p><strong>Date:</strong> ${new Date(res.reservation_date).toLocaleString()}</p>
            </div>
            <button class="btn btn-secondary" onclick="returnBook(${res.book_id})">
                Return Book
            </button>
        </div>
    `).join('');
}

// Return book
async function returnBook(bookId) {
    if (!confirm('Are you sure you want to return this book?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/return/${bookId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            alert('Book returned successfully!');
            loadBooks();
            loadReservations();
        } else {
            alert(data.error || 'Failed to return book');
        }
    } catch (error) {
        console.error('Error returning book:', error);
        alert('Failed to return book. Please try again.');
    }
}

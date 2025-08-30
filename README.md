📚 Library Management System API
📌 Overview

This project is a Library Management System API built with Django and Django REST Framework (DRF).
It allows users to manage books, borrow and return them, and track their library transactions.

🚀 Features

Books Management (CRUD): Create, Read, Update, Delete books.

User Management (CRUD): Manage library users with unique usernames and emails.

Borrowing & Returning: Users can check out and return books.

Availability Tracking: Keeps track of the number of available copies.

Search & Filters: Search books by title, author, or ISBN; filter by availability.

Authentication: Supports login and user-specific borrowing history.
## Purpose
This project solves the basic workflow for a small library:
- Add/search/list books
- Borrow (checkout) and return
- Track availability
## Future Improvements

Pagination & ordering

Auth & roles (librarian vs member)

Rate limiting & throttling

Better search (icontains/multi-fields)

Swagger/OpenAPI schema

🛠️ Tech Stack

Python 3

Django

Django REST Framework

SQLite / PostgreSQL (Database)

⚙️ Installation & Setup

Clone the repository:
**Author**: Farah Ramadan  
**Email**: rafarah507@gmail.com

git clone https://github.com/Farahrama/library-management-system-api.git
cd library-management-system-api


Create and activate a virtual environment:

python -m venv env
source env/bin/activate   # Linux / Mac
env\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run development server:

python manage.py runserver


Access the API in your browser:

http://127.0.0.1:8000/api/

🔑 Example Endpoints

Books

GET /api/books/ → List all books

POST /api/books/ → Create a book

PUT /api/books/{id}/ → Update a book

DELETE /api/books/{id}/ → Delete a book

Borrow & Return

POST /api/checkout/ → Borrow a book

POST /api/return/ → Return a book

Search & Filters

GET /api/books/?search=python

GET /api/books/?available=true

GET /api/books/?ordering=-published_date

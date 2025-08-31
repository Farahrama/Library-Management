Library Management System
Django-based web application for managing a small library, including book listings, borrowing, returning, and API endpoints
Overview

The Library Management System is a web application built with Django and Django REST Framework (DRF) to manage books, borrowing, and returning. It provides a RESTful API for book management and a simple web interface for browsing books, borrowing, and returning them.

Features





Web Interface:





Home page (/): Displays links to various functionalities.



Books list page (/books/): Displays a list of all books in the library.



Borrow page (/checkout/): Allows authenticated users to borrow a book.



Return page (/return/): Allows authenticated users to return a borrowed book.



REST API:





/api/books/: Manage books (Create, Read, Update, Delete) with search and filtering support.



/api/books/stats/: Retrieve statistics (total books and available copies).



/api/checkout/ and /api/return/ (under development).



Arabic validation messages (e.g., "Publication date cannot be in the future").



Admin panel (/admin/) for managing books and users.

Installation Requirements





Python 3.13 or higher



Required packages (listed in requirements.txt):

Django>=4.0,<5.0
djangorestframework>=3.14
python-dotenv>=1.0
psycopg2-binary>=2.9

Setup Instructions





Clone the repository:

git clone https://github.com/Farahrama/Library-Management
cd Library-Management



Create and activate a virtual environment:

python -m venv env
env\Scripts\activate     # On Windows



Install dependencies:

pip install -r requirements.txt



Apply migrations to set up the database:

python manage.py makemigrations
python manage.py migrate



Create a superuser (optional, for admin access):

python manage.py createsuperuser



Run the development server:

python manage.py runserver

Usage





Web Interface:





Home page: http://127.0.0.1:8000/



Books list: http://127.0.0.1:8000/books/



Borrow a book: http://127.0.0.1:8000/checkout/ (requires login)



Return a book: http://127.0.0.1:8000/return/ (requires login)



Admin panel: http://127.0.0.1:8000/admin/ (for superusers)



REST API:





List books: GET /api/books/



Search: GET /api/books/?search=<title_or_author>



Filter: GET /api/books/?author=<author_name>



Statistics: GET /api/books/stats/



Note: If authentication is enabled, obtain a JWT token via:

curl -X POST http://127.0.0.1:8000/api/token/ -d "username=<username>&password=<password>"

Notes





Authentication: The /checkout/ and /return/ pages require login. You can temporarily disable authentication for testing by updating settings.py:

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    # ... other settings ...
}



Testing: The project includes a basic SmokeTest. Comprehensive tests for CRUD operations and borrowing/returning are recommended.



Future Improvements:





Add Swagger/OpenAPI documentation for the API.



Enhance security by storing SECRET_KEY in a .env file.



Implement additional tests for all features.

Security





Move SECRET_KEY to a .env file for security:

SECRET_KEY=your-secret-key-here

Update settings.py:

import os
from dotenv import load_dotenv
load_dotenv()

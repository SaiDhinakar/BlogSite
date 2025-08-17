# BlogSite

A simple Django-based blog application with authentication, TinyMCE editor, and user profile management.

## Features

- User registration and authentication
- Blog post creation and editing with TinyMCE rich text editor
- User profile images
- Admin interface

## Live Demo

[View the live demo](http://127.0.0.1:8000/)

## Getting Started

1. Clone the repository
2. Install dependencies from `requirements.txt`
3. Run migrations:
   ```sh
   python manage.py migrate
   ```
4. Start the development server:
   ```sh
   python manage.py runserver
   ```
5. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser

## Static & Media Files

- Place static files in the `static/` directory.
- Place uploaded media (e.g., profile images) in the `media/` directory.

# Adombire Press - Backend

Django DRF backend for Adombire Press blog.

## Features
- Blog post management (CRUD)
- User authentication
- Categories and comments
- RESTful APIs

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`
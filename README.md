# codElevate - Interactive Learning Management System

---

A modern learning management system built with Django that provides an engaging platform for online education. codElevate offers a seamless experience for both educators and learners with its intuitive interface and comprehensive feature set.

---

## Key Features

- **User Authentication**
  - Secure login and signup system
  - Password reset functionality
  - Session management

- **User Dashboard**
  - Personalized learning progress tracking
  - Quick access to enrolled courses
  - Latest activity feed

- **Course Management**
  - Browse available courses
  - Course enrollment system
  - Progress tracking

- **User Profiles**
  - Customizable user profiles
  - Learning history
  - Achievement tracking

---

## Technology Stack

- **Backend**: Django 5.2
- **Database**: SQLite (default)
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django Authentication System

---

## Project Structure

```
codElevate/
├── codElevate/          # Main project configuration
├── courses/             # Courses management app
├── dashboard/           # User dashboard app
├── login/               # Authentication system
├── myprofile/           # User profile management
├── static/              # Project-wide static files
├── staticfiles/         # Collected static files
└── templates/           # Project-wide templates
```

---

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment tool (venv)

---

## Setup Instructions

1. Clone the repository :--

   ```bash
   git clone https://github.com/WhiteJadeWolf/code-E-levate.git
   cd codElevate
   ```

2. Install Python uv (universal package resolver & installer) :--

   ```bash
   pip install uv
   ```

3. Create and activate a virtual environment :--

   ```bash
   uv venv
   ```

   Then,
   For Mac :

   ```bash
   source .venv/bin/activate
   ```

   For Windows :

   ```bash
   .venv\Scripts\activate
   ```


4. Install dependencies :--

   ```bash
   pip install -r requirements.txt
   ```

5. Configure the environment :--
   - Copy `.env.example` to `.env` (if exists)
   - Update the configuration values as needed

6. Apply database migrations :--

   ```bash
   python manage.py migrate
   ```

7. Create a superuser (admin) :--

   ```bash
   python manage.py createsuperuser
   ```

8. Collect static files :--

   ```bash
   python manage.py collectstatic
   ```

9. Run the development server :--

   ```bash
   python manage.py runserver <port-address>
   ```
   Specifying Port Address is `optional`
   Default Port : 8000

10. Access the application :--
   - Main site: http://localhost:8000  (or respective custom port)
   - Admin panel: http://localhost:8000/admin

**NOTE :**
To deactivate the virtual environment, run this command :

```bash
deactivate
```

---

## Development Guide

### Project Configuration
- Main settings: `codElevate/settings.py`
- URL configuration: `codElevate/urls.py`
- WSGI/ASGI configuration: `codElevate/wsgi.py`, `codElevate/asgi.py`

### Static Files
- Static files are organized by app in their respective `static/` directories
- Project-wide static files go in the root `static/` directory
- Run `python manage.py collectstatic` after adding/modifying static files

### Templates
- Templates are organized by app in their respective `templates/` directories
- Project-wide templates go in the root `templates/` directory

### Adding New Features
1. Create a new Django app: `python manage.py startapp app_name`
2. Add the app to `INSTALLED_APPS` in `settings.py`
3. Create necessary models, views, and templates
4. Add URL patterns in the app's `urls.py`
5. Include the app's URLs in the main `urls.py`

---

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

---

## License

[MIT License](https://github.com/WhiteJadeWolf/codElevate/blob/main/LICENSE)

---

## Author

- Shuvrangshu Barua (@WhiteJadeWolf)
- Dheeraj Dubey (@Dhiraj2684)

---

## Acknowledgments

- Django documentation and community
- Contributors to the project
- All open-source packages used in this project

---

# codElevate - Learning Management System

A modern learning management system built with Django that provides an interactive platform for online education.

## Project Structure

```
codElevate/
├── codElevate/          # Main project configuration
├── courses/             # Courses app
├── dashboard/           # User dashboard app
├── login/              # Authentication app
├── myprofile/          # User profile app
├── static/             # Project-wide static files
├── staticfiles/        # Collected static files
└── templates/          # Project-wide templates
```

## Features

- User Authentication (Login/Signup)
- User Dashboard
- Course Management
- User Profiles

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Dhiraj2684/code-E-levate.git
   cd codElevate
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install django
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://localhost:8000

## Development

- Main settings file: `codElevate/settings.py`
- URL configuration: `codElevate/urls.py`
- Static files are organized by app in the `static/` directory
- Templates are organized by app in their respective `templates/` directories

## License

This project is licensed under the MIT License.
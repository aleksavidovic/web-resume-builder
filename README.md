# Web Resume Builder

Web Resume Builder is a dynamic web application designed to streamline the process of creating, managing, and customizing multiple versions of a professional resume. Built with Flask and SQLAlchemy, this project showcases a modern and modular approach to web development, providing users with a flexible platform to tailor their resumes for various job applications.

## Key Features

- **Dynamic Resume Sections**: Create and manage distinct entries for different parts of your resume, including:
    - Basic Information (contact details, job titles)
    - Professional Summaries
    - Work Experience
    - Education History
    - Skills
    - Languages
- **Custom Resume Assembly**: Build unique resume versions by selecting from your stored entries. This allows for easy customization for different job applications.
- **User Authentication**: A secure user registration and login system to keep your resume data private and organized.
- **Markdown Preview**: Instantly generate and preview a markdown version of any resume you create, laying the groundwork for future PDF generation.
- **Modular Architecture**: The application is built using Flask Blueprints, ensuring a clean and scalable codebase.

## Tech Stack

This project leverages a modern and robust technology stack:
- Backend: Flask, Gunicorn
- Database: Flask-SQLAlchemy, with Flask-Migrate and Alembic for database migrations.
- Authentication: Flask-Login and Flask-Bcrypt for secure user session management.
- Frontend: Jinja2 for templating, with standard HTML and CSS.
- Tooling: uv for package management.

# Getting Started

To get a local copy up and running, follow these simple steps.

## Prerequisites
```
    Python 3.13+
    uv package manager
```

## Installation
Clone the repository:
```bash

git clone https://github.com/your-username/web-resume-builder.git
cd web-resume-builder
```

Create a virtual environment and install dependencies:
```bash
uv venv
uv pip install -r requirements.txt
```

Set up your environment variables:
Create a .env file in the root directory and add the following, replacing the placeholder values:
```
SECRET_KEY='a-strong-and-secret-key'
SQLALCHEMY_DATABASE_URI='sqlite:///instance/resume_builder.db'
```

Run the database migrations:
Bash

flask db upgrade

Run the application:
Bash

    ./run.sh
    The application will be available at http://localhost:8080.

Project Structure

The project follows a modular structure, with key components organized into Flask Blueprints:

    src/resume_builder/: The main application package.
        main/: Handles the main landing and informational pages.
        auth/: Manages user authentication (login, registration).
        resume_builder_core/: The core logic for creating and managing resumes.
        models.py: Defines the SQLAlchemy database models.
        extensions.py: Initializes Flask extensions.
    migrations/: Contains the Alembic database migration scripts.
    templates/: Holds all Jinja2 templates for the application.

# Future Enhancements

This project has a solid foundation with several exciting possibilities for future development:
- **PDF Generation (WIP)**: Implement a feature to convert the markdown previews into downloadable PDF resumes.
- **Template Customization**: Offer a variety of professional resume templates for users to choose from.
- **Enhanced UI/UX**: Improve the user interface with a more modern frontend framework like React or Vue.js.

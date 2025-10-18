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
```bash
./run.sh
```

The application will be available at http://localhost:8080.

## Project Structure

The project follows a modular structure, with key components organized into Flask Blueprints:

```
src/resume_builder/: The main application package.
    main/: Handles the main landing and informational pages.
    auth/: Manages user authentication (login, registration).
    resume_builder_core/: The core logic for creating and managing resumes.
    models.py: Defines the SQLAlchemy database models.
    extensions.py: Initializes Flask extensions.
migrations/: Contains the Alembic database migration scripts.
templates/: Holds all Jinja2 templates for the application.
```

# Future Enhancements

This project has a solid foundation with several exciting possibilities for future development:
- [x] **PDF Generation**: Implement a feature to convert the markdown previews into downloadable PDF resumes.
- [x] **Template Customization**: Offer a variety of professional resume templates for users to choose from.
- [ ] **Enhanced UI/UX**: Improve the user interface with a more modern frontend framework like React or Vue.js.

```
## Database Schema

Here is the Entity-Relationship Diagram for the database:

```mermaid
erDiagram
    %% --- Existing Resume Builder Entities ---
    USER ||--o{ BASIC_INFO : "has"
    USER ||--o{ SUMMARY : "has"
    USER ||--o{ EXPERIENCE : "has"
    USER ||--o{ EDUCATION : "has"
    USER ||--o{ SKILLS : "has"
    USER ||--o{ LANGUAGE : "has"
    USER ||--o{ BUILT_RESUME : "has"
    USER ||--o| INVITE_CODE : "redeemed by"

    BUILT_RESUME ||--|| BASIC_INFO : "uses"
    BUILT_RESUME ||--|| SUMMARY : "uses"
    BUILT_RESUME ||--|| RESUME_THEME : "uses"

    BUILT_RESUME }o--o{ EXPERIENCE : "includes"
    BUILT_RESUME }o--o{ EDUCATION : "includes"
    BUILT_RESUME }o--o{ SKILLS : "includes"
    BUILT_RESUME }o--o{ LANGUAGE : "includes"

    %% --- New Job Application Tracking Entities ---
    USER ||--o{ JOB_APPLICATION : "has"
    JOB_APPLICATION ||--o{ APPLICATION_NOTE : "has"
    JOB_APPLICATION ||--|| APPLICATION_STAGE : "is at"
    JOB_APPLICATION ||--o| BUILT_RESUME : "used"  // Optional relationship

    %% --- Entity Definitions ---

    INVITE_CODE {
        GUID id PK
        string code
        text description
        boolean redeemed
        GUID user_id FK "nullable, unique"
        datetime created_at
        datetime updated_at
    }

    USER {
        GUID id PK
        string username UK
        string password_hash
        boolean is_admin
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    BASIC_INFO {
        GUID id PK
        string full_name
        string job_title
        string address
        string contact_email
        string contact_phone
        string linkedin_url "nullable"
        string github_url "nullable"
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    SUMMARY {
        GUID id PK
        text content "nullable"
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    EXPERIENCE {
        GUID id PK
        string job_title
        string company_name
        date date_started
        date date_finished "nullable"
        text description "nullable"
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    EDUCATION {
        GUID id PK
        string degree_name
        string school_name
        date date_started
        date date_finished "nullable"
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    SKILLS {
        GUID id PK
        string skill_group_title "nullable"
        text description
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    LANGUAGE {
        GUID id PK
        string name
        string proficiency
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    RESUME_THEME {
        GUID id PK
        string name UK
        string description "nullable"
        text styles
        datetime created_at
        datetime updated_at
    }

    BUILT_RESUME {
        GUID id PK
        GUID basic_info_id FK "references BASIC_INFO.id"
        GUID summary_id FK "references SUMMARY.id"
        GUID theme_id FK "references RESUME_THEME.id"
        GUID user_id FK "references USER.id"
        string entry_title "UK with user_id"
        datetime created_at
        datetime updated_at
    }

    %% --- New Entities Added Below ---

    APPLICATION_STAGE {
        int id PK
        string name UK
        string description "nullable"
        int display_order UK "Defines sequence: Wishlist=10, Contacted=15, Screening=20, Applied=30, Interview=40, Assessment=50, Offer=60, Rejected=70, Withdrawn=80"
    }

    JOB_APPLICATION {
        GUID id PK
        string job_title
        string company_name
        string location "nullable"
        date application_date
        string job_url "nullable"
        string application_source "nullable, e.g., 'LinkedIn Ad', 'Recruiter Outreach'"
        int application_stage_id FK "references APPLICATION_STAGE.id"
        string salary_expected "nullable"
        string salary_offered "nullable"
        text notes "nullable"
        GUID built_resume_id FK "nullable, references BUILT_RESUME.id"
        GUID user_id FK "references USER.id"
        datetime created_at
        datetime updated_at
    }

    APPLICATION_NOTE {
        GUID id PK
        text content
        GUID job_application_id FK "references JOB_APPLICATION.id"
        datetime created_at
        datetime updated_at
    }

    %% --- Notes on Association Tables (Implicit in Mermaid's M-N syntax) ---
    %% built_resume_experience (built_resume_id PK, FK | experience_id PK, FK)
    %% built_resume_education (built_resume_id PK, FK | education_id PK, FK)
    %% built_resume_skills (built_resume_id PK, FK | skills_id PK, FK)
    %% built_resume_language (built_resume_id PK, FK | language_id PK, FK)


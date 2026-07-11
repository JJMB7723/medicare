# MediCare - Hospital Management System

MediCare is an enterprise-grade, production-quality Hospital Management System built with Python, Django, MySQL, and Bootstrap 5. It follows clean architecture, modular coding standards, role-based access control, and responsive design guidelines.

## Technology Stack

- **Backend:** Python 3.x, Django 6.0, Django ORM
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript, Bootstrap Icons
- **Database:** MySQL (production-ready) with seamless SQLite fallback for local development
- **Styling & Forms:** Django Crispy Forms (Bootstrap 5 templates)
- **Media Uploads:** Pillow (Doctor profile photos, Clinical lab sheets)

---

## Project Structure

```text
medicare/
│
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── README.md
│
├── medicare/                  # Project config directory
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                  # Auth & User profiles
│   ├── mixins.py              # Role-based access controls
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── password_change.html
│   │   ├── password_change_done.html
│   │   ├── password_reset.html
│   │   └── dashboard.html     # Role-based unified dashboard
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── core/                      # Public pages (Home, About)
│   ├── models.py              # GalleryImage models
│   ├── templates/core/
│   │   ├── home.html
│   │   └── about.html
│   ├── views.py
│   └── urls.py
│
├── departments/               # Department CRUD & display
│   ├── templates/departments/
│   │   ├── list.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── doctors/                   # Doctor profiles & details
│   ├── templates/doctors/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── patients/                  # Patient registration & profiles
│   ├── templates/patients/
│   │   ├── register.html
│   │   ├── list.html
│   │   └── form.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── appointments/              # Appointment booking & status
│   ├── templates/appointments/
│   │   ├── book.html
│   │   ├── history.html
│   │   └── list.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── medical_records/           # Diagnoses & prescriptions
│   ├── templates/medical_records/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── form.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── contact/                   # Contact form & messages
│   ├── templates/contact/
│   │   ├── contact.html
│   │   └── messages_list.html
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── templates/                 # Shared base layout components
│   ├── base.html
│   ├── navbar.html
│   └── footer.html
│
└── static/                    # Custom global style assets
    ├── css/
    │   └── custom.css
    └── js/
        └── custom.js
```

---

## Detailed Installation & Setup

### 1. Prerequisites
- Python 3.10+
- MySQL Server (Optional, SQLite will run by default)
- Virtual Environment tool (`venv` or `virtualenv`)

### 2. Setup Database (Optional - MySQL)
1. Start your local MySQL server.
2. Log in and create the database:
   ```sql
   CREATE DATABASE medicare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### 3. Clone and Initialize Project
1. Navigate to the project root directory.
2. Create and activate a python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Environment Configuration
1. Open the `.env` file at the root.
2. Set `USE_MYSQL=True` if using MySQL. Otherwise, keep it as `False` to run on the default SQLite setup.
3. Configure your MySQL credentials:
   ```ini
   USE_MYSQL=True
   DB_NAME=medicare_db
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

### 5. Database Migrations
Run the following commands to generate schemas and initialize base structures:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
Create an administrative login to manage the Django Admin portal and core features:
```bash
python manage.py createsuperuser
```

### 7. Run Server
Start the local development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## Automated Testing & Validation

The application contains custom unit test coverage for booking schedule validation checks and profile constraints.

To execute tests, run:
```bash
python manage.py test
```

### Validation Highlights:
- **Past-Date Validation:** Prevents patients or receptionists from scheduling appointments in the past.
- **Double Booking Check:** Automatically checks if a doctor is already booked for the specified date and time, preventing overlap.
- **Custom Doctor Cascading Select:** Limits Doctor select choices client-side dynamically based on selected Department categories.

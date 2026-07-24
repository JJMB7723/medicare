# MediCare – Hospital Management System

MediCare is a production-quality, web-based Hospital Management System built using Python 3, Django, MySQL, Bootstrap 5, and Vanilla JavaScript. 

The application facilitates complete clinical administration, patient self-registration, dynamic appointment scheduling with double-booking prevention, medical history tracking (diagnoses & prescriptions), printing prescriptions, and contact message logging.

---

## Technology Stack

* **Backend**: Python 3, Django Web Framework (with MTV Architecture)
* **Frontend**: HTML5, CSS3, Bootstrap 5 (with Bootstrap Icons), Vanilla JavaScript (AJAX)
* **Database**: MySQL Database
* **Styling & Presentation**: Django Crispy Forms, Custom clean clinical stylesheets

---

## Features

1. **Custom User Authentication & Role System**:
   * Multi-role authorization: **Administrator**, **Receptionist**, **Doctor**, and **Patient**.
   * Secure registration, login, logout, and password change utilities.
2. **Department Management**:
   * Complete CRUD for departments (Cardiology, Neurology, Pediatrics, Orthopedics, etc.).
   * Visual directory lists using clean Bootstrap cards.
3. **Doctor Profiles**:
   * Complete Doctor database logs, fee configurations, qualifications, and scheduling availabilities.
   * Direct booking shortcuts per doctor.
4. **Patient Registration & Profiles**:
   * Online self-registration form using Crispy Forms with email, username, and password confirmations.
   * Full profile tracking ages, blood groups, addresses, and clinical symptoms.
5. **Appointment Booking (with AJAX)**:
   * Dynamically loads doctors based on selected department using clean AJAX callbacks.
   * **Past Date Prevention**: Rejects booking dates prior to current local time.
   * **Double-Booking Protection**: Validates and blocks overlapping appointments for the same doctor, date, and time slot.
   * Logs status tracking: *Pending*, *Approved*, *Completed*, or *Cancelled*.
6. **Medical Records**:
   * Attending doctors can add detailed clinical diagnoses, medication prescriptions, and upload lab report files.
   * Premium printable prescription invoice templates with built-in `window.print()` triggers.
7. **Contact Module**:
   * Google Maps locator embed, address listings, ambulance and reception hotlines.
   * Stores customer/patient messages directly in the database for admin review.
8. **Customized Django Admin Panel**:
   * Rebranded header ("MediCare Hospital Administration").
   * Interactive filters, inline doctor photo thumbnails, search parameters, and bulk status update actions.

---

## Installation & Setup Guide

### 1. Prerequisites
Ensure you have Python 3.x and MySQL installed on your system.

### 2. Clone and Initialize Environment
Navigate to the project root directory and initialize the virtual environment:
```bash
python -m venv .venv
```

Activate the virtual environment:
* **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database & Environment Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your MySQL credentials (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).

### 5. Generate Schema & Migrate
Generate migrations and apply them to create the tables in your database:
```bash
python manage.py makemigrations accounts departments doctors patients appointments medical_records contact
python manage.py migrate
```

### 6. Seed Demo Data
Populate the database with pre-configured departments, doctor profiles, and demo users:
```bash
python seed_db.py
```

### 7. Run the Server
Launch the Django local development server:
```bash
python manage.py runserver
```
Visit the application in your browser at `http://127.0.0.1:8000/`.

---

## Demo Account Credentials

Use these pre-seeded accounts to explore different features:

| Role | Username | Password | Actions Available |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full dashboard, create/edit doctors & departments, read contact inbox |
| **Doctor** | `doctor` | `doctor123` | View assigned appointments, append patient medical records |
| **Receptionist** | `receptionist` | `receptionist123` | Register patients, book appointments, approve or cancel bookings |
| **Patient** | `patient` | `patient123` | Book doctor appointments, view prescription details, view medical history |

---

## Running Unit Tests

Run the automated tests to verify booking constraints:
```bash
python manage.py test appointments
```

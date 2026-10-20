# 🎬 Movie Magic

A modern, cloud-native movie ticket booking application built with **Flask**, designed for scalable deployment across **AWS** (Amazon DynamoDB, Amazon SNS, and Amazon EC2 with Gunicorn & Nginx).

---

## 🚀 Phase 1: Project Foundation & Architecture

Phase 1 provides the foundational architecture, security framework, responsive cinematic UI, interactive seat booking workflow, and comprehensive test suite:

- **Cinematic Dark Navy & Violet UI**: Dark aesthetic (`#070b14`), luminous accents, responsive navigation, and mobile-friendly layouts.
- **Interactive Theater Seating**: Curved screen visual, seat tiers (VIP Recliner, Premium Gold, Standard Silver), live seat selection, collision prevention, and real-time total calculator.
- **E-Ticket & Booking Receipts**: Simulated QR code generation, ticket reference numbers, and printable ticket layout.
- **Security First**: Werkzeug password hashing (PBKDF2/scrypt), CSRF form protection via Flask-WTF, role-based access control (`@login_required`, `@admin_required`), and secure session cookies (`HttpOnly`, `SameSite=Lax`).
- **AWS Integration Stubs**: Centralized `app/aws/` client factory, DynamoDB service adapter, and SNS notification publisher ready for seamless Phase 2 cloud connection without hardcoded keys.
- **Health Check API**: `/health` endpoint for readiness probes, load balancers, and monitoring.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.11+ / Flask 3.1 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons |
| **Security** | Werkzeug Security, Flask-WTF (CSRF), itsdangerous |
| **AWS SDK** | `boto3` (Centralized adapter with local/demo mock fallback) |
| **Database (Planned Phase 2)** | Amazon DynamoDB |
| **Messaging (Planned Phase 2)** | Amazon SNS (Booking Confirmation Emails) |
| **Hosting & Web Server** | Amazon EC2, Gunicorn (WSGI), Nginx reverse proxy |
| **Testing** | Pytest 8+ |

---

## 📂 Project Directory Structure

```text
movie-magic/
│
├── .env.example              # Environment variables template (no secrets committed)
├── .gitignore                # Git exclusions (virtual env, caches, sensitive files)
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Setup & documentation
├── run.py                    # Application entry point
│
├── app/
│   ├── __init__.py           # Application factory (create_app), blueprints, CSRF
│   ├── config.py             # Config classes (Development, Testing, Production)
│   ├── forms.py              # Flask-WTF forms with CSRF protection
│   │
│   ├── aws/                  # AWS service interfaces & adapters (ready for Phase 2)
│   │   ├── __init__.py
│   │   ├── client_factory.py # Safe boto3 client factory with mock fallback
│   │   ├── dynamodb.py       # DynamoDB table operations adapter
│   │   └── sns.py            # SNS email dispatch adapter
│   │
│   ├── data/                 # Sample movie catalog & theater datasets
│   │   ├── __init__.py
│   │   └── sample_movies.py  # Realistic movies, showtimes, cities, seat tiers
│   │
│   ├── repositories/         # Data access layer (in-memory for Phase 1, DynamoDB ready)
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   ├── movie_repository.py
│   │   └── booking_repository.py
│   │
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Registration, authentication, password verification
│   │   ├── movie_service.py  # Movie catalog query, filtering, search
│   │   └── booking_service.py# Seat reservation logic, pricing, notifications
│   │
│   ├── utils/                # Security decorators & helpers
│   │   ├── __init__.py
│   │   ├── decorators.py     # @login_required, @admin_required
│   │   └── security.py       # Password hashing & validation
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── cinematic.css # Custom dark navy & violet styling
│   │   └── js/
│   │       ├── main.js       # Toast alerts & UI helpers
│   │       └── seat-map.js   # Interactive seat selection & live price calculator
│   │
│   └── templates/
│       ├── base.html         # Base template with glassmorphic navbar & demo banner
│       ├── main/
│       │   ├── index.html    # Home page with hero, search, filters & movie cards
│       │   ├── movies.html   # Full movie catalog
│       │   └── movie_detail.html # Movie synopsis, cast, formats, showtimes
│       ├── auth/
│       │   ├── login.html    # Sign In with CSRF & demo autofill buttons
│       │   └── register.html # Sign Up with password complexity checks
│       ├── booking/
│       │   ├── select_seats.html # Interactive auditorium seat layout
│       │   ├── confirmation.html # E-ticket with simulated QR code & print style
│       │   └── history.html  # User booking history
│       ├── admin/
│       │   ├── dashboard.html# Management dashboard & analytics
│       │   └── add_movie.html# Add movie to inventory
│       └── errors/
│           ├── 403.html
│           ├── 404.html
│           └── 500.html
│
└── tests/
    ├── __init__.py
    ├── conftest.py           # Pytest fixtures (client, auth_client, admin_client)
    ├── test_health.py        # Health-check endpoint tests
    ├── test_auth.py          # Registration, login, password hashing tests
    ├── test_movies.py        # Catalog, search, filtering tests
    ├── test_booking.py       # Seat reservation & price calculation tests
    └── test_admin.py         # Role-based access & admin operations tests
```

---

## 💻 Local Windows PowerShell Setup Instructions

Follow these exact steps in **Windows PowerShell** to install dependencies, run the test suite, and start the development server.

### 1. Clone & Navigate to Project Directory
```powershell
git clone https://github.com/GKExpo/movie-magic.git
cd movie-magic
```

### 2. Create and Activate Virtual Environment
```powershell
# Create virtual environment named .venv
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or directly invoke `.\.venv\Scripts\python.exe`.)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template configuration file:
```powershell
Copy-Item .env.example .env
```

### 5. Run the Automated Test Suite
Execute pytest to verify all routes, authentication, seat selection, and security controls:
```powershell
pytest
```
*Expected result: 23 passing tests with zero failures.*

### 6. Start the Flask Development Server
```powershell
python run.py
```

The application will start on:
- 🌐 **Web Interface:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- 🩺 **Health Check:** [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)

---

## 🔑 Pre-Configured Demo Accounts

For convenient testing during Phase 1 development, the in-memory repository includes the following accounts:

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Demo User** | `demo@moviemagic.com` | `Demo@123` | Browse catalog, select seats, book tickets, view history |
| **Administrator** | `admin@moviemagic.com` | `Admin@123` | Access Admin Portal, view revenue metrics, add/delete movies |

*(You can also register any new account on the [Registration Page](http://127.0.0.1:5000/auth/register).)*

---

## 🩺 Health Check Verification

The `/health` endpoint returns a 200 OK JSON response:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"
```
```json
{
  "status": "healthy",
  "service": "Movie Magic",
  "version": "1.0.0-phase1",
  "environment": "development",
  "aws_mode": "mock/demo"
}
```

---

## 🔒 Security Best Practices Implemented

1. **No Plaintext Passwords**: Passwords are saved as cryptographic hashes using Werkzeug (`generate_password_hash` / `check_password_hash`).
2. **CSRF Protection**: All state-changing POST forms (Login, Register, Book Seats, Add Movie, Delete Movie) require valid CSRF tokens via Flask-WTF.
3. **Restricted Admin Routes**: Protected by the `@admin_required` decorator; non-administrators receive `403 Forbidden`.
4. **Separation of Settings**: Base configuration, Development, Testing, and Production are cleanly isolated in `app/config.py`.
5. **No AWS Secret Leaks**: Zero hardcoded credentials. All AWS settings read from environment variables or use local demo mode when keys are omitted.

---

## 🗺️ Next Steps: Phase 2 Roadmap

- **Amazon DynamoDB Integration**: Provision tables (`moviemagic_users`, `moviemagic_movies`, `moviemagic_theaters`, `moviemagic_bookings`) and switch repositories from in-memory to DynamoDB.
- **Amazon SNS Integration**: Connect booking checkout to Amazon SNS Topic ARN to send email confirmations to ticket buyers.
- **IAM Policies**: Define least-privilege IAM roles for EC2 instances.
- **EC2 & Production Hosting**: Create deployment scripts with Gunicorn systemd service and Nginx reverse proxy configuration.

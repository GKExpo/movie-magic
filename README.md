# 🎬 Movie Magic

A modern, cloud-native movie ticket booking application built with **Flask**, designed for scalable deployment across **AWS** (Amazon DynamoDB, Amazon SNS, and Amazon EC2 with Gunicorn & Nginx).

---

## 🚀 Phase 2: Amazon DynamoDB Integration (Milestones 1, 2 & 3 Complete)

Phase 2 transitions Movie Magic to a cloud-native AWS architecture using Amazon DynamoDB in the **`ap-south-1` (Mumbai)** region:

- **DynamoDB Catalogue & Venue Integration (Milestone 3)**:
  - Backed by `moviemagic_movies`, `moviemagic_theaters`, and `moviemagic_showtimes` tables.
  - **GSI Query Optimization**:
    - `CategoryIndex` query on `moviemagic_movies` for category browsing (avoiding full-table scans).
    - `CityStatusIndex` composite query on `moviemagic_theaters` for operational venue filtering by city.
    - `MovieShowtimeIndex` and `TheaterShowtimeIndex` queries on `moviemagic_showtimes` for separated schedule lookups.
  - **Pagination & Decimal Handling**: Recursively decodes DynamoDB `Decimal` types into Python `float`/`int` and transparently handles pagination tokens (`LastEvaluatedKey`).
  - **Demo Showtime Guard**: Demo schedules explicitly maintain `is_verified: False` and `status: "Demo / Sample"` badges and disclaimers.
  - **Strict Anti-Degradation**: `USE_AWS_MOCK=False` raises an explicit `RuntimeError` if AWS client fails to initialize.
  - **Mock Mode Continuity**: Seamless in-memory repository fallback during local development.
- **DynamoDB User Authentication (Milestone 2)**:
  - Backed by `moviemagic_users` table in `ap-south-1`.
  - **Atomic Email Uniqueness**: Enforces email uniqueness via native DynamoDB `TransactWriteItems` writing both User Profile (`user_id = usr-<uuid>`) and Email Lock (`user_id = EMAIL#<email>`) with `attribute_not_exists(user_id)` condition.
  - **Selective Cancellation Analysis**: Inspects `TransactionCanceledException` cancellation reasons, mapping only email-lock failures to `DuplicateEmailError` while handling other transient errors safely.
  - **Normalized Email Handling**: Consistent whitespace stripping and lowercasing across registrations, lookups, locks, and logins.
  - **Zero Schema Changes**: Fully compatible with existing table schema and sparse `EmailIndex` GSI.
  - **Strict Anti-Degradation**: `USE_AWS_MOCK=False` raises an explicit `RuntimeError` if AWS credentials/client fail, prohibiting silent fallback to mock.
  - **Mock Mode Continuity**: In-memory repository remains active by default with pre-seeded demo accounts.
- **Boto3 AWS Client Factory & Credential Chain (Milestone 1)**:
  - Centralized in `app/aws/client_factory.py`.
  - Supports standard AWS credential resolution (IAM roles on EC2 IMDSv2, AWS credentials file, profiles, environment variables).
  - Configurable `DYNAMODB_ENDPOINT_URL` for local DynamoDB (`http://localhost:8000`) or testing containers.
  - Zero-cost mock mode (`USE_AWS_MOCK=True`) active by default, ensuring zero external network calls or costs during local development.
- **On-Demand Table Architecture (6 Tables, PAY_PER_REQUEST)**:
  1. `moviemagic_users` (PK: `user_id`, GSI: `EmailIndex` on `email`)
  2. `moviemagic_movies` (PK: `movie_id`, GSI: `CategoryIndex` on `category` + `release_year`)
  3. `moviemagic_theaters` (PK: `theater_id`, GSI: `CityStatusIndex` on `city` + `operational_status`)
  4. `moviemagic_showtimes` (PK: `showtime_id`, GSIs: `MovieShowtimeIndex`, `TheaterShowtimeIndex`)
  5. `moviemagic_bookings` (PK: `booking_id`, GSI: `UserBookingsIndex` on `user_id` + `created_at`)
  6. `moviemagic_show_seats` (PK: `show_key`, SK: `seat_code` — Atomic double-booking prevention)
- **Infrastructure Management CLI (`scripts/create_dynamodb_tables.py`)**:
  - Safe inspection by default (`--check`).
  - Requires explicit opt-in (`--create`) to provision resources.
  - Automatic schema and GSI mismatch detection.
  - Never deletes tables or data automatically.
- **Idempotent Catalogue Seeder CLI (`scripts/seed_dynamodb.py`)**:
  - Populates verified catalogue movies (28), venues (5), and demo showtimes (6).
  - Converts floating-point numbers to Python `Decimal` for DynamoDB compatibility.
  - **Strict Customer Protection Guard**: Under no circumstance will `users`, `bookings`, or `show_seats` tables be touched or overwritten by the seeder.
  - Supports safe read-only preview by default (`--check`) and explicit opt-in (`--seed`).

---

## 🚀 Phase 1.75: Verified Real Movie Posters & Image Integration

Phase 1.75 brings genuine, network-verified theatrical poster art from **The Movie Database (TMDB)** for all 28 catalogue titles across Anime, Marvel, and South Indian cinema, while adhering to TMDB's usage policies:

- **100% Genuine Theatrical Artwork**:
  - All 28 titles audited against TMDB CDN (`https://image.tmdb.org/t/p/w500/...`).
  - Network verified with HTTP 200 responses, standard 2:3 theatrical aspect ratios, and `object-fit: cover`.
  - Machine-readable manifest generated at `app/data/poster_manifest.json`.
- **Zero Runtime Dependency**:
  - Movie page requests load directly using verified static CDN URLs with graceful HTML/CSS local gradient fallback on image errors (`onerror`).
  - Core app functionality never makes live external API calls at user request time.
- **Repeatable Sync & Verification Utility (`scripts/sync_movie_posters.py`)**:
  - Audits catalogue against TMDB API or audited canonical fallback dataset.
  - Supports `--dry-run`, `--verify-urls` (HTTP network check), and `--update-data`.
- **Admin Live Poster Preview**:
  - Real-time client-side preview in the admin movie form (`/admin/movies/new` and `/admin/movies/<id>/edit`) with fallback testing.
- **TMDB Attribution**:
  - Mandatory TMDB footer badge and attribution statement: *"This product uses the TMDB API but is not endorsed or certified by TMDB."*

---

## 🚀 Phase 1.5: Real Movie Catalogue & Kolhapur Theatres

Phase 1.5 upgrades Movie Magic from generic placeholder data to a curated, verified cinema catalogue and real cinema venues in **Kolhapur, Maharashtra, India**, while enforcing a strict separation between catalogue films and actual bookable showtimes:

- **Curated Multi-Genre Catalogue (28 Titles)**:
  - **Anime (8 Titles)**: *Demon Slayer: Infinity Castle*, *Your Name.*, *Suzume*, *Jujutsu Kaisen 0*, *The First Slam Dunk*, *Spirited Away*, *Weathering with You*, *A Silent Voice*.
  - **Marvel (8 Titles)**: *Avengers: Endgame*, *Avengers: Infinity War*, *Spider-Man: No Way Home*, *Spider-Man: Across the Spider-Verse*, *Deadpool & Wolverine*, *Guardians of the Galaxy Vol. 3*, *Black Panther: Wakanda Forever*, *Doctor Strange in the Multiverse of Madness*.
  - **South Indian Cinema (12 Titles)**: *Pushpa 2: The Rule* (Telugu), *Kalki 2898 AD* (Telugu), *RRR* (Telugu), *Baahubali 2: The Conclusion* (Telugu), *K.G.F: Chapter 2* (Kannada), *Kantara* (Kannada), *Leo* (Tamil), *Vikram* (Tamil), *Jailer* (Tamil), *Manjummel Boys* (Malayalam), *Aavesham* (Malayalam), *Premalu* (Malayalam).
- **Real Kolhapur Cinema Venues**:
  - **PVR DYP City Mall**: Kavala Naka, Kolhapur (Verified, 3 Screens, District.in source reference).
  - **INOX Reliance Mega Mall**: Laxmipuri, Kolhapur (Verified, 4 Screens, CinemaTimes source reference).
  - **Prabhat Royal Cineplex**: Laxmipuri, Kolhapur (Verified, 2 Screens, BookMyShow source reference).
  - **Shahu Cinema**: Shahupuri / Laxmipuri, Kolhapur (Verified Heritage Single Screen, BookMyShow source reference).
  - **Padma Talkies**: Laxmipuri, Kolhapur (Unverified, Online Booking Disabled).
- **Catalogue vs. Showtime Distinction (Mandatory Guard)**:
  - A catalogue title does *not* imply it is currently screening.
  - Separate `Showtime` data model with status flags (`Verified` vs `Demo / Sample`).
  - Movies without showtimes prominently display: *"Showtimes not verified — check with the cinema directly"* alongside official external listings.
  - Fake bookings cannot be initiated for non-scheduled catalogue films or unverified venues.
- **Graceful Poster & Artwork Fallback**:
  - Official TMDB poster image paths with 2:3 responsive cards.
  - HTML `onerror` fallback that immediately reveals local CSS cinematic gradient art if offline or unresolvable.
  - Optional `TMDB_API_KEY` configuration documented; zero paid API dependency for core operations.
- **Admin Management Portal**:
  - Full CRUD operations for movies, cinema venues, and showtimes with `@admin_required` route protection.
  - One-click theatre operational status toggling and verification control.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.11+ / Flask 3.1 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons |
| **Security** | Werkzeug Security, Flask-WTF (CSRF), itsdangerous |
| **AWS SDK** | `boto3` (Centralized adapter with local/demo mock fallback) |
| **Database** | Amazon DynamoDB (`ap-south-1` Mumbai, on-demand PAY_PER_REQUEST, with mock fallback) |
| **Messaging** | Amazon SNS (Booking confirmation notifications with mock fallback) |
| **Hosting & Web Server** | Amazon EC2, Gunicorn (WSGI), Nginx reverse proxy |
| **Testing** | Pytest 8+ (139 automated tests) |

---

## 💻 Local Windows PowerShell Setup Instructions

### 1. Clone & Navigate to Project Directory
```powershell
git clone https://github.com/GKExpo/movie-magic.git
cd movie-magic
```

### 2. Activate Virtual Environment
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```
*(Or invoke `.\.venv\Scripts\python.exe` directly.)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template configuration file:
```powershell
Copy-Item .env.example .env
```

*(Optional) Configure a free TMDB API key in `.env`:*
```ini
TMDB_API_KEY=your_free_tmdb_api_key_here
```
*Note: Movie Magic functions out of the box without any third-party API key.*

### 5. Run the Automated Test Suite
Execute pytest to run the complete 139-test suite:
```powershell
.\.venv\Scripts\python.exe -m pytest
```
*Expected result: 139 passed in < 3.5 seconds.*

### 6. Inspect DynamoDB Table Schemas & Catalogue Seeder (Dry-Run)
Inspect table schemas and catalogue seeding data safely in read-only mode:
```powershell
# Inspect DynamoDB table definitions and schema checks (read-only)
.\.venv\Scripts\python.exe scripts/create_dynamodb_tables.py --check

# Dry-run inspection of catalogue movies and Kolhapur theatres dataset
.\.venv\Scripts\python.exe scripts/seed_dynamodb.py --check
```

### 7. Verify & Audit Movie Posters (Optional CLI Utility)
Audit and verify the 28 catalogue posters against TMDB CDN and local metadata:
```powershell
# Safe inspection / dry-run (no file modifications)
.\.venv\Scripts\python.exe scripts/sync_movie_posters.py --dry-run

# Network check (verifies HTTP 200 image responses over the network)
.\.venv\Scripts\python.exe scripts/sync_movie_posters.py --dry-run --verify-urls

# Update catalogue file and refresh poster manifest
.\.venv\Scripts\python.exe scripts/sync_movie_posters.py --update-data --verify-urls
```

### 8. Start the Flask Development Server
```powershell
python run.py
```

The application will start on:
- 🌐 **Web Interface:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- 🩺 **Health Check:** [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)

---

## 🔑 Pre-Configured Demo Accounts

| Role | Email | Password | Permissions |
|---|---|---|---|
| **Demo User** | `demo@moviemagic.com` | `Demo@123` | Browse catalogue, select seats, book demo tickets, view receipts |
| **Administrator** | `admin@moviemagic.com` | `Admin@123` | Full access to Admin Portal: add/edit movies, venues, showtimes |

---

## 🩺 Health Check Endpoint

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"
```
```json
{
  "status": "healthy",
  "service": "Movie Magic",
  "version": "1.75.0-verified-posters",
  "environment": "development",
  "default_city": "Kolhapur",
  "aws_mode": "mock/demo"
}
```

---

## 🚀 Amazon EC2 Production Deployment Guide

Follow this guide to deploy Movie Magic on an Amazon EC2 instance using **Gunicorn**, **Nginx**, and an **IAM Instance Role** with least-privilege permissions.

### Prerequisites & Architecture
- **AWS Region**: `ap-south-1` (Mumbai)
- **Instance Type**: `t3.micro` or `t2.micro` (AWS Free Tier eligible)
- **OS**: Amazon Linux 2023 (AL2023)
- **Security**: No AWS access keys on the server; credentials resolve automatically via the attached EC2 IAM Role.
- **Port Mapping**:
  - Inbound Port 80 (HTTP) -> Nginx Reverse Proxy -> Gunicorn WSGI (`127.0.0.1:5000`) -> Flask
  - Inbound Port 22 (SSH) -> Administrative access

---

### Step 1: Create the Least-Privilege IAM Role for EC2

1. Open **AWS Management Console** > **IAM** > **Policies** > **Create policy**.
2. Select the **JSON** tab and paste the contents of `deploy/iam-ec2-policy.json`.
3. Name the policy: `MovieMagicEC2AppPolicy`.
4. Navigate to **IAM** > **Roles** > **Create role**.
5. Choose **AWS service** as the trusted entity type and select **EC2**.
6. Attach the policy created above: `MovieMagicEC2AppPolicy`.
7. Name the role: `MovieMagicEC2Role` and click **Create role**.

---

### Step 2: (Optional) Create Amazon SNS Booking Notification Topic

If you want live email notifications dispatched for completed bookings:
1. Open **Amazon SNS** > **Topics** > **Create topic**.
2. Type: **Standard**.
3. Name: `moviemagic-booking-notifications`.
4. Click **Create topic**, then copy the generated **Topic ARN** (e.g. `arn:aws:sns:ap-south-1:123456789012:moviemagic-booking-notifications`).
5. Under **Subscriptions**, click **Create subscription**:
   - Protocol: `Email`
   - Endpoint: `your-email@example.com`
6. Click **Create subscription**.
7. Check your email inbox and click **"Confirm subscription"** in the verification email from AWS.

---

### Step 3: Launch the EC2 Instance

1. Open **EC2 Console** > **Instances** > **Launch instances**.
2. **Name**: `Movie-Magic-Production`.
3. **AMI**: Amazon Linux 2023 AMI (AL2023).
4. **Instance type**: `t3.micro` (or `t2.micro`).
5. **Key pair**: Select your existing key pair or create one.
6. **Network settings** > **Edit**:
   - Auto-assign public IP: **Enable**
   - Security group rule 1: SSH (Port 22) from `My IP`.
   - Security group rule 2: HTTP (Port 80) from `Anywhere (0.0.0.0/0)`.
7. **Advanced details** > **IAM instance profile**:
   - Select `MovieMagicEC2Role`.
8. Click **Launch instance**.

---

### Step 4: Run the Deployment Script

1. Connect to your EC2 instance via SSH or AWS EC2 Instance Connect:
   ```bash
   ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
   ```
2. Clone the repository and execute the automated setup script:
   ```bash
   git clone https://github.com/GKExpo/movie-magic.git
   cd movie-magic
   sudo bash deploy/ec2-setup.sh
   ```
3. If using Amazon SNS, edit the generated `.env` file to add your Topic ARN:
   ```bash
   nano /home/ec2-user/movie-magic/.env
   # Set: SNS_BOOKING_TOPIC_ARN=arn:aws:sns:ap-south-1:...
   # Save and restart the service:
   sudo systemctl restart moviemagic
   ```

---

### Step 5: Verification & End-to-End Testing

1. **Health Check Probe**:
   Open in your browser:
   `http://<EC2-PUBLIC-IP>/health`
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "Movie Magic",
     "version": "1.75.0-verified-posters",
     "environment": "production",
     "default_city": "Kolhapur",
     "aws_mode": "live"
   }
   ```
2. **Catalogue & Venue Browsing**:
   Visit `http://<EC2-PUBLIC-IP>/` to verify that all 28 movies, 5 Kolhapur theatres, and demo showtimes load live from DynamoDB.
3. **User Registration & Login**:
   Register a new account (e.g. `student@test.com`) with a strong password. Log in and verify that the session persists.
4. **Seat Selection & Booking**:
   Select a movie, choose seats (e.g. `C4`, `C5`), and complete the reservation. Verify the confirmation receipt displays with your booking reference.
5. **Atomic Concurrency Test**:
   Open an incognito window, log in as another user, and attempt to reserve the exact same seat (`C4`). Verify that the system cleanly rejects the reservation with:
   `"Seat C4 has already been reserved. Please choose another seat."`
6. **Inspect Application Logs**:
   ```bash
   # Live application logs
   journalctl -u moviemagic.service -f
   
   # Nginx access and error logs
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

---

## ⚖️ Legal & Partnership Disclaimer

Movie Magic is an educational demonstration project. It is **not** affiliated with, endorsed by, or in partnership with BookMyShow, District, PVR INOX Ltd., or any cinema operator. Live showtimes and ticket availability are determined solely by the respective theatre managements.

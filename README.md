# 🎬 Movie Magic

A modern, cloud-native movie ticket booking application built with **Flask**, designed for scalable deployment across **AWS** (Amazon DynamoDB, Amazon SNS, and Amazon EC2 with Gunicorn & Nginx).

---

## 🚀 Phase 2: Amazon DynamoDB Integration (Milestones 1 & 2 Complete)

Phase 2 transitions Movie Magic to a cloud-native AWS architecture using Amazon DynamoDB in the **`ap-south-1` (Mumbai)** region:

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
| **Messaging (Planned Phase 2)** | Amazon SNS (Booking Confirmation Emails) |
| **Hosting & Web Server** | Amazon EC2, Gunicorn (WSGI), Nginx reverse proxy |
| **Testing** | Pytest 8+ (92 automated tests) |

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
Execute pytest to run the complete 92-test suite:
```powershell
.\.venv\Scripts\python.exe -m pytest
```
*Expected result: 92 passed in < 3.0 seconds.*

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

## ⚖️ Legal & Partnership Disclaimer

Movie Magic is an educational demonstration project. It is **not** affiliated with, endorsed by, or in partnership with BookMyShow, District, PVR INOX Ltd., or any cinema operator. Live showtimes and ticket availability are determined solely by the respective theatre managements.

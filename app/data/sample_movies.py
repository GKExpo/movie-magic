"""Sample movie catalog, theater, and showtime dataset for development & testing.
All records in this module are clearly identified as DEMO / SAMPLE data.
"""

SAMPLE_CITIES = [
    "New York",
    "Los Angeles",
    "San Francisco",
    "Chicago",
    "London",
    "Mumbai"
]

SAMPLE_GENRES = [
    "All",
    "Sci-Fi",
    "Action",
    "Adventure",
    "Thriller",
    "Drama",
    "Animation"
]

SAMPLE_THEATERS = [
    {"id": "th-1", "name": "Starlight IMAX & Laser", "city": "New York", "screens": ["Screen 1 (IMAX)", "Screen 2 (Dolby)"]},
    {"id": "th-2", "name": "Galaxy Cinema Royale", "city": "New York", "screens": ["Screen 3", "Screen 4 (VIP)"]},
    {"id": "th-3", "name": "Eclipse CineDome", "city": "Los Angeles", "screens": ["Dome A", "Dome B (Dolby)"]},
    {"id": "th-4", "name": "Pacific Star Theaters", "city": "Los Angeles", "screens": ["Screen 1 (4DX)", "Screen 2"]},
    {"id": "th-5", "name": "Bayview Silver Screens", "city": "San Francisco", "screens": ["Auditorium 1", "Auditorium 2"]},
    {"id": "th-6", "name": "Midwest Grand Cinema", "city": "Chicago", "screens": ["Hall 1", "Hall 2 (IMAX)"]},
    {"id": "th-7", "name": "Regal Odeon Leicester", "city": "London", "screens": ["Screen 1 (IMAX)", "Screen 2"]},
    {"id": "th-8", "name": "PVR Icon Palladium", "city": "Mumbai", "screens": ["Audi 1 (IMAX 3D)", "Audi 2 (4DX)"]}
]

SAMPLE_MOVIES = [
    {
        "id": "mov-1",
        "title": "Cosmic Odyssey: Beyond the Nebula",
        "tagline": "The furthest journey begins within.",
        "genre": "Sci-Fi",
        "duration": "2h 45m",
        "duration_minutes": 165,
        "rating": "PG-13",
        "imdb_score": 8.9,
        "release_year": 2026,
        "director": "Elena Vance",
        "cast": ["Marcus Reed", "Aria Jensen", "Kaelen Chen", "David O'Connor"],
        "synopsis": "When a deep space telemetry array picks up an anomalous resonance from the edge of the Perseus Arm, a crew of exploratory scientists embarks on a high-stakes interstellar voyage through uncharted gravitational anomalies.",
        "format": "IMAX 3D / Dolby Atmos",
        "is_featured": True,
        "badge": "Trending #1",
        "poster_color": "#1e1b4b",
        "accent_color": "#6366f1",
        "bg_gradient": "linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%)",
        "showtimes": [
            {"time": "10:30 AM", "format": "IMAX 3D", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"},
            {"time": "02:15 PM", "format": "Dolby Atmos", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"},
            {"time": "06:00 PM", "format": "IMAX 3D", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"},
            {"time": "09:45 PM", "format": "Standard", "screen": "Screen 2", "price_tier": "Gold"}
        ]
    },
    {
        "id": "mov-2",
        "title": "Shadow Protocol: Neon Nights",
        "tagline": "In a city without shadows, secrets are deadly.",
        "genre": "Action",
        "duration": "2h 18m",
        "duration_minutes": 138,
        "rating": "R",
        "imdb_score": 8.5,
        "release_year": 2026,
        "director": "Kenji Sato",
        "cast": ["Tatsuo Jin", "Clara Montgomery", "Vikram Patel", "Maya Lin"],
        "synopsis": "An ex-intelligence operative is pulled out of hiding when a rogue algorithmic syndicate hijacks the orbital surveillance grid in a sprawling futuristic metropolis.",
        "format": "Dolby Vision / 4DX",
        "is_featured": True,
        "badge": "Blockbuster",
        "poster_color": "#172554",
        "accent_color": "#0ea5e9",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%)",
        "showtimes": [
            {"time": "11:00 AM", "format": "Standard", "screen": "Screen 2", "price_tier": "Silver"},
            {"time": "03:30 PM", "format": "4DX", "screen": "Screen 1 (4DX)", "price_tier": "VIP"},
            {"time": "07:15 PM", "format": "Dolby Vision", "screen": "Screen 3", "price_tier": "Gold"},
            {"time": "10:30 PM", "format": "Dolby Vision", "screen": "Screen 3", "price_tier": "Gold"}
        ]
    },
    {
        "id": "mov-3",
        "title": "The Glass Fortress",
        "tagline": "Every illusion has a breaking point.",
        "genre": "Thriller",
        "duration": "1h 56m",
        "duration_minutes": 116,
        "rating": "PG-13",
        "imdb_score": 8.2,
        "release_year": 2026,
        "director": "Sophie Laurent",
        "cast": ["Emma Watson-Greene", "Liam Gallagher", "Noah Sterling"],
        "synopsis": "A brilliant forensic psychologist is trapped inside an ultra-secure automated high-altitude alpine retreat with five suspects who all share the same forgotten past.",
        "format": "Digital 4K",
        "is_featured": False,
        "badge": "Critically Acclaimed",
        "poster_color": "#3b0764",
        "accent_color": "#a855f7",
        "bg_gradient": "linear-gradient(135deg, #2e1065 0%, #3b0764 50%, #581c87 100%)",
        "showtimes": [
            {"time": "12:00 PM", "format": "Digital 4K", "screen": "Screen 4", "price_tier": "Silver"},
            {"time": "04:45 PM", "format": "Digital 4K", "screen": "Screen 4", "price_tier": "Gold"},
            {"time": "08:30 PM", "format": "Digital 4K", "screen": "Screen 4", "price_tier": "Gold"}
        ]
    },
    {
        "id": "mov-4",
        "title": "Aetheria: Flight of the Sunbird",
        "tagline": "Hope has wings.",
        "genre": "Animation",
        "duration": "1h 44m",
        "duration_minutes": 104,
        "rating": "PG",
        "imdb_score": 8.7,
        "release_year": 2026,
        "director": "Mateo Morales",
        "cast": ["Zoe Martinez (voice)", "Oliver Grant (voice)", "Samira Khan (voice)"],
        "synopsis": "In a floating archipelago powered by crystalline winds, an intrepid young mechanic and a mythical winged guardian embark on an adventure to reignite the Great Solar Beacon.",
        "format": "RealD 3D / Atmos",
        "is_featured": False,
        "badge": "Family Favorite",
        "poster_color": "#701a75",
        "accent_color": "#ec4899",
        "bg_gradient": "linear-gradient(135deg, #4a044e 0%, #701a75 50%, #9d174d 100%)",
        "showtimes": [
            {"time": "10:00 AM", "format": "RealD 3D", "screen": "Screen 2", "price_tier": "Silver"},
            {"time": "01:15 PM", "format": "RealD 3D", "screen": "Screen 2", "price_tier": "Gold"},
            {"time": "04:00 PM", "format": "Standard", "screen": "Screen 2", "price_tier": "Silver"}
        ]
    },
    {
        "id": "mov-5",
        "title": "Quantum Horizon",
        "tagline": "Time is no longer a straight line.",
        "genre": "Sci-Fi",
        "duration": "2h 30m",
        "duration_minutes": 150,
        "rating": "PG-13",
        "imdb_score": 8.4,
        "release_year": 2026,
        "director": "Nolan Drake",
        "cast": ["Christian Bale-Smith", "Jessica Chastain-Lee", "Hiroyuki Sanada"],
        "synopsis": "A team of theoretical physicists accidentally open a stable temporal conduit, forcing them to navigate shifting timelines to save Earth from a synthetic cascade event.",
        "format": "70mm IMAX",
        "is_featured": True,
        "badge": "Popular",
        "poster_color": "#064e3b",
        "accent_color": "#10b981",
        "bg_gradient": "linear-gradient(135deg, #022c22 0%, #064e3b 50%, #047857 100%)",
        "showtimes": [
            {"time": "11:30 AM", "format": "70mm IMAX", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"},
            {"time": "03:45 PM", "format": "70mm IMAX", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"},
            {"time": "07:30 PM", "format": "70mm IMAX", "screen": "Screen 1 (IMAX)", "price_tier": "VIP"}
        ]
    },
    {
        "id": "mov-6",
        "title": "Apex Legends: Origins",
        "tagline": "Heroes are made in the fire of competition.",
        "genre": "Action",
        "duration": "2h 05m",
        "duration_minutes": 125,
        "rating": "PG-13",
        "imdb_score": 7.9,
        "release_year": 2026,
        "director": "Chad Stahelski Jr.",
        "cast": ["Jordan Vance", "Sasha Banks", "Dave Bautista"],
        "synopsis": "Across the frontier of the Outlands, elite combatants battle in tactical arenas where teamwork, agility, and cutting-edge combat engineering dictate survival.",
        "format": "IMAX / Dolby Atmos",
        "is_featured": False,
        "badge": "Action Packed",
        "poster_color": "#7c2d12",
        "accent_color": "#f97316",
        "bg_gradient": "linear-gradient(135deg, #431407 0%, #7c2d12 50%, #c2410c 100%)",
        "showtimes": [
            {"time": "01:00 PM", "format": "Standard", "screen": "Screen 3", "price_tier": "Silver"},
            {"time": "05:15 PM", "format": "Dolby Atmos", "screen": "Screen 3", "price_tier": "Gold"},
            {"time": "09:00 PM", "format": "Dolby Atmos", "screen": "Screen 3", "price_tier": "Gold"}
        ]
    }
]

# Standard Seat Tier Definitions
SEAT_TIERS = {
    "VIP": {"name": "VIP Recliner", "price": 22.00, "rows": ["A", "B"], "badge_color": "warning"},
    "Gold": {"name": "Premium Gold", "price": 16.00, "rows": ["C", "D", "E"], "badge_color": "info"},
    "Silver": {"name": "Standard Silver", "price": 12.00, "rows": ["F", "G", "H"], "badge_color": "secondary"}
}

# Standard 8x10 Grid for Theater Layout (A to H, 1 to 10)
TOTAL_ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
SEATS_PER_ROW = 10

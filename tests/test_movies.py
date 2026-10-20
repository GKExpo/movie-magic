"""Tests for curated movie catalogue, categories, Kolhapur theatres, and filtering."""


def test_index_page_loads(client):
    """Verify home page loads successfully with Kolhapur as default and real catalogue."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Movie Magic" in response.data
    assert b"Kolhapur" in response.data
    assert b"Pushpa 2: The Rule" in response.data
    assert b"PVR DYP City Mall" in response.data


def test_kolhapur_default_location(client):
    """Verify Kolhapur is selected as the default location."""
    response = client.get("/")
    assert response.status_code == 200
    # Verified venue in Kolhapur
    assert b"Cinema Venues in Kolhapur" in response.data


def test_movies_catalog_loads(client):
    """Verify full movie catalogue view loads with curated categories."""
    response = client.get("/movies")
    assert response.status_code == 200
    assert b"Curated Movie Catalogue" in response.data
    assert b"Demon Slayer" in response.data
    assert b"Avengers: Endgame" in response.data
    assert b"Pushpa 2: The Rule" in response.data


def test_category_filter_anime(client):
    """Verify Anime category filtering returns anime titles only."""
    response = client.get("/movies?category=Anime")
    assert response.status_code == 200
    assert b"Demon Slayer" in response.data
    assert b"Your Name." in response.data
    assert b"Suzume" in response.data
    assert b"Avengers: Endgame" not in response.data
    assert b"Pushpa 2" not in response.data


def test_category_filter_marvel(client):
    """Verify Marvel category filtering returns Marvel titles."""
    response = client.get("/movies?category=Marvel")
    assert response.status_code == 200
    assert b"Avengers: Endgame" in response.data
    assert b"Spider-Man: Across the Spider-Verse" in response.data
    assert b"Deadpool &amp; Wolverine" in response.data or b"Deadpool & Wolverine" in response.data
    assert b"Your Name." not in response.data
    assert b"Kalki 2898 AD" not in response.data


def test_category_filter_south_indian(client):
    """Verify South Indian category filtering returns regional cinema titles."""
    response = client.get("/movies?category=South Indian")
    assert response.status_code == 200
    assert b"Pushpa 2: The Rule" in response.data
    assert b"Kalki 2898 AD" in response.data
    assert b"RRR" in response.data
    assert b"Manjummel Boys" in response.data
    assert b"Avengers: Endgame" not in response.data
    assert b"Suzume" not in response.data


def test_language_filter(client):
    """Verify language filtering works for Japanese, Telugu, and Malayalam."""
    # Test Japanese
    res_ja = client.get("/movies?language=Japanese")
    assert res_ja.status_code == 200
    assert b"Demon Slayer" in res_ja.data
    assert b"Pushpa 2" not in res_ja.data

    # Test Malayalam
    res_ml = client.get("/movies?language=Malayalam")
    assert res_ml.status_code == 200
    assert b"Manjummel Boys" in res_ml.data
    assert b"Aavesham" in res_ml.data
    assert b"Avengers: Endgame" not in res_ml.data


def test_movie_search_filter(client):
    """Test searching by title query across real movies."""
    response = client.get("/movies?q=Kalki")
    assert response.status_code == 200
    assert b"Kalki 2898 AD" in response.data
    assert b"Your Name." not in response.data


def test_kolhapur_theaters_and_sources(client):
    """Verify real Kolhapur cinema venues and public source listing URLs."""
    response = client.get("/")
    assert response.status_code == 200
    # PVR DYP City Mall
    assert b"PVR DYP City Mall" in response.data
    assert b"Kavala Naka" in response.data
    assert b"district.in" in response.data
    # INOX Reliance Mega Mall
    assert b"INOX Reliance Mega Mall" in response.data
    assert b"Laxmipuri" in response.data
    assert b"cinematimes.in" in response.data
    # Prabhat Royal Cineplex
    assert b"Prabhat Royal Cineplex" in response.data
    # Shahu Cinema
    assert b"Shahu Cinema" in response.data


def test_unverified_theater_status(client):
    """Verify unverified theatre (Padma Talkies) is visibly marked and not confirmed operational."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Padma Talkies" in response.data
    assert b"Unverified" in response.data


def test_movie_detail_page_with_demo_showtimes(client):
    """Test movie details for film with demo showtimes displays visible demo notice."""
    response = client.get("/movies/mov-south-1")
    assert response.status_code == 200
    assert b"Pushpa 2: The Rule" in response.data
    assert b"Sukumar" in response.data
    assert b"DEMO DATA NOTICE" in response.data
    assert b"Select Seats (Demo)" in response.data


def test_movie_detail_without_showtimes_shows_referral(client):
    """Test catalogue movie without active showtimes displays 'Showtimes not verified' notice."""
    response = client.get("/movies/mov-anime-2")  # Your Name (catalogue only)
    assert response.status_code == 200
    assert b"Your Name." in response.data
    assert b"Showtimes not verified" in response.data
    assert b"district.in" in response.data or b"bookmyshow.com" in response.data


def test_movie_detail_not_found(client):
    """Test 404 for nonexistent movie."""
    response = client.get("/movies/mov-nonexistent-999")
    assert response.status_code == 404
    assert b"404" in response.data

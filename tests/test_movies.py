"""Tests for movie catalog, browsing, filtering, and detail views."""


def test_index_page_loads(client):
    """Verify home page loads successfully with featured movies."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Movie Magic" in response.data
    assert b"Now Showing" in response.data
    assert b"Cosmic Odyssey" in response.data


def test_movies_catalog_loads(client):
    """Verify full movie catalog view."""
    response = client.get("/movies")
    assert response.status_code == 200
    assert b"Movie Catalog" in response.data
    assert b"Shadow Protocol" in response.data


def test_movie_search_filter(client):
    """Test searching by title query."""
    response = client.get("/movies?q=Odyssey")
    assert response.status_code == 200
    assert b"Cosmic Odyssey" in response.data
    assert b"Apex Legends" not in response.data


def test_movie_genre_filter(client):
    """Test filtering by movie genre."""
    response = client.get("/movies?genre=Animation")
    assert response.status_code == 200
    assert b"Aetheria" in response.data
    assert b"Shadow Protocol" not in response.data


def test_movie_detail_page(client):
    """Test movie details and showtimes display."""
    response = client.get("/movies/mov-1")
    assert response.status_code == 200
    assert b"Cosmic Odyssey" in response.data
    assert b"Select Showtime &amp; Theater" in response.data or b"Select Showtime & Theater" in response.data
    assert b"Elena Vance" in response.data


def test_movie_detail_not_found(client):
    """Test 404 for nonexistent movie."""
    response = client.get("/movies/mov-nonexistent-999")
    assert response.status_code == 404
    assert b"404" in response.data

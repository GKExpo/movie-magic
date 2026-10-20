"""Tests for administrator dashboard, role-based access control, and inventory operations."""


def test_admin_dashboard_anonymous_redirected(client):
    """Anonymous visitor must be redirected to sign in."""
    response = client.get("/admin/", follow_redirects=False)
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_dashboard_regular_user_forbidden(auth_client):
    """Regular user accessing admin dashboard receives 403 Forbidden."""
    response = auth_client.get("/admin/")
    assert response.status_code == 403
    assert b"403" in response.data or b"Forbidden" in response.data


def test_admin_dashboard_admin_allowed(admin_client):
    """Administrator accessing admin dashboard receives 200 OK."""
    response = admin_client.get("/admin/")
    assert response.status_code == 200
    assert b"Operational Management" in response.data
    assert b"Simulated Revenue" in response.data


def test_admin_add_movie(admin_client):
    """Admin can successfully add a new movie to schedule."""
    response = admin_client.post(
        "/admin/movies/new",
        data={
            "title": "Quantum Odyssey Test",
            "tagline": "Beyond all known boundaries",
            "genre": "Sci-Fi",
            "duration": "2h 10m",
            "rating": "PG-13",
            "imdb_score": 8.8,
            "release_year": 2026,
            "director": "Christopher Vance",
            "format": "IMAX 3D",
            "synopsis": "A test synopsis for admin testing.",
            "badge": "Premiere",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Quantum Odyssey Test" in response.data


def test_admin_delete_movie(admin_client):
    """Admin can delete a movie from schedule."""
    response = admin_client.post("/admin/movies/mov-6/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"Movie removed from catalog" in response.data

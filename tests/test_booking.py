"""Tests for seat selection, booking flow, price calculation, and duplicate prevention."""
import json
from app.services import booking_service


def test_seat_selection_page_loads(client):
    """Verify seat selection view renders screen and seating grid."""
    response = client.get("/book/seats/mov-1")
    assert response.status_code == 200
    assert b"CINEMATIC SCREEN" in response.data
    assert b"Booking Summary" in response.data


def test_seat_booking_price_calculation():
    """Verify tiered seat pricing calculation."""
    # Row A (VIP) = $22.00
    price_vip, tier_vip = booking_service.calculate_total(["A1"])
    assert price_vip == 22.00
    assert "VIP" in tier_vip

    # Row D (Gold) = $16.00
    price_gold, tier_gold = booking_service.calculate_total(["D1"])
    assert price_gold == 16.00
    assert "Gold" in tier_gold

    # Row G (Silver) = $12.00
    price_silver, tier_silver = booking_service.calculate_total(["G1"])
    assert price_silver == 12.00
    assert "Silver" in tier_silver

    # Multiple seats: A1 ($22) + G1 ($12) = $34.00
    price_combo, tier_combo = booking_service.calculate_total(["A1", "G1"])
    assert price_combo == 34.00


def test_unauthenticated_user_redirected_on_booking(client):
    """Anonymous user attempting to submit booking is redirected to login."""
    response = client.post(
        "/book/confirm",
        data={
            "movie_id": "mov-1",
            "theater_id": "th-1",
            "showtime": "10:30 AM",
            "show_date": "Today",
            "selected_seats": json.dumps(["F1", "F2"]),
        },
        follow_redirects=False,
    )
    # Redirects to login
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_authenticated_user_booking_flow(auth_client):
    """Logged in user can successfully complete a booking."""
    response = auth_client.post(
        "/book/confirm",
        data={
            "movie_id": "mov-1",
            "theater_id": "th-1",
            "showtime": "10:30 AM",
            "show_date": "Today",
            "selected_seats": json.dumps(["B1", "B2"]),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"RESERVATION CONFIRMED" in response.data
    assert b"B1" in response.data
    assert b"B2" in response.data


def test_duplicate_seat_booking_prevention(auth_client):
    """Attempting to book an already occupied seat should be rejected."""
    # First booking: reserve H8
    success1, _, _ = booking_service.create_booking(
        user_id="usr-demo-1",
        user_email="demo@moviemagic.com",
        movie_id="mov-1",
        theater_id="th-1",
        showtime="10:30 AM",
        show_date="Today",
        seats=["H8"],
    )
    assert success1 is True

    # Second booking attempting the same seat H8: should fail
    success2, msg, _ = booking_service.create_booking(
        user_id="usr-demo-1",
        user_email="demo@moviemagic.com",
        movie_id="mov-1",
        theater_id="th-1",
        showtime="10:30 AM",
        show_date="Today",
        seats=["H8"],
    )
    assert success2 is False
    assert "already been reserved" in msg


def test_booking_history_page(auth_client):
    """Verify user booking history page displays bookings."""
    response = auth_client.get("/bookings/history")
    assert response.status_code == 200
    assert b"My Booking History" in response.data
    assert b"CONFIRMED" in response.data

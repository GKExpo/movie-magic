"""Booking Repository (In-Memory Phase 1, DynamoDB ready for Phase 2)."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from .base import BaseRepository


class BookingRepository(BaseRepository):
    """Booking data access repository."""

    def __init__(self):
        self._bookings: Dict[str, Dict[str, Any]] = {}
        # Key: (movie_id, theater_id, showtime) -> set of booked seat codes (e.g. 'A1', 'C4')
        self._occupied_seats: Dict[str, Set[str]] = {}
        self._seed_sample_bookings()

    def _get_show_key(self, movie_id: str, theater_id: str, showtime: str) -> str:
        return f"{movie_id}#{theater_id}#{showtime}"

    def _seed_sample_bookings(self):
        """Seed initial realistic booked seats and demo booking record."""
        # Pre-reserve a few seats for demo realism
        key1 = self._get_show_key("mov-1", "th-1", "10:30 AM")
        self._occupied_seats[key1] = {"A4", "A5", "C6", "C7", "D3"}

        key2 = self._get_show_key("mov-2", "th-3", "03:30 PM")
        self._occupied_seats[key2] = {"B4", "B5", "E1", "E2"}

        sample_booking = {
            "id": "MM-2026-DEMO-001",
            "user_id": "usr-demo-1",
            "user_email": "demo@moviemagic.com",
            "movie_id": "mov-1",
            "movie_title": "Cosmic Odyssey: Beyond the Nebula",
            "theater_id": "th-1",
            "theater_name": "Starlight IMAX & Laser (New York)",
            "showtime": "10:30 AM",
            "show_date": "Today",
            "seats": ["A4", "A5"],
            "tier": "VIP",
            "ticket_count": 2,
            "total_price": 44.00,
            "status": "CONFIRMED (DEMO)",
            "is_demo": True,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        }
        self._bookings[sample_booking["id"]] = sample_booking

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self._bookings.get(item_id)

    def get_all(self) -> List[Dict[str, Any]]:
        return sorted(
            list(self._bookings.values()),
            key=lambda x: x.get("created_at", ""),
            reverse=True,
        )

    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        return sorted(
            [b for b in self._bookings.values() if b.get("user_id") == user_id],
            key=lambda x: x.get("created_at", ""),
            reverse=True,
        )

    def get_booked_seats(self, movie_id: str, theater_id: str, showtime: str) -> List[str]:
        key = self._get_show_key(movie_id, theater_id, showtime)
        return sorted(list(self._occupied_seats.get(key, set())))

    def create_booking(
        self,
        user_id: str,
        user_email: str,
        movie_id: str,
        movie_title: str,
        theater_id: str,
        theater_name: str,
        showtime: str,
        show_date: str,
        seats: List[str],
        tier: str,
        total_price: float,
    ) -> Dict[str, Any]:
        """Create and record a booking."""
        show_key = self._get_show_key(movie_id, theater_id, showtime)
        if show_key not in self._occupied_seats:
            self._occupied_seats[show_key] = set()

        # Check for seat collision
        for seat in seats:
            if seat in self._occupied_seats[show_key]:
                raise ValueError(f"Seat {seat} has already been reserved. Please choose another seat.")

        # Mark seats as reserved
        for seat in seats:
            self._occupied_seats[show_key].add(seat)

        booking_id = f"MM-2026-{uuid.uuid4().hex[:6].upper()}"
        booking = {
            "id": booking_id,
            "user_id": user_id,
            "user_email": user_email,
            "movie_id": movie_id,
            "movie_title": movie_title,
            "theater_id": theater_id,
            "theater_name": theater_name,
            "showtime": showtime,
            "show_date": show_date,
            "seats": seats,
            "tier": tier,
            "ticket_count": len(seats),
            "total_price": total_price,
            "status": "CONFIRMED (DEMO)",
            "is_demo": True,
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        }
        self._bookings[booking_id] = booking
        return booking


# Singleton instance for in-memory session persistence
booking_repository = BookingRepository()

"""Booking Service.
Coordinates seat reservation, price calculation, validation, and notification dispatch.
"""
from typing import List, Dict, Any, Optional, Tuple
from app.repositories import booking_repository, movie_repository
from app.aws.sns import SNSService
from app.data.sample_movies import TOTAL_ROWS, SEATS_PER_ROW, SEAT_TIERS


class BookingService:
    """Business logic for reservations, seat map generation, and booking receipts."""

    def __init__(self, repo=booking_repository, movie_repo=movie_repository):
        self.repo = repo
        self.movie_repo = movie_repo
        self.sns_service = SNSService()

    def get_seat_layout(self, movie_id: str, theater_id: str, showtime: str) -> Dict[str, Any]:
        """Generate interactive seat grid with current reserved states and tiers."""
        booked_seats = set(self.repo.get_booked_seats(movie_id, theater_id, showtime))

        rows_data = []
        for row_letter in TOTAL_ROWS:
            # Determine tier for this row
            row_tier = "Silver"
            price = 12.00
            for tier_name, tier_info in SEAT_TIERS.items():
                if row_letter in tier_info["rows"]:
                    row_tier = tier_name
                    price = tier_info["price"]
                    break

            seats_in_row = []
            for num in range(1, SEATS_PER_ROW + 1):
                seat_id = f"{row_letter}{num}"
                is_booked = seat_id in booked_seats
                seats_in_row.append({
                    "id": seat_id,
                    "row": row_letter,
                    "number": num,
                    "tier": row_tier,
                    "price": price,
                    "is_booked": is_booked,
                })

            rows_data.append({
                "row_letter": row_letter,
                "tier": row_tier,
                "price": price,
                "seats": seats_in_row,
            })

        return {
            "rows": rows_data,
            "tiers": SEAT_TIERS,
            "total_rows": TOTAL_ROWS,
            "seats_per_row": SEATS_PER_ROW,
            "booked_count": len(booked_seats),
        }

    def calculate_total(self, seats: List[str]) -> Tuple[float, str]:
        """Calculate total price based on selected seats and their row tiers."""
        if not seats:
            return 0.0, "None"

        total = 0.0
        tiers_used = set()
        for seat in seats:
            row_letter = seat[0].upper()
            seat_price = 12.00  # Default
            for tier_name, tier_info in SEAT_TIERS.items():
                if row_letter in tier_info["rows"]:
                    seat_price = tier_info["price"]
                    tiers_used.add(tier_name)
                    break
            total += seat_price

        tier_summary = ", ".join(sorted(tiers_used)) if tiers_used else "Standard"
        return round(total, 2), tier_summary

    def create_booking(
        self,
        user_id: str,
        user_email: str,
        movie_id: str,
        theater_id: str,
        showtime: str,
        show_date: str,
        seats: List[str],
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Validate and create a movie ticket booking."""
        if not seats:
            return False, "Please select at least one seat to proceed.", None

        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            return False, "Selected movie not found.", None

        theater = self.movie_repo.get_theater_by_id(theater_id)
        theater_name = theater["name"] if theater else "Premier Cinema"

        total_price, tier = self.calculate_total(seats)

        try:
            booking = self.repo.create_booking(
                user_id=user_id,
                user_email=user_email,
                movie_id=movie_id,
                movie_title=movie["title"],
                theater_id=theater_id,
                theater_name=theater_name,
                showtime=showtime,
                show_date=show_date,
                seats=seats,
                tier=tier,
                total_price=total_price,
            )

            # Trigger simulated or real SNS notification
            self.sns_service.publish_booking_confirmation(booking)

            return True, "Booking confirmed successfully!", booking
        except ValueError as e:
            return False, str(e), None

    def get_booking(self, booking_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(booking_id)

    def get_user_bookings(self, user_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_by_user_id(user_id)

    def get_all_bookings(self) -> List[Dict[str, Any]]:
        return self.repo.get_all()


booking_service = BookingService()

"""Movie & Theater Repository (In-Memory Phase 1, DynamoDB ready for Phase 2)."""
import uuid
from typing import Any, Dict, List, Optional
from app.data.sample_movies import (
    SAMPLE_MOVIES,
    SAMPLE_THEATERS,
    SAMPLE_CITIES,
    SAMPLE_GENRES,
    SEAT_TIERS,
)
from .base import BaseRepository


class MovieRepository(BaseRepository):
    """Movie catalog data access repository."""

    def __init__(self):
        self._movies: Dict[str, Dict[str, Any]] = {}
        self._theaters: Dict[str, Dict[str, Any]] = {}
        self._cities: List[str] = list(SAMPLE_CITIES)
        self._genres: List[str] = list(SAMPLE_GENRES)
        self._seed_data()

    def _seed_data(self):
        for movie in SAMPLE_MOVIES:
            self._movies[movie["id"]] = dict(movie)
        for theater in SAMPLE_THEATERS:
            self._theaters[theater["id"]] = dict(theater)

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self._movies.get(item_id)

    def get_all(
        self,
        city: Optional[str] = None,
        genre: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(self._movies.values())

        if genre and genre != "All":
            results = [m for m in results if m.get("genre", "").lower() == genre.lower()]

        if search_query:
            query = search_query.strip().lower()
            results = [
                m for m in results
                if query in m.get("title", "").lower()
                or query in m.get("synopsis", "").lower()
                or query in m.get("director", "").lower()
                or any(query in actor.lower() for actor in m.get("cast", []))
            ]

        return results

    def get_theaters(self, city: Optional[str] = None) -> List[Dict[str, Any]]:
        theaters = list(self._theaters.values())
        if city and city != "All":
            theaters = [t for t in theaters if t.get("city", "").lower() == city.lower()]
        return theaters

    def get_theater_by_id(self, theater_id: str) -> Optional[Dict[str, Any]]:
        return self._theaters.get(theater_id)

    def get_cities(self) -> List[str]:
        return list(self._cities)

    def get_genres(self) -> List[str]:
        return list(self._genres)

    def get_seat_tiers(self) -> Dict[str, Any]:
        return dict(SEAT_TIERS)

    def add_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        movie_id = movie_data.get("id") or f"mov-{uuid.uuid4().hex[:8]}"
        new_movie = dict(movie_data)
        new_movie["id"] = movie_id
        if "badge" not in new_movie:
            new_movie["badge"] = "New Release"
        if "poster_color" not in new_movie:
            new_movie["poster_color"] = "#1e293b"
        if "accent_color" not in new_movie:
            new_movie["accent_color"] = "#6366f1"
        if "bg_gradient" not in new_movie:
            new_movie["bg_gradient"] = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)"
        self._movies[movie_id] = new_movie
        return new_movie

    def delete_movie(self, movie_id: str) -> bool:
        if movie_id in self._movies:
            del self._movies[movie_id]
            return True
        return False


# Singleton instance for in-memory session persistence
movie_repository = MovieRepository()

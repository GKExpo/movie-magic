"""Movie, Theater & Showtime Repository (In-Memory Phase 1.5, DynamoDB ready for Phase 2)."""
import uuid
from typing import Any, Dict, List, Optional
from app.data.sample_movies import (
    SAMPLE_MOVIES,
    SAMPLE_THEATERS,
    SAMPLE_SHOWTIMES,
    SAMPLE_CITIES,
    SAMPLE_CATEGORIES,
    SAMPLE_LANGUAGES,
    SAMPLE_GENRES,
    SEAT_TIERS,
)
from .base import BaseRepository


class MovieRepository(BaseRepository):
    """Movie catalog, cinema venue, and showtime data access repository."""

    def __init__(self):
        self._movies: Dict[str, Dict[str, Any]] = {}
        self._theaters: Dict[str, Dict[str, Any]] = {}
        self._showtimes: Dict[str, Dict[str, Any]] = {}
        self._cities: List[str] = list(SAMPLE_CITIES)
        self._categories: List[str] = list(SAMPLE_CATEGORIES)
        self._languages: List[str] = list(SAMPLE_LANGUAGES)
        self._genres: List[str] = list(SAMPLE_GENRES)
        self._seed_data()

    def _seed_data(self):
        for movie in SAMPLE_MOVIES:
            self._movies[movie["id"]] = dict(movie)
        for theater in SAMPLE_THEATERS:
            self._theaters[theater["id"]] = dict(theater)
        for show in SAMPLE_SHOWTIMES:
            self._showtimes[show["id"]] = dict(show)

    # -------------------------------------------------------------------------
    # Movie Catalog Queries
    # -------------------------------------------------------------------------
    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self._movies.get(item_id)

    def get_all(
        self,
        city: Optional[str] = None,
        genre: Optional[str] = None,
        category: Optional[str] = None,
        language: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(self._movies.values())

        if category and category != "All":
            results = [m for m in results if m.get("category", "").lower() == category.lower()]

        if genre and genre != "All":
            results = [m for m in results if genre.lower() in m.get("genre", "").lower()]

        if language and language != "All":
            results = [
                m for m in results
                if m.get("language", "").lower() == language.lower()
                or any(language.lower() in d.lower() for d in m.get("dubbed_languages", []))
            ]

        if search_query:
            query = search_query.strip().lower()
            results = [
                m for m in results
                if query in m.get("title", "").lower()
                or query in m.get("original_title", "").lower()
                or query in m.get("synopsis", "").lower()
                or query in m.get("director", "").lower()
                or query in m.get("genre", "").lower()
                or query in m.get("category", "").lower()
                or query in m.get("language", "").lower()
                or any(query in actor.lower() for actor in m.get("cast", []))
            ]

        return results

    def add_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        movie_id = movie_data.get("id") or f"mov-{uuid.uuid4().hex[:8]}"
        new_movie = dict(movie_data)
        new_movie["id"] = movie_id
        if "badge" not in new_movie:
            new_movie["badge"] = "New Release"
        if "category" not in new_movie:
            new_movie["category"] = "General"
        if "language" not in new_movie:
            new_movie["language"] = "English"
        if "poster_color" not in new_movie:
            new_movie["poster_color"] = "#1e293b"
        if "accent_color" not in new_movie:
            new_movie["accent_color"] = "#6366f1"
        if "bg_gradient" not in new_movie:
            new_movie["bg_gradient"] = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)"
        self._movies[movie_id] = new_movie
        return new_movie

    def update_movie(self, movie_id: str, movie_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if movie_id not in self._movies:
            return None
        self._movies[movie_id].update(movie_data)
        return self._movies[movie_id]

    def delete_movie(self, movie_id: str) -> bool:
        if movie_id in self._movies:
            del self._movies[movie_id]
            # Also clean up associated showtimes
            self._showtimes = {
                s_id: s for s_id, s in self._showtimes.items() if s.get("movie_id") != movie_id
            }
            return True
        return False

    # -------------------------------------------------------------------------
    # Theater Venue Queries
    # -------------------------------------------------------------------------
    def get_theaters(self, city: Optional[str] = None, operational_only: bool = False) -> List[Dict[str, Any]]:
        theaters = list(self._theaters.values())
        if city and city != "All":
            theaters = [t for t in theaters if t.get("city", "").lower() == city.lower()]
        if operational_only:
            theaters = [
                t for t in theaters
                if t.get("operational_status") == "Operational" and t.get("is_verified") is True
            ]
        return theaters

    def get_theater_by_id(self, theater_id: str) -> Optional[Dict[str, Any]]:
        return self._theaters.get(theater_id)

    def add_theater(self, theater_data: Dict[str, Any]) -> Dict[str, Any]:
        theater_id = theater_data.get("id") or f"th-{uuid.uuid4().hex[:8]}"
        new_th = dict(theater_data)
        new_th["id"] = theater_id
        self._theaters[theater_id] = new_th
        return new_th

    def update_theater(self, theater_id: str, theater_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if theater_id not in self._theaters:
            return None
        self._theaters[theater_id].update(theater_data)
        return self._theaters[theater_id]

    # -------------------------------------------------------------------------
    # Showtime Queries (Separated from Movies)
    # -------------------------------------------------------------------------
    def get_showtimes(
        self,
        movie_id: Optional[str] = None,
        theater_id: Optional[str] = None,
        date: Optional[str] = None,
        verified_only: bool = False,
    ) -> List[Dict[str, Any]]:
        shows = list(self._showtimes.values())

        if movie_id:
            shows = [s for s in shows if s.get("movie_id") == movie_id]

        if theater_id:
            shows = [s for s in shows if s.get("theater_id") == theater_id]

        if date and date != "All":
            shows = [s for s in shows if s.get("date", "").lower() == date.lower()]

        if verified_only:
            shows = [s for s in shows if s.get("is_verified") is True]

        # Enrich with theater & movie details for UI display
        enriched = []
        for s in shows:
            item = dict(s)
            th = self.get_theater_by_id(s.get("theater_id", ""))
            mov = self.get_by_id(s.get("movie_id", ""))
            item["theater_name"] = th.get("name") if th else "Unknown Venue"
            item["theater_city"] = th.get("city") if th else "Kolhapur"
            item["theater_verified"] = th.get("is_verified") if th else False
            item["movie_title"] = mov.get("title") if mov else "Unknown Movie"
            enriched.append(item)

        return enriched

    def get_showtime_by_id(self, show_id: str) -> Optional[Dict[str, Any]]:
        show = self._showtimes.get(show_id)
        if not show:
            return None
        item = dict(show)
        th = self.get_theater_by_id(show.get("theater_id", ""))
        mov = self.get_by_id(show.get("movie_id", ""))
        item["theater_name"] = th.get("name") if th else "Unknown Venue"
        item["theater_city"] = th.get("city") if th else "Kolhapur"
        item["theater_verified"] = th.get("is_verified") if th else False
        item["movie_title"] = mov.get("title") if mov else "Unknown Movie"
        return item

    def add_showtime(self, show_data: Dict[str, Any]) -> Dict[str, Any]:
        show_id = show_data.get("id") or f"show-{uuid.uuid4().hex[:8]}"
        new_show = dict(show_data)
        new_show["id"] = show_id
        if "is_verified" not in new_show:
            new_show["is_verified"] = False
        if "status" not in new_show:
            new_show["status"] = "Verified" if new_show["is_verified"] else "Demo / Sample"
        self._showtimes[show_id] = new_show
        return new_show

    def update_showtime(self, show_id: str, show_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if show_id not in self._showtimes:
            return None
        self._showtimes[show_id].update(show_data)
        return self._showtimes[show_id]

    def delete_showtime(self, show_id: str) -> bool:
        if show_id in self._showtimes:
            del self._showtimes[show_id]
            return True
        return False

    # -------------------------------------------------------------------------
    # Metadata Lookups
    # -------------------------------------------------------------------------
    def get_cities(self) -> List[str]:
        return list(self._cities)

    def get_categories(self) -> List[str]:
        return list(self._categories)

    def get_languages(self) -> List[str]:
        return list(self._languages)

    def get_genres(self) -> List[str]:
        return list(self._genres)

    def get_seat_tiers(self) -> Dict[str, Any]:
        return dict(SEAT_TIERS)


# Singleton instance for in-memory session persistence
movie_repository = MovieRepository()

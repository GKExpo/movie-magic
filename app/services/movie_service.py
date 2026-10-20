"""Movie Service.
Coordinates movie browsing, filtering, search, and theater queries.
"""
from typing import List, Dict, Any, Optional
from app.repositories import movie_repository


class MovieService:
    """Business logic for movie catalog and theater schedules."""

    def __init__(self, repo=movie_repository):
        self.repo = repo

    def get_featured_movies(self) -> List[Dict[str, Any]]:
        all_movies = self.repo.get_all()
        featured = [m for m in all_movies if m.get("is_featured")]
        return featured if featured else all_movies[:3]

    def list_movies(
        self,
        city: Optional[str] = None,
        genre: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self.repo.get_all(city=city, genre=genre, search_query=search_query)

    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(movie_id)

    def get_theaters(self, city: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repo.get_theaters(city=city)

    def get_theater_by_id(self, theater_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_theater_by_id(theater_id)

    def get_available_cities(self) -> List[str]:
        return self.repo.get_cities()

    def get_available_genres(self) -> List[str]:
        return self.repo.get_genres()

    def add_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.repo.add_movie(movie_data)

    def delete_movie(self, movie_id: str) -> bool:
        return self.repo.delete_movie(movie_id)


movie_service = MovieService()

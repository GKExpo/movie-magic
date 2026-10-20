from .user_repository import (
    user_repository,
    UserRepository,
    InMemoryUserRepository,
    DynamoDBUserRepository,
    DuplicateEmailError,
    UserPersistenceError,
    normalize_email,
    get_user_repository,
)
from .movie_repository import (
    movie_repository,
    MovieRepository,
    InMemoryMovieRepository,
    DynamoDBMovieRepository,
    CataloguePersistenceError,
    get_movie_repository,
)
from .booking_repository import booking_repository, BookingRepository

__all__ = [
    "user_repository",
    "UserRepository",
    "InMemoryUserRepository",
    "DynamoDBUserRepository",
    "DuplicateEmailError",
    "UserPersistenceError",
    "normalize_email",
    "get_user_repository",
    "movie_repository",
    "MovieRepository",
    "InMemoryMovieRepository",
    "DynamoDBMovieRepository",
    "CataloguePersistenceError",
    "get_movie_repository",
    "booking_repository",
    "BookingRepository",
]

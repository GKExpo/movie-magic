"""Main Blueprint: Home, catalog, movie details, search, and health check."""
from flask import Blueprint, render_template, request, jsonify, current_app
from app.services import movie_service
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/health", methods=["GET"])
def health_check():
    """Application Health Check endpoint.
    Used for local verification, load balancers, and EC2 readiness probes.
    """
    return jsonify({
        "status": "healthy",
        "service": "Movie Magic",
        "version": "1.0.0-phase1",
        "environment": current_app.config.get("ENV", "development"),
        "aws_mode": "mock/demo" if current_app.config.get("USE_AWS_MOCK") else "live",
    }), 200


@main_bp.route("/", methods=["GET"])
def index():
    """Home landing page featuring hero carousel, trending movies, and location filter."""
    selected_city = request.args.get("city", "All")
    selected_genre = request.args.get("genre", "All")
    search_query = request.args.get("q", "").strip()

    featured_movies = movie_service.get_featured_movies()
    all_movies = movie_service.list_movies(city=selected_city, genre=selected_genre, search_query=search_query)
    cities = movie_service.get_available_cities()
    genres = movie_service.get_available_genres()

    return render_template(
        "main/index.html",
        featured_movies=featured_movies,
        movies=all_movies,
        cities=cities,
        genres=genres,
        selected_city=selected_city,
        selected_genre=selected_genre,
        search_query=search_query,
    )


@main_bp.route("/movies", methods=["GET"])
def movies_catalog():
    """Browse movies with search and filters."""
    selected_city = request.args.get("city", "All")
    selected_genre = request.args.get("genre", "All")
    search_query = request.args.get("q", "").strip()

    movies = movie_service.list_movies(city=selected_city, genre=selected_genre, search_query=search_query)
    cities = movie_service.get_available_cities()
    genres = movie_service.get_available_genres()

    return render_template(
        "main/movies.html",
        movies=movies,
        cities=cities,
        genres=genres,
        selected_city=selected_city,
        selected_genre=selected_genre,
        search_query=search_query,
    )


@main_bp.route("/movies/<movie_id>", methods=["GET"])
def movie_detail(movie_id):
    """Movie details page with synopsis, cast, ratings, and theater showtimes."""
    movie = movie_service.get_movie_by_id(movie_id)
    if not movie:
        return render_template("errors/404.html", message="Movie not found"), 404

    selected_city = request.args.get("city", "New York")
    theaters = movie_service.get_theaters(city=selected_city)
    cities = movie_service.get_available_cities()

    return render_template(
        "main/movie_detail.html",
        movie=movie,
        theaters=theaters,
        cities=cities,
        selected_city=selected_city,
    )

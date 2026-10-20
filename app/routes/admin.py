"""Admin Blueprint: Management dashboard, movie inventory, showtimes, bookings."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import AddMovieForm
from app.services import movie_service, booking_service
from app.repositories import user_repository
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/", methods=["GET"])
@admin_required
def dashboard():
    """Admin dashboard layout showing metrics, movies, showtimes, and recent bookings."""
    all_movies = movie_service.list_movies()
    all_bookings = booking_service.get_all_bookings()
    all_users = user_repository.get_all()

    total_revenue = sum(b.get("total_price", 0) for b in all_bookings)
    total_tickets = sum(b.get("ticket_count", 0) for b in all_bookings)

    stats = {
        "movie_count": len(all_movies),
        "booking_count": len(all_bookings),
        "user_count": len(all_users),
        "total_revenue": total_revenue,
        "total_tickets": total_tickets,
    }

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        movies=all_movies,
        recent_bookings=all_bookings[:10],
    )


@admin_bp.route("/movies/new", methods=["GET", "POST"])
@admin_required
def add_movie():
    """Add a new movie to the catalog."""
    form = AddMovieForm()

    if form.validate_on_submit():
        movie_data = {
            "title": form.title.data.strip(),
            "tagline": form.tagline.data.strip(),
            "genre": form.genre.data,
            "duration": form.duration.data.strip(),
            "duration_minutes": 120,
            "rating": form.rating.data,
            "imdb_score": float(form.imdb_score.data),
            "release_year": int(form.release_year.data),
            "director": form.director.data.strip(),
            "cast": ["Cast Members TBD"],
            "synopsis": form.synopsis.data.strip(),
            "format": form.format.data.strip(),
            "badge": form.badge.data.strip() if form.badge.data else "New",
            "is_featured": False,
            "showtimes": [
                {"time": "11:00 AM", "format": form.format.data.strip(), "screen": "Screen 1", "price_tier": "Silver"},
                {"time": "03:30 PM", "format": form.format.data.strip(), "screen": "Screen 1", "price_tier": "Gold"},
                {"time": "07:30 PM", "format": form.format.data.strip(), "screen": "Screen 1", "price_tier": "VIP"},
            ],
        }
        movie_service.add_movie(movie_data)
        flash(f"Movie '{movie_data['title']}' added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_movie.html", form=form)


@admin_bp.route("/movies/<movie_id>/delete", methods=["POST"])
@admin_required
def delete_movie(movie_id):
    """Delete a movie from the catalog."""
    success = movie_service.delete_movie(movie_id)
    if success:
        flash("Movie removed from catalog.", "info")
    else:
        flash("Movie not found.", "warning")
    return redirect(url_for("admin.dashboard"))

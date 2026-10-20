"""Web forms using Flask-WTF and WTForms for validation and CSRF protection."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    FloatField,
    IntegerField,
    SelectField,
    HiddenField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    NumberRange,
    ValidationError,
)
from app.data.sample_movies import SAMPLE_GENRES


class LoginForm(FlaskForm):
    """User Sign In Form."""
    email = StringField(
        "Email Address",
        validators=[DataRequired(message="Please enter your email."), Email(message="Invalid email address.")],
        render_kw={"placeholder": "you@example.com", "autocomplete": "email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Please enter your password.")],
        render_kw={"placeholder": "••••••••", "autocomplete": "current-password"},
    )
    remember_me = BooleanField("Remember me for 30 days")
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    """User Registration Form."""
    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full name is required."),
            Length(min=2, max=80, message="Name must be between 2 and 80 characters."),
        ],
        render_kw={"placeholder": "Alex Morgan", "autocomplete": "name"},
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email address is required."),
            Email(message="Invalid email address."),
        ],
        render_kw={"placeholder": "you@example.com", "autocomplete": "email"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters long."),
        ],
        render_kw={"placeholder": "At least 8 characters, letters & digits", "autocomplete": "new-password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Re-enter your password", "autocomplete": "new-password"},
    )
    submit = SubmitField("Create Account")


class BookingSubmissionForm(FlaskForm):
    """Form for processing seat booking with CSRF protection."""
    movie_id = HiddenField("Movie ID", validators=[DataRequired()])
    theater_id = HiddenField("Theater ID", validators=[DataRequired()])
    showtime = HiddenField("Showtime", validators=[DataRequired()])
    show_date = HiddenField("Show Date", validators=[DataRequired()])
    selected_seats = HiddenField("Selected Seats", validators=[DataRequired(message="Please select at least one seat.")])
    submit = SubmitField("Confirm Booking")


class AddMovieForm(FlaskForm):
    """Admin form to add a new movie."""
    title = StringField("Movie Title", validators=[DataRequired(), Length(max=120)])
    tagline = StringField("Tagline", validators=[DataRequired(), Length(max=200)])
    genre = SelectField("Genre", choices=[(g, g) for g in SAMPLE_GENRES if g != "All"], validators=[DataRequired()])
    duration = StringField("Duration (e.g., 2h 15m)", validators=[DataRequired(), Length(max=20)])
    rating = SelectField("Content Rating", choices=[("G", "G"), ("PG", "PG"), ("PG-13", "PG-13"), ("R", "R"), ("NC-17", "NC-17")])
    imdb_score = FloatField("IMDb Score", validators=[DataRequired(), NumberRange(min=1.0, max=10.0)])
    release_year = IntegerField("Release Year", validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    director = StringField("Director", validators=[DataRequired(), Length(max=100)])
    synopsis = TextAreaField("Synopsis", validators=[DataRequired(), Length(max=1000)])
    format = StringField("Formats (e.g. IMAX 3D, Dolby Atmos)", validators=[DataRequired(), Length(max=80)])
    badge = StringField("Badge Tag (e.g. Trending, Premiere)", validators=[Length(max=40)])
    submit = SubmitField("Save Movie")

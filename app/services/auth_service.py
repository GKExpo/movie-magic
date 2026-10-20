"""Authentication Service.
Handles user registration, login verification, password strength checks, and session data.
"""
from typing import Optional, Dict, Any, Tuple
from app.repositories import user_repository
from app.utils.security import hash_password, verify_password, validate_password_strength


class AuthService:
    """Business logic for authentication and authorization."""

    def __init__(self, repo=user_repository):
        self.repo = repo

    def register(self, email: str, password: str, full_name: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Register a new user account."""
        email = email.strip().lower()
        if not email or "@" not in email:
            return False, "A valid email address is required.", None

        existing_user = self.repo.get_by_email(email)
        if existing_user:
            return False, "An account with this email address already exists.", None

        is_strong, msg = validate_password_strength(password)
        if not is_strong:
            return False, msg, None

        if not full_name or len(full_name.strip()) < 2:
            return False, "Please enter your full name.", None

        hashed = hash_password(password)
        new_user = self.repo.create_user(email=email, password_hash=hashed, full_name=full_name, role="user")
        return True, "Registration successful! You may now sign in.", new_user

    def authenticate(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Authenticate user by email and password."""
        email = email.strip().lower()
        user = self.repo.get_by_email(email)

        if not user:
            return False, "Invalid email or password.", None

        if not verify_password(password, user.get("password_hash", "")):
            return False, "Invalid email or password.", None

        return True, "Sign in successful.", user

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(user_id)


auth_service = AuthService()

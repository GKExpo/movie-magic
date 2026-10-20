"""User Repository (In-Memory Phase 1, DynamoDB ready for Phase 2)."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.utils.security import hash_password
from .base import BaseRepository


class UserRepository(BaseRepository):
    """User data access repository with in-memory store for Phase 1 development."""

    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
        self._email_index: Dict[str, str] = {}
        self._seed_initial_users()

    def _seed_initial_users(self):
        """Seed demo users with securely hashed passwords."""
        demo_users = [
            {
                "id": "usr-admin-1",
                "email": "admin@moviemagic.com",
                "full_name": "Admin Manager",
                "password_hash": hash_password("Admin@123"),
                "role": "admin",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "id": "usr-demo-1",
                "email": "demo@moviemagic.com",
                "full_name": "Demo Moviegoer",
                "password_hash": hash_password("Demo@123"),
                "role": "user",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
        ]
        for user in demo_users:
            self._users[user["id"]] = user
            self._email_index[user["email"].lower()] = user["id"]

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self._users.get(item_id)

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        user_id = self._email_index.get(email.strip().lower())
        if user_id:
            return self._users.get(user_id)
        return None

    def get_all(self) -> List[Dict[str, Any]]:
        return list(self._users.values())

    def create_user(self, email: str, password_hash: str, full_name: str, role: str = "user") -> Dict[str, Any]:
        """Create a new user record."""
        user_id = f"usr-{uuid.uuid4().hex[:12]}"
        user = {
            "id": user_id,
            "email": email.strip().lower(),
            "password_hash": password_hash,
            "full_name": full_name.strip(),
            "role": role,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._users[user_id] = user
        self._email_index[user["email"]] = user_id
        return user


# Singleton instance for in-memory session persistence
user_repository = UserRepository()

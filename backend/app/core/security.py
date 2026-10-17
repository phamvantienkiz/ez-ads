"""Security utilities: Token sanitization and OAuth CSRF state protection."""

import re
import secrets
import time
from typing import Any

# Regex to detect Facebook access tokens (often start with EAAB, EAAG, EAA..., etc.)
TOKEN_PATTERN = re.compile(r"EAA[A-Za-z0-9]+", re.IGNORECASE)
SECRET_PATTERN = re.compile(r"(client_secret|app_secret|secret)=([a-zA-Z0-9_-]+)", re.IGNORECASE)


def sanitize_meta_error(error_content: Any) -> str:
    """Sanitize error messages to ensure zero token/secret exposure in logs or UI."""
    if error_content is None:
        return "Unknown error"

    if isinstance(error_content, dict):
        # Extract message or error_user_msg if available
        msg = (
            error_content.get("error_user_msg")
            or error_content.get("message")
            or str(error_content)
        )
    else:
        msg = str(error_content)

    # Redact tokens
    sanitized = TOKEN_PATTERN.sub("[REDACTED_TOKEN]", msg)
    # Redact secret params
    sanitized = SECRET_PATTERN.sub(r"\1=[REDACTED_SECRET]", sanitized)

    return sanitized


class StateManager:
    """In-memory cryptographic nonce manager for OAuth CSRF protection with TTL."""

    def __init__(self, ttl_seconds: int = 600) -> None:
        self.ttl_seconds = ttl_seconds
        self._states: dict[str, float] = {}

    def generate_state(self) -> str:
        """Generate a cryptographically secure random state nonce and track it."""
        self._clean_expired()
        state = f"baha_{secrets.token_urlsafe(24)}"
        self._states[state] = time.time() + self.ttl_seconds
        return state

    def verify_and_consume(self, state: str) -> bool:
        """Verify the state exists and is not expired, then remove it (single-use)."""
        self._clean_expired()
        if not state:
            return False
        if state in self._states:
            del self._states[state]
            return True
        return False

    def _clean_expired(self) -> None:
        now = time.time()
        expired = [s for s, expiry in self._states.items() if expiry < now]
        for s in expired:
            del self._states[s]


state_manager = StateManager()

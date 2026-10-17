"""Unit tests for currency multiplier invariant and security token redaction."""

from app.core.security import StateManager, sanitize_meta_error
from app.services.ad_service import format_meta_budget


def test_format_meta_budget_invariants() -> None:
    """Verify D-06 Currency Multiplier Invariant."""
    # Zero-decimal currencies: keep exact integer
    assert format_meta_budget(50000, "VND") == "50000"
    assert format_meta_budget(50000.0, "vnd") == "50000"
    assert format_meta_budget(1200, "JPY") == "1200"
    assert format_meta_budget(3000, "KRW") == "3000"

    # Decimal currencies: multiply by 100
    assert format_meta_budget(20, "USD") == "2000"
    assert format_meta_budget(15.5, "USD") == "1550"
    assert format_meta_budget(100, "EUR") == "10000"
    assert format_meta_budget(50.25, "GBP") == "5025"


def test_sanitize_meta_error_redaction() -> None:
    """Verify zero token and secret exposure in error sanitization."""
    raw_error_with_token = "Error calling Meta: token EAAB1234567890abcdef is invalid."
    sanitized = sanitize_meta_error(raw_error_with_token)
    assert "EAAB1234567890abcdef" not in sanitized
    assert "[REDACTED_TOKEN]" in sanitized

    raw_error_with_secret = "Client failed with client_secret=secret12345678"
    sanitized_secret = sanitize_meta_error(raw_error_with_secret)
    assert "secret12345678" not in sanitized_secret
    assert "[REDACTED_SECRET]" in sanitized_secret

    # Dictionary input
    dict_err = {
        "message": "Token EAAG9988776655 expired",
        "error_user_msg": "Phiên làm việc đã hết hạn",
    }
    sanitized_dict = sanitize_meta_error(dict_err)
    assert sanitized_dict == "Phiên làm việc đã hết hạn"


def test_state_manager_csrf_protection() -> None:
    """Verify CSRF state nonce generation and single-use consumption."""
    manager = StateManager(ttl_seconds=60)
    state = manager.generate_state()

    assert state.startswith("baha_")
    # First verification should succeed
    assert manager.verify_and_consume(state) is True
    # Replay attack (second verification) should fail
    assert manager.verify_and_consume(state) is False

    # Invalid state
    assert manager.verify_and_consume("invalid_state_nonce") is False
    assert manager.verify_and_consume("") is False

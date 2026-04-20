import pytest
from jose import jwt

from app.config import settings
from app.services.auth import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        hashed = hash_password("SecurePass1")
        assert isinstance(hashed, str)

    def test_hash_password_not_equal_to_plain(self):
        plain = "SecurePass1"
        hashed = hash_password(plain)
        assert hashed != plain

    def test_hash_starts_with_bcrypt_prefix(self):
        hashed = hash_password("SecurePass1")
        assert hashed.startswith("$2b$")

    def test_same_password_produces_different_hashes(self):
        # bcrypt adds random salt — same password = different hash every time
        hash1 = hash_password("SecurePass1")
        hash2 = hash_password("SecurePass1")
        assert hash1 != hash2

    def test_verify_correct_password_returns_true(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("SecurePass1", hashed) is True

    def test_verify_wrong_password_returns_false(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("WrongPass1", hashed) is False

    def test_verify_empty_password_returns_false(self):
        hashed = hash_password("SecurePass1")
        assert verify_password("", hashed) is False


class TestAccessToken:
    def test_create_access_token_returns_string(self):
        token = create_access_token("some-user-id")
        assert isinstance(token, str)

    def test_access_token_contains_correct_subject(self):
        user_id = "dbcfe9cf-e5c6-4015-be1f-9aa2ad962e62"
        token = create_access_token(user_id)
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        assert payload["sub"] == user_id

    def test_access_token_type_is_access(self):
        token = create_access_token("some-user-id")
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        assert payload["type"] == "access"

    def test_access_token_has_expiry(self):
        token = create_access_token("some-user-id")
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        assert "exp" in payload


class TestRefreshToken:
    def test_refresh_token_type_is_refresh(self):
        token = create_refresh_token("some-user-id")
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        assert payload["type"] == "refresh"

    def test_access_and_refresh_tokens_are_different(self):
        user_id = "some-user-id"
        access = create_access_token(user_id)
        refresh = create_refresh_token(user_id)
        assert access != refresh
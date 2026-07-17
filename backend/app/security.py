from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import get_settings


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()

    now = datetime.now(timezone.utc)

    expires_at = now + (
        expires_delta
        or timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
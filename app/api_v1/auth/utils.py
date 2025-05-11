import jwt
import bcrypt

from app.core.config import AuthJWT

def encode_jwt(
        payload: dict,
        private_key: str = AuthJWT.private_key.read_text(),
        algorithm: str = AuthJWT.ALGORITHM,
):
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded

def decode_jwt(
        token: str | bytes,
        public_key: str = AuthJWT.public_key.read_text(),
        algorithm: str = AuthJWT.ALGORITHM,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithm=[algorithm],
    )
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)
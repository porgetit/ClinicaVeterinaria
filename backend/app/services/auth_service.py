from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

# Configuration (In a real app, use environment variables)
SECRET_KEY = "super-secret-key-for-vet-clinic"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hardcoded Master User for simplicity as requested
MASTER_USER = {
    "username": "admin",
    "password_hash": "$2b$12$e/KcV6UEzbAemiOBmUFOLuKU113TbnJXZ88cqQZ8rcGSzY3W3Hhx."  # bcrypt hash for "admin123"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate_master_user(username, password):
        if username == MASTER_USER["username"] and AuthService.verify_password(password, MASTER_USER["password_hash"]):
            return {"username": username}
        return None

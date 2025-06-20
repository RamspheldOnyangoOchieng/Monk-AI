from datetime import datetime, timedelta
from typing import Optional, Union, Any, Dict

from jose import jwt
import bcrypt
import secrets
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings

# JWT Algorithm
ALGORITHM = "HS256"

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    # Convert strings to bytes if necessary
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
        
    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a password hash."""
    # Convert to bytes if it's a string
    if isinstance(password, str):
        password = password.encode('utf-8')
        
    # Generate a salt and hash the password
    salt = bcrypt.gensalt(rounds=12)  # 12 is a good default for security/performance
    hashed = bcrypt.hashpw(password, salt)
    
    # Return as string for storage
    return hashed.decode('utf-8')

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token for the specified subject.
    
    Args:
        subject: Typically user ID or username
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token as a string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any]) -> str:
    """
    Create a longer-lived refresh token.
    
    Args:
        subject: Typically user ID or username
        
    Returns:
        Encoded refresh token as a string
    """
    # Refresh tokens typically live longer than access tokens
    expire = datetime.utcnow() + timedelta(days=30)
    
    # Add a unique jti (JWT ID) to allow revocation
    jti = secrets.token_urlsafe(32)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "jti": jti,
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, jti

def decode_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token to decode
        token_type: Type of token to expect (access or refresh)
        
    Returns:
        Decoded payload
        
    Raises:
        HTTPException if token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get current user from JWT token with retry logic.
    
    Args:
        token: JWT token from request
        
    Returns:
        User object
        
    Raises:
        HTTPException if token is invalid
    """
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Here you would normally fetch the user from database
    # For example: user = await get_user(user_id)
    # Return the user object
    return {"user_id": user_id}

# Rate limiting implementation
class RateLimiter:
    """
    Simple in-memory rate limiter.
    In production, this should be replaced with a Redis-based implementation.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.request_history = {}  # ip -> [timestamp1, timestamp2, ...]
        
    def is_rate_limited(self, ip: str) -> bool:
        """Check if the IP is currently rate limited."""
        now = datetime.now()
        if ip not in self.request_history:
            self.request_history[ip] = []
            
        # Clean up old entries (older than 1 minute)
        minute_ago = now - timedelta(minutes=1)
        self.request_history[ip] = [
            ts for ts in self.request_history[ip] 
            if ts > minute_ago
        ]
        
        # Check if rate limit is exceeded
        if len(self.request_history[ip]) >= self.requests_per_minute:
            return True
            
        # Record this request
        self.request_history[ip].append(now)
        return False

# Create an instance of the rate limiter
rate_limiter = RateLimiter()

async def verify_rate_limit(request: Request):
    """Middleware function to check rate limiting."""
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
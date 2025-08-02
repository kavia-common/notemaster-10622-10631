from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User

# PUBLIC_INTERFACE
def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password)

# PUBLIC_INTERFACE
def verify_password(password_hash, password):
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)

# PUBLIC_INTERFACE
def authenticate_user(username, password):
    """
    Verify username and password, return user object if successful, else None.
    """
    user = User.query.filter_by(username=username).first()
    if user and verify_password(user.password_hash, password):
        return user
    return None

# PUBLIC_INTERFACE
def create_jwt_for_user(user):
    """
    Create JWT access token for user.
    """
    payload = {"user_id": user.id, "username": user.username}
    return create_access_token(identity=payload)

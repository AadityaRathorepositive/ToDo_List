"""
user.py - User Management Module

Handles all user-related operations including registration, login, 
authentication, and password hashing.

Classes:
    - User: Entity class representing a user
    - Auth: Abstract base class for authentication
    - SimpleAuth: Concrete implementation with custom hash
"""

from abc import ABC, abstractmethod
from typing import Optional


class User:
    """
    Entity class representing a user in the system.
    
    Attributes:
        id: Unique identifier for the user
        username: Unique username for login
        password_hash: Hashed password (never plain text)
    """
    
    def __init__(self, id: int, username: str, password_hash: str):
        """
        Initialize a User instance.
        
        Args:
            id: Unique user ID
            username: Unique username
            password_hash: Hashed password
        """
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    def __repr__(self) -> str:
        """Return string representation of User."""
        return f"User(id={self.id}, username='{self.username}')"
    
    def to_dict(self) -> dict:
        """
        Convert User to dictionary.
        
        Returns:
            Dictionary representation of the user
        """
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Create User instance from dictionary.
        
        Args:
            data: Dictionary with user data
            
        Returns:
            User instance
        """
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            password_hash=data.get('password_hash')
        )


class Auth(ABC):
    """
    Abstract base class for authentication strategies.
    
    Defines the interface that all authentication implementations must follow.
    This allows for easy addition of new authentication methods in the future
    (e.g., OAuth, JWT, LDAP) without modifying existing code.
    
    Design Pattern: Strategy Pattern
    """
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Hash a password for storage.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        pass
    
    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored hash to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        pass


class SimpleAuth(Auth):
    """
    Simple authentication implementation using custom hashing.
    
    Uses a simple hash function for password storage.
    This is suitable for an in-memory application without external dependencies.
    
    Note: This is NOT cryptographically secure for production use.
    For production, use bcrypt, argon2, or similar libraries.
    """
    
    def __init__(self):
        """Initialize SimpleAuth with salt."""
        self._salt = self._generate_salt()
    
    def _generate_salt(self) -> str:
        """
        Generate a simple salt for hashing.
        
        Returns:
            A simple salt string
        """
        # Simple salt generation - not cryptographically secure
        # In production, use secrets or os.urandom
        import time
        return str(int(time.time() * 1000))
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using simple custom algorithm.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string with salt appended
        """
        # Simple hash: reverse + salt + shift
        # This is for demonstration - NOT secure for production!
        reversed_pwd = password[::-1]
        shifted = ''.join(chr(ord(c) + 3) for c in reversed_pwd)
        hashed = f"{self._salt}${shifted}"
        return hashed
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against stored hash.
        
        Args:
            password: Plain text password
            password_hash: Stored hash (salt$hashed)
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            salt, stored_hash = password_hash.split('$')
            # Reverse the hashing process
            unshifted = ''.join(chr(ord(c) - 3) for c in stored_hash)
            original = unshifted[::-1]
            # Hash the provided password and compare
            test_hash = self.hash_password(password)
            _, test_final = test_hash.split('$')
            return stored_hash == test_final
        except (ValueError, IndexError):
            return False


class UserManager:
    """
    Manages user operations including registration and authentication.
    
    This class coordinates between User entity, authentication, and database.
    """
    
    def __init__(self, user_table, auth: Auth|None = None):
        """
        Initialize UserManager.
        
        Args:
            user_table: Database table for users (UserTable instance)
            auth: Authentication strategy (defaults to SimpleAuth)
        """
        self._user_table = user_table
        self._auth = auth or SimpleAuth()
        self._current_user: Optional[User] = None
    
    def register(self, username: str, password: str) -> User:
        """
        Register a new user.
        
        Args:
            username: Desired username (must be unique)
            password: Plain text password
            
        Returns:
            Created User instance
            
        Raises:
            ValueError: If username already exists
        """
        # Validate inputs
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not password or len(password) < 1:
            raise ValueError("Password cannot be empty")
        
        # Hash password
        password_hash = self._auth.hash_password(password)
        
        # Create user record
        user_data = {
            'username': username.strip(),
            'password_hash': password_hash
        }
        
        # Add to database (will raise ValueError if username exists)
        created = self._user_table.add(user_data)
        
        return User.from_dict(created)
    
    def login(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        # Find user by username
        user_data = self._user_table.find_by_username(username)
        
        if user_data is None:
            return None
        
        # Verify password
        if not self._auth.verify_password(password, user_data.get('password_hash')):
            return None
        
        # Create user object and set as current user
        user = User.from_dict(user_data)
        self._current_user = user
        return user
    
    def logout(self):
        """Log out the current user."""
        self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """
        Get the currently logged in user.
        
        Returns:
            Current User or None if not logged in
        """
        return self._current_user
    
    def is_logged_in(self) -> bool:
        """
        Check if a user is currently logged in.
        
        Returns:
            True if logged in, False otherwise
        """
        return self._current_user is not None
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user account.
        
        Args:
            user_id: ID of user to delete
            
        Returns:
            True if successful, False if user not found
        """
        return self._user_table.delete(user_id)
    
    def get_all_users(self) -> list[User]:
        """
        Get all registered users.
        
        Returns:
            List of all User instances
        """
        users_data = self._user_table.find_all()
        return [User.from_dict(u) for u in users_data]


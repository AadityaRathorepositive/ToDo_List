"""
database.py - Data Storage Module

Provides CRUD (Create, Read, Update, Delete) operations using in-memory data structures.
Implements the repository pattern with abstract base class for consistent interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class DBTable(ABC):
    """
    Abstract base class for all database tables.
    
    Defines the interface that all table implementations must follow.
    This ensures consistent behavior across all data access layers
    and allows for easy substitution of storage backends in the future.
    """
    
    def __init__(self):
        """Initialize the table with empty storage."""
        self._data: list[dict] = []
    
    @abstractmethod
    def add(self, record: dict) -> dict:
        """
        Add a new record to the table.
        
        Args:
            record: Dictionary containing the record data
            
        Returns:
            The added record with generated ID
        """
        pass
    
    @abstractmethod
    def update(self, record_id: Any, data: dict) -> bool:
        """
        Update an existing record.
        
        Args:
            record_id: Unique identifier of the record
            data: Dictionary containing fields to update
            
        Returns:
            True if update was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete(self, record_id: Any) -> bool:
        """
        Delete a record by ID.
        
        Args:
            record_id: Unique identifier of the record
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def find_by_id(self, record_id: Any) -> Optional[dict]:
        """
        Find a record by its ID.
        
        Args:
            record_id: Unique identifier of the record
            
        Returns:
            The record if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> list[dict]:
        """
        Retrieve all records from the table.
        
        Returns:
            List of all records
        """
        pass
    
    def _generate_id(self) -> int:
        """
        Generate a unique ID for new records.
        
        Returns:
            A unique integer ID
        """
        if not self._data:
            return 1
        return max(record.get('id', 0) for record in self._data) + 1
    
    def _find_index_by_id(self, record_id: Any) -> int:
        """
        Find the index of a record by ID.
        
        Args:
            record_id: Unique identifier of the record
            
        Returns:
            Index of the record, -1 if not found
        """
        for i, record in enumerate(self._data):
            if record.get('id') == record_id:
                return i
        return -1


class UserTable(DBTable):
    """
    Table for storing user records.
    
    Manages user data including username and password hash.
    Each user has a unique ID and username.
    """
    
    def __init__(self):
        super().__init__()
    
    def add(self, record: dict) -> dict:
        """
        Add a new user to the table.
        
        Args:
            record: Dictionary with 'username' and 'password_hash'
            
        Returns:
            The added user record with generated ID
            
        Raises:
            ValueError: If username already exists
        """
        # Check for duplicate username
        for user in self._data:
            if user.get('username') == record.get('username'):
                raise ValueError(f"Username '{record.get('username')}' already exists")
        
        new_user = {
            'id': self._generate_id(),
            'username': record.get('username'),
            'password_hash': record.get('password_hash')
        }
        self._data.append(new_user)
        return new_user
    
    def update(self, record_id: Any, data: dict) -> bool:
        """
        Update user information.
        
        Args:
            record_id: User ID
            data: Dictionary with fields to update
            
        Returns:
            True if successful, False if user not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        
        # Update only provided fields
        for key, value in data.items():
            if key != 'id':  # Don't allow changing ID
                self._data[index][key] = value
        return True
    
    def delete(self, record_id: Any) -> bool:
        """
        Delete a user by ID.
        
        Args:
            record_id: User ID
            
        Returns:
            True if successful, False if user not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        self._data.pop(index)
        return True
    
    def find_by_id(self, record_id: Any) -> Optional[dict]:
        """
        Find a user by ID.
        
        Args:
            record_id: User ID
            
        Returns:
            User record or None
        """
        index = self._find_index_by_id(record_id)
        return self._data[index] if index != -1 else None
    
    def find_all(self) -> list[dict]:
        """Get all users."""
        return self._data.copy()
    
    def find_by_username(self, username: str) -> Optional[dict]:
        """
        Find a user by username.
        
        Args:
            username: Username to search for
            
        Returns:
            User record or None
        """
        for user in self._data:
            if user.get('username') == username:
                return user
        return None


class ItemTable(DBTable):
    """
    Table for storing task/item records.
    
    Manages task data including name, description, priority, deadline, and status.
    Each item has a unique ID.
    """
    
    def __init__(self):
        super().__init__()
    
    def add(self, record: dict) -> dict:
        """
        Add a new item to the table.
        
        Args:
            record: Dictionary with item data
            
        Returns:
            The added item with generated ID
        """
        new_item = {
            'id': self._generate_id(),
            'name': record.get('name'),
            'description': record.get('description'),
            'priority': record.get('priority', 'LOW'),
            'deadline': record.get('deadline'),
            'status': record.get('status', 'TODO')
        }
        self._data.append(new_item)
        return new_item
    
    def update(self, record_id: Any, data: dict) -> bool:
        """
        Update an item.
        
        Args:
            record_id: Item ID
            data: Dictionary with fields to update
            
        Returns:
            True if successful, False if item not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        
        for key, value in data.items():
            if key != 'id':  # Don't allow changing ID
                self._data[index][key] = value
        return True
    
    def delete(self, record_id: Any) -> bool:
        """
        Delete an item by ID.
        
        Args:
            record_id: Item ID
            
        Returns:
            True if successful, False if item not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        self._data.pop(index)
        return True
    
    def find_by_id(self, record_id: Any) -> Optional[dict]:
        """
        Find an item by ID.
        
        Args:
            record_id: Item ID
            
        Returns:
            Item record or None
        """
        index = self._find_index_by_id(record_id)
        return self._data[index] if index != -1 else None
    
    def find_all(self) -> list[dict]:
        """Get all items."""
        return self._data.copy()


class UserItemsTable(DBTable):
    """
    Table for managing the relationship between users and their items.
    
    Acts as a join table to associate users with their tasks.
    Each record links a user_id to an item_id.
    """
    
    def __init__(self):
        super().__init__()
    
    def add(self, record: dict) -> dict:
        """
        Create a user-item association.
        
        Args:
            record: Dictionary with 'user_id' and 'item_id'
            
        Returns:
            The created association record
        """
        new_association = {
            'id': self._generate_id(),
            'user_id': record.get('user_id'),
            'item_id': record.get('item_id')
        }
        self._data.append(new_association)
        return new_association
    
    def update(self, record_id: Any, data: dict) -> bool:
        """
        Update an association (rarely used).
        
        Args:
            record_id: Association ID
            data: Dictionary with fields to update
            
        Returns:
            True if successful, False if not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        
        for key, value in data.items():
            if key != 'id':
                self._data[index][key] = value
        return True
    
    def delete(self, record_id: Any) -> bool:
        """
        Delete an association.
        
        Args:
            record_id: Association ID
            
        Returns:
            True if successful, False if not found
        """
        index = self._find_index_by_id(record_id)
        if index == -1:
            return False
        self._data.pop(index)
        return True
    
    def find_by_id(self, record_id: Any) -> Optional[dict]:
        """
        Find an association by ID.
        
        Args:
            record_id: Association ID
            
        Returns:
            Association record or None
        """
        index = self._find_index_by_id(record_id)
        return self._data[index] if index != -1 else None
    
    def find_all(self) -> list[dict]:
        """Get all associations."""
        return self._data.copy()
    
    def find_by_user_id(self, user_id: Any) -> list[dict]:
        """
        Find all item IDs associated with a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of association records for the user
        """
        return [assoc for assoc in self._data if assoc.get('user_id') == user_id]
    
    def find_by_item_id(self, item_id: Any) -> list[dict]:
        """
        Find all user IDs associated with an item.
        
        Args:
            item_id: Item ID
            
        Returns:
            List of association records for the item
        """
        return [assoc for assoc in self._data if assoc.get('item_id') == item_id]
    
    def delete_by_user_id(self, user_id: Any) -> int:
        """
        Delete all associations for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of associations deleted
        """
        original_count = len(self._data)
        self._data = [assoc for assoc in self._data if assoc.get('user_id') != user_id]
        return original_count - len(self._data)
    
    def delete_by_item_id(self, item_id: Any) -> int:
        """
        Delete all associations for an item.
        
        Args:
            item_id: Item ID
            
        Returns:
            Number of associations deleted
        """
        original_count = len(self._data)
        self._data = [assoc for assoc in self._data if assoc.get('item_id') != item_id]
        return original_count - len(self._data)


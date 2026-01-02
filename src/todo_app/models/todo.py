"""
Todo model representing a single todo item.

This module defines the Todo class which represents a single todo item
with attributes like id, title, completion status, and creation timestamp.
"""

from datetime import datetime
from typing import Dict, Any


class Todo:
    """
    Represents a single todo item.

    Attributes:
        id (int): Unique identifier for the todo
        title (str): Description of the task
        completed (bool): Completion status (default: False)
        created_at (datetime): Timestamp when the todo was created
    """

    def __init__(self, id: int, title: str, completed: bool = False):
        """
        Initialize a Todo instance.

        Args:
            id (int): Unique identifier for the todo
            title (str): Description of the task
            completed (bool): Completion status (default: False)
        """
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty")

        self.id = id
        self.title = title.strip()
        self.completed = completed
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Todo instance to a dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the todo
        """
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self) -> str:
        """
        String representation of the Todo instance.

        Returns:
            str: String representation
        """
        status = "Complete" if self.completed else "Incomplete"
        return f"Todo(id={self.id}, title='{self.title}', status={status})"

    def __eq__(self, other) -> bool:
        """
        Check equality with another Todo instance.

        Args:
            other: Another Todo instance to compare with

        Returns:
            bool: True if both instances have the same attributes
        """
        if not isinstance(other, Todo):
            return False
        return (self.id == other.id and
                self.title == other.title and
                self.completed == other.completed)
"""
Todo service layer for business logic.

This module defines the TodoService class which handles all business logic
for managing todo items, including adding, updating, deleting, and marking
todos as complete.
"""

from typing import List, Optional, Dict, Any
from ..models.todo import Todo


class TodoService:
    """
    Service class for managing todo items.

    This class provides methods for all CRUD operations on todo items
    and maintains the in-memory storage of todos.
    """

    def __init__(self):
        """Initialize the TodoService with an empty todo list."""
        self._todos: Dict[int, Todo] = {}
        self._next_id = 1

    def add_todo(self, title: str) -> Optional[Todo]:
        """
        Add a new todo item to the collection.

        Args:
            title (str): The description of the task

        Returns:
            Todo: The created todo object if successful, None if validation fails
        """
        if not title or not title.strip():
            return None

        todo = Todo(id=self._next_id, title=title.strip())
        self._todos[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all todo items in the system.

        Returns:
            List[Todo]: List of all todo objects
        """
        return list(self._todos.values())

    def update_todo(self, id: int, new_title: str) -> Optional[Todo]:
        """
        Update the title of an existing todo item.

        Args:
            id (int): The ID of the todo to update
            new_title (str): The new description

        Returns:
            Todo: Updated todo object if successful, None if not found or validation fails
        """
        if id not in self._todos:
            return None

        if not new_title or not new_title.strip():
            return None

        self._todos[id].title = new_title.strip()
        return self._todos[id]

    def delete_todo(self, id: int) -> bool:
        """
        Remove a todo item from the collection.

        Args:
            id (int): The ID of the todo to delete

        Returns:
            bool: True if deletion was successful, False if todo was not found
        """
        if id not in self._todos:
            return False

        del self._todos[id]
        return True

    def mark_todo_complete(self, id: int) -> bool:
        """
        Mark a todo item as complete.

        Args:
            id (int): The ID of the todo to mark complete

        Returns:
            bool: True if marking was successful, False if todo was not found
        """
        if id not in self._todos:
            return False

        self._todos[id].completed = True
        return True

    def get_todo_by_id(self, id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo item by its ID.

        Args:
            id (int): The ID of the todo to retrieve

        Returns:
            Todo: Todo object if found, None if not found
        """
        return self._todos.get(id)
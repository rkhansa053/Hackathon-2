"""
CLI interface for the Todo application.

This module defines the TodoCLI class which provides the console-based
user interface for interacting with todo items.
"""

from typing import Optional
from ..services.todo_service import TodoService


class TodoCLI:
    """
    Command-line interface for the Todo application.

    This class provides methods for all user interactions with the todo list
    through a console-based menu system.
    """

    def __init__(self):
        """Initialize the CLI with a TodoService instance."""
        self.service = TodoService()

    def run(self):
        """Main application loop with menu system."""
        while True:
            self._display_menu()
            choice = input("Enter your choice: ").strip().lower()

            if choice in ['q', 'quit', 'exit']:
                print("Goodbye!")
                break
            elif choice in ['a', 'add']:
                self._add_todo()
            elif choice in ['v', 'view']:
                self._view_todos()
            elif choice in ['u', 'update']:
                self._update_todo()
            elif choice in ['d', 'delete']:
                self._delete_todo()
            elif choice in ['m', 'mark', 'complete']:
                self._mark_todo_complete()
            elif choice in ['h', 'help']:
                self._display_help()
            else:
                print("Invalid choice. Please try again.")
            print()  # Empty line for readability

    def _display_menu(self):
        """Display the main menu options."""
        print("Options: (A)dd, (V)iew, (U)pdate, (D)elete, (M)ark complete, (H)elp, (Q)uit")

    def _display_help(self):
        """Display help information."""
        print("\nHelp:")
        print("  A/a - Add a new todo item")
        print("  V/v - View all todo items")
        print("  U/u - Update a todo item")
        print("  D/d - Delete a todo item")
        print("  M/m - Mark a todo as complete")
        print("  H/h - Show this help message")
        print("  Q/q - Quit the application")
        print()

    def _add_todo(self):
        """Add a new todo item."""
        title = input("Enter todo description: ").strip()
        if not title:
            print("Error: Todo description cannot be empty.")
            return

        todo = self.service.add_todo(title)
        if todo:
            print(f"Todo added with ID {todo.id}")
        else:
            print("Error: Failed to add todo.")

    def _view_todos(self):
        """View all todo items."""
        todos = self.service.get_all_todos()
        if not todos:
            print("No todos in the list.")
            return

        print("Todos:")
        for todo in todos:
            status = "Complete" if todo.completed else "Incomplete"
            print(f"{todo.id}: {todo.title} [{status}]")

    def _update_todo(self):
        """Update a todo item."""
        try:
            id = int(input("Enter todo ID to update: "))
        except ValueError:
            print("Error: Please enter a valid ID number.")
            return

        # Check if the todo exists before asking for new title
        existing_todo = self.service.get_todo_by_id(id)
        if not existing_todo:
            print(f"Error: Todo with ID {id} not found.")
            return

        new_title = input(f"Enter new title for todo {id} (current: '{existing_todo.title}'): ").strip()
        if not new_title:
            print("Error: Todo title cannot be empty.")
            return

        updated_todo = self.service.update_todo(id, new_title)
        if updated_todo:
            print(f"Todo {id} updated successfully.")
        else:
            print("Error: Failed to update todo.")

    def _delete_todo(self):
        """Delete a todo item."""
        try:
            id = int(input("Enter todo ID to delete: "))
        except ValueError:
            print("Error: Please enter a valid ID number.")
            return

        if self.service.delete_todo(id):
            print(f"Todo {id} deleted successfully.")
        else:
            print(f"Error: Todo with ID {id} not found.")

    def _mark_todo_complete(self):
        """Mark a todo item as complete."""
        try:
            id = int(input("Enter todo ID to mark complete: "))
        except ValueError:
            print("Error: Please enter a valid ID number.")
            return

        if self.service.mark_todo_complete(id):
            print(f"Todo {id} marked as complete.")
        else:
            print(f"Error: Todo with ID {id} not found.")
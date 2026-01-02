#!/usr/bin/env python3
"""
Main entry point for the Todo Application.

This console-based application allows users to manage their todo list with
add, view, update, delete, and mark complete functionality.
"""

from todo_app.cli.todo_cli import TodoCLI


def main():
    """Main application entry point."""
    print("Welcome to the Todo App!")
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()
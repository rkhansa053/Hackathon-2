# Console Todo App

A simple console-based todo application with in-memory storage, built as part of a multi-phase evolution project.

## Overview

This is Phase I of a multi-phase Todo application project. It provides a console-based interface for managing todo items with in-memory storage.

## Features

- Add new todo items
- View all todo items
- Update todo item descriptions
- Delete todo items
- Mark todo items as complete/incomplete
- Interactive menu system
- Input validation and error handling

## Requirements

- Python 3.13 or higher

## Installation

This project uses `uv` for fast Python package management. To set up the project:

1. Install `uv` if you haven't already:
   ```bash
   pip install uv
   ```

2. Create a virtual environment:
   ```bash
   uv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

4. Install the project in development mode:
   ```bash
   uv pip install -e .
   ```

## Usage

To run the application:

```bash
python src/main.py
```

Or if installed in development mode:
```bash
todo-app
```

## Project Structure

```
src/
├── main.py                 # Application entry point
└── todo_app/               # Main package
    ├── __init__.py
    ├── models/             # Data models
    │   ├── __init__.py
    │   └── todo.py
    ├── services/           # Business logic
    │   ├── __init__.py
    │   └── todo_service.py
    └── cli/                # Command-line interface
        ├── __init__.py
        └── todo_cli.py
```

## Development

To run tests:
```bash
python test_todo_app.py
```

## Phase I Constraints

- In-memory only (no persistence)
- Console-based interaction
- Python standard library only (no external dependencies for Phase I)
- Data resets on program restart

## License

MIT"# Hackathon-2" 

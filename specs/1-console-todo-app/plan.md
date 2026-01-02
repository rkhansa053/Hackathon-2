# Implementation Plan: In-Memory Python Console Todo App

**Feature**: 1-console-todo-app
**Author**: Claude Code
**Date**: 2026-01-02
**Status**: Draft

## Technical Context

### Architecture Overview
- Single-process CLI application
- In-memory task store using Python data structures
- Layered structure: CLI → Service → Model

### Technology Stack
- Python 3.13+ (as specified in requirements)
- Standard library only (no external dependencies for Phase I)
- Console-based user interface

### Current State
- Feature specification: `specs/1-console-todo-app/spec.md`
- Project constitution: `.specify/memory/constitution.md`

### Unknowns
- Specific Python modules to use for CLI interface (RESOLVED in research.md)
- Data structure choice for in-memory storage (RESOLVED in research.md)

## Constitution Check

Based on `.specify/memory/constitution.md`, this implementation must:

✅ **Simplicity First**: Implementation will use clean, readable Python code with minimal complexity
✅ **In-Memory Data Handling**: Data will be stored in memory using Python data structures, with no persistence
✅ **Clean Separation of Concerns**: Clear layers for CLI interface, business logic (services), and data models
✅ **Production-Readiness at Each Phase**: Proper error handling and input validation will be implemented
✅ **Phase-Based Development**: Code structure will allow for future phase extensions

## Phase 0: Outline & Research

### Research Tasks

1. **CLI Interface Decision**
   - Decision: Use Python's built-in `input()` and `print()` functions for console interaction
   - Rationale: Simplest approach using standard library, matches requirement for Python standard library preferred
   - Alternatives considered: argparse for command-line arguments vs interactive menu system; chose interactive menu for better user experience

2. **Data Structure Decision**
   - Decision: Use Python list of dictionaries for in-memory storage
   - Rationale: Simple, efficient, and allows for easy manipulation of todo items
   - Alternatives considered: list of objects vs dictionaries vs other structures; dictionaries provide good balance of simplicity and functionality

3. **Project Structure Decision**
   - Decision: Organize code in modules - models, services, cli
   - Rationale: Follows the required layered architecture (CLI → Service → Model)
   - Alternatives considered: Single file vs modular approach; modular approach better for maintainability

## Phase 1: Design & Contracts

### Data Model

#### Todo Entity
- **id**: Unique identifier (integer, auto-incremented)
- **title**: Task description (string, required)
- **completed**: Status flag (boolean, default: False)
- **created_at**: Creation timestamp (datetime, auto-generated)

#### Todo List
- **todos**: Collection of Todo entities (list/dictionary)
- **next_id**: Counter for next available ID (integer, auto-incremented)

### API Contracts

Based on functional requirements from spec, the service layer will expose:

1. **add_todo(title: str) -> Todo**
   - Validates non-empty title
   - Creates new Todo with unique ID
   - Returns created Todo

2. **get_all_todos() -> List[Todo]**
   - Returns all todos in the system
   - Returns empty list if no todos exist

3. **update_todo(id: int, new_title: str) -> Todo | None**
   - Updates title of existing todo
   - Returns updated todo or None if not found
   - Validates non-empty new_title

4. **delete_todo(id: int) -> bool**
   - Deletes todo by ID
   - Returns True if successful, False if not found

5. **mark_todo_complete(id: int) -> bool**
   - Marks todo as complete by ID
   - Returns True if successful, False if not found

### Quickstart Guide

1. Run `python todo_app.py` to start the application
2. Use the menu options to interact with your todo list:
   - 'A' or 'a' to add a new todo
   - 'V' or 'v' to view all todos
   - 'U' or 'u' to update a todo
   - 'D' or 'd' to delete a todo
   - 'M' or 'm' to mark a todo as complete
   - 'Q' or 'q' to quit the application

## Phase 2: Implementation Strategy

### File Structure
```
specs/1-console-todo-app/
├── plan.md (this file)
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── todo-api.md
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── todo.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py
│   └── cli/
│       ├── __init__.py
│       └── todo_cli.py
└── main.py
```

### Implementation Tasks
1. Create data models for Todo entity
2. Implement in-memory repository and service layer
3. Build CLI interface with menu system
4. Integrate all components
5. Add input validation and error handling
6. Test functionality

## Gate Analysis

✅ **Constitution Compliance**: All implementation decisions align with project constitution
✅ **Scope Adherence**: Stays within Phase I requirements (console, in-memory, no persistence)
✅ **Technology Alignment**: Uses Python standard library as required
✅ **Architecture Consistency**: Follows layered architecture pattern
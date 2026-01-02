# Data Model: In-Memory Python Console Todo App

## Todo Entity

### Attributes
- **id**: Unique identifier (integer, auto-incremented)
- **title**: Task description (string, required)
- **completed**: Status flag (boolean, default: False)
- **created_at**: Creation timestamp (datetime, auto-generated)

### Validation Rules
- `id` must be unique within the system
- `title` must not be empty or only whitespace
- `completed` must be a boolean value
- `created_at` is set automatically when todo is created

### State Transitions
- New todo: `completed` = False (default)
- Updated todo: `completed` can transition from False to True or vice versa
- Deleted todo: removed from the system entirely

## Todo List Collection

### Attributes
- **todos**: Collection of Todo entities (list/dictionary)
- **next_id**: Counter for next available ID (integer, auto-incremented, starts at 1)

### Operations
- Add new todo: increases `next_id` counter
- Update existing todo: preserves ID
- Delete todo: ID becomes available for future use (implementation detail)
- Mark complete: updates only the completion status

## In-Memory Storage Structure

The application will use a Python dictionary to store todos:
```python
{
    "todos": {
        1: {"id": 1, "title": "Sample task", "completed": False, "created_at": "timestamp"},
        2: {"id": 2, "title": "Another task", "completed": True, "created_at": "timestamp"}
    },
    "next_id": 3
}
```

This structure allows for O(1) access to any todo by its ID and maintains uniqueness of IDs.
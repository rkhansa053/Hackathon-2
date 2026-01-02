# Todo API Contracts

## Service Layer Interface

### TodoService Class

#### Methods

**add_todo(title: str) -> dict | None**
- **Purpose**: Add a new todo item to the collection
- **Input**: title (string) - the description of the task
- **Output**: Todo object (dict) with all attributes if successful, None if validation fails
- **Preconditions**: title must not be empty
- **Postconditions**: New todo is added to the collection with unique ID
- **Side effects**: Increments next_id counter

**get_all_todos() -> list**
- **Purpose**: Retrieve all todo items in the system
- **Input**: None
- **Output**: List of all todo objects (list of dicts)
- **Preconditions**: None
- **Postconditions**: None
- **Side effects**: None

**update_todo(id: int, new_title: str) -> dict | None**
- **Purpose**: Update the title of an existing todo item
- **Input**: id (integer) - the ID of the todo to update, new_title (string) - the new description
- **Output**: Updated todo object (dict) if successful, None if not found or validation fails
- **Preconditions**: Todo with given ID must exist, new_title must not be empty
- **Postconditions**: Todo with given ID has updated title
- **Side effects**: None

**delete_todo(id: int) -> bool**
- **Purpose**: Remove a todo item from the collection
- **Input**: id (integer) - the ID of the todo to delete
- **Output**: True if deletion was successful, False if todo was not found
- **Preconditions**: Todo with given ID must exist
- **Postconditions**: Todo with given ID is removed from the collection
- **Side effects**: None

**mark_todo_complete(id: int) -> bool**
- **Purpose**: Mark a todo item as complete
- **Input**: id (integer) - the ID of the todo to mark complete
- **Output**: True if marking was successful, False if todo was not found
- **Preconditions**: Todo with given ID must exist
- **Postconditions**: Todo with given ID has completed status set to True
- **Side effects**: None

**get_todo_by_id(id: int) -> dict | None**
- **Purpose**: Retrieve a specific todo item by its ID
- **Input**: id (integer) - the ID of the todo to retrieve
- **Output**: Todo object (dict) if found, None if not found
- **Preconditions**: None
- **Postconditions**: None
- **Side effects**: None

## Data Contracts

### Todo Object Structure
```json
{
  "id": 1,
  "title": "Sample task",
  "completed": false,
  "created_at": "2026-01-02T19:18:00Z"
}
```

### Error Response Structure
```json
{
  "error": "Error message describing the issue"
}
```

## Validation Rules

1. **Title Validation**: All titles must be non-empty strings with at least one non-whitespace character
2. **ID Validation**: All IDs must be positive integers
3. **Status Validation**: Completed status must be a boolean value
4. **Existence Validation**: Operations requiring an ID will fail if no todo exists with that ID
"""
Simple test to verify the todo application components work correctly.
"""
from todo_app.models.todo import Todo
from todo_app.services.todo_service import TodoService

def test_todo_creation():
    """Test creating a todo item."""
    todo = Todo(id=1, title="Test task")
    assert todo.id == 1
    assert todo.title == "Test task"
    assert todo.completed == False
    print("PASS: Todo creation test passed")

def test_todo_service():
    """Test the todo service functionality."""
    service = TodoService()

    # Test adding a todo
    todo = service.add_todo("Test task")
    assert todo is not None
    assert todo.id == 1
    assert todo.title == "Test task"

    # Test getting all todos
    todos = service.get_all_todos()
    assert len(todos) == 1
    assert todos[0].id == 1

    # Test updating a todo
    updated_todo = service.update_todo(1, "Updated task")
    assert updated_todo is not None
    assert updated_todo.title == "Updated task"

    # Test marking complete
    result = service.mark_todo_complete(1)
    assert result == True
    assert service.get_todo_by_id(1).completed == True

    # Test deleting a todo
    result = service.delete_todo(1)
    assert result == True
    assert service.get_todo_by_id(1) is None

    print("PASS: Todo service test passed")

if __name__ == "__main__":
    test_todo_creation()
    test_todo_service()
    print("SUCCESS: All tests passed! The application components are working correctly.")
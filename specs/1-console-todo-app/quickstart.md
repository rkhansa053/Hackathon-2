# Quickstart Guide: In-Memory Python Console Todo App

## Prerequisites
- Python 3.13 or higher
- Basic command line familiarity

## Setup
1. Ensure Python 3.13+ is installed on your system
2. Clone or access the project directory
3. No additional dependencies required (using Python standard library only)

## Running the Application
1. Navigate to the project root directory
2. Run the application: `python main.py`
3. The application will start with an interactive menu

## Using the Todo App
Once the application starts, you'll see a menu with the following options:

- **A/a**: Add a new todo item
  - Enter a description when prompted
  - The app will create a new todo with an auto-generated ID

- **V/v**: View all todo items
  - Displays all todos with their ID, title, and completion status
  - Shows a message if the list is empty

- **U/u**: Update a todo item
  - Enter the ID of the todo you want to update
  - Enter the new title for the todo
  - The app will update the title if the ID exists

- **D/d**: Delete a todo item
  - Enter the ID of the todo you want to delete
  - The app will remove the todo if the ID exists

- **M/m**: Mark a todo as complete
  - Enter the ID of the todo you want to mark complete
  - The app will update the status if the ID exists

- **Q/q**: Quit the application
  - Exits the application
  - All data will be lost when the application closes (in-memory storage)

## Example Usage Session
```
Welcome to the Todo App!
Options: (A)dd, (V)iew, (U)pdate, (D)elete, (M)ark complete, (Q)uit
> a
Enter todo description: Buy groceries
Todo added with ID 1

> a
Enter todo description: Walk the dog
Todo added with ID 2

> v
Todos:
1: Buy groceries [Incomplete]
2: Walk the dog [Incomplete]

> m
Enter todo ID to mark complete: 2
Todo 2 marked as complete

> v
Todos:
1: Buy groceries [Incomplete]
2: Walk the dog [Complete]

> q
Goodbye!
```

## Error Handling
- Invalid menu selections will show an error message and return to the menu
- Non-existent todo IDs will show an appropriate error message
- Empty todo descriptions will be rejected

## Development
The application follows a layered architecture:
- CLI layer: Handles user input and displays output
- Service layer: Contains business logic and data operations
- Model layer: Defines data structures and validation rules
# Todo Application

A simple command-line todo list application built with Python. Manage your tasks with priorities, deadlines, and status tracking.

## Features

- **User Authentication**: Register and login to manage your personal task list
- **Task Management**: Create, read, update, and delete tasks
- **Priority Levels**: Assign priorities (LOW, MEDIUM, HIGH, CRITICAL)
- **Deadlines**: Set due dates for tasks
- **Status Tracking**: Track task progress (TODO, INPROGRESS, DONE, CANCELLED)
- **Smart Ordering**: Tasks are automatically sorted by priority (CRITICAL first) then by deadline

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the `ToDo_List/python/ToDoList` directory
3. No additional installation steps required!

## Usage

### Running the Application

```bash
python main.py
```

### Getting Started

1. **Launch the application**: Run `python main.py`
2. **Register**: Choose option 2 to create a new account
3. **Login**: Use your credentials to access your task list
4. **Create Tasks**: Press N to create a new task

### Main Menu Options

| Option | Action |
|--------|--------|
| `N` | Create a new task |
| `[number]` | View/edit an existing task |
| `Q` | Logout and exit |

### Task Actions

When viewing a task, you can:
1. **Update Task** - Modify task details
2. **Change Status** - Update task progress
3. **Delete Task** - Remove the task
4. **Back** - Return to main menu

## Task Properties

| Property | Description | Required |
|----------|-------------|----------|
| Name | Task summary/title | Yes |
| Description | Detailed description | No |
| Priority | LOW, MEDIUM, HIGH, CRITICAL | No (default: LOW) |
| Deadline | Due date (YYYY-MM-DD format) | No |
| Status | TODO, INPROGRESS, DONE, CANCELLED | No (default: TODO) |

## Project Structure

```
ToDoList/
├── main.py         # CLI interface and application entry point
├── user.py         # User management and authentication
├── task.py         # Task definitions and management
├── database.py     # In-memory data storage
├── Architecture.md # Technical architecture documentation
├── DesignDecisions.md # Design decisions and rationale
└── Scope.md       # Project scope and requirements
```

## Architecture

The application follows a modular architecture with clear separation of concerns:

- **user.py**: User entity, authentication (Auth abstract class), and UserManager
- **task.py**: Task entity, Priority/Status enums, and TaskManager
- **database.py**: In-memory storage with DBTable abstract base class
- **main.py**: CLI interface and application orchestration

See `Architecture.md` for detailed technical documentation.

## Data Storage

- All data is stored in-memory (no database setup required)
- Data is lost when the application exits
- Passwords are hashed using a simple custom algorithm (not cryptographically secure - for demonstration only)

## License

This project is for educational purposes.


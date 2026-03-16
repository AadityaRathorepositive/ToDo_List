# Architecture Document

## 1. Overview

This document outlines the technical architecture of the Todo application. The system is designed as a modular, in-memory application using Python's built-in data structures without external dependencies.

## 2. Module Structure

The application is organized into four main modules:

```
ToDoList/
├── user.py      # User management and authentication
├── task.py      # Task definitions and enums
├── database.py  # Data storage and CRUD operations
└── main.py      # CLI interface and orchestration
```

## 3. Module Details

### 3.1 user.py - User Management

**Purpose**: Handles all user-related operations including registration, login, authentication, and password hashing.

**Classes**:

| Class | Type | Responsibility |
|-------|------|----------------|
| User | Entity | Represents a user with username and password hash |
| Auth | Abstract Base Class | Defines authentication interface |
| SimpleAuth | Concrete Implementation | Implements custom simple hash for password storage |
| UserManager | Manager/Service | Coordinates user operations, registration, login, and session management |

**UserManager Methods**:
- `register(username, password)` - Register a new user
- `login(username, password)` - Authenticate a user
- `logout()` - Log out current user
- `get_current_user()` - Get the currently logged in user
- `is_logged_in()` - Check if user is logged in
- `delete_user(user_id)` - Delete a user account
- `get_all_users()` - Get all registered users

**Benefits**:
- **Encapsulation**: All user-related logic is self-contained
- **Abstraction**: Auth abstract class allows future authentication methods to be added easily
- **Security**: Passwords are never stored in plain text; custom hashing protects user credentials
- **Extensibility**: New authentication strategies can be added by implementing the Auth interface
- **Separation of Concerns**: UserManager separates business logic from data access

**Design Rationale**:
- Using an abstract base class for Auth follows the Strategy pattern, making the system flexible for future authentication methods (e.g., if later adding OAuth or JWT)
- SimpleAuth provides a lightweight, dependency-free password hashing solution suitable for an in-memory application
- UserManager acts as a facade, coordinating between User entity, authentication, and database layers

---

### 3.2 task.py - Task Management

**Purpose**: Defines the Task entity, enumerations, and task management operations.

**Classes/Enums**:

| Class/Enum | Type | Responsibility |
|------------|------|----------------|
| Priority | Enum | Defines task priority levels: LOW, MEDIUM, HIGH, CRITICAL |
| Status | Enum | Defines task status: TODO, INPROGRESS, DONE, CANCELLED |
| Task | Entity | Represents a task with all properties (name, description, priority, deadline, status) |
| TaskManager | Manager/Service | Coordinates task CRUD operations, queries, and user-task associations |

**Task Properties**:
- `name/summary` (string, required)
- `description` (string, optional)
- `priority` (Priority enum, default: LOW)
- `deadline` (date, optional)
- `status` (Status enum, default: TODO)

**TaskManager Methods**:
- `create_task(user_id, name, description, priority, deadline, status)` - Create a new task
- `get_tasks_by_user(user_id)` - Get all tasks for a user
- `get_task_by_id(task_id)` - Get a task by ID
- `update_task(task_id, name, description, priority, deadline, status)` - Update a task
- `delete_task(task_id)` - Delete a task
- `get_tasks_by_status(user_id, status)` - Get tasks filtered by status
- `get_tasks_by_priority(user_id, priority)` - Get tasks filtered by priority
- `get_overdue_tasks(user_id)` - Get overdue tasks (deadline passed, not done/cancelled)
- `mark_as_done(task_id)` - Mark task as DONE
- `mark_as_inprogress(task_id)` - Mark task as INPROGRESS
- `mark_as_cancelled(task_id)` - Mark task as CANCELLED
- `get_all_tasks()` - Get all tasks in system
- `delete_user_tasks(user_id)` - Delete all tasks for a user

**Benefits**:
- **Type Safety**: Enums prevent invalid priority or status values
- **Clarity**: Using enums makes code self-documenting
- **Validation**: Enum constraints are enforced at the type level
- **Maintainability**: Changing priority/status values only requires updating the enum definition
- **Separation of Concerns**: TaskManager handles business logic, while Task is a simple data entity

**Design Rationale**:
- Enums are used instead of strings to provide type safety and IDE autocomplete support
- Keeping Task as a simple data class with no business logic follows the Single Responsibility Principle
- TaskManager acts as a facade, coordinating between Task entity, database tables, and user-task associations

---

### 3.3 database.py - Data Storage

**Purpose**: Provides CRUD (Create, Read, Update, Delete) operations using in-memory data structures.

**Classes**:

| Class | Type | Responsibility |
|-------|------|----------------|
| DBTable | Abstract Base Class | Defines database table interface |
| UserTable | Concrete Implementation | Stores and manages User objects |
| TaskTable | Concrete Implementation | Stores and manages Task objects |
| UserTasksTable | Concrete Implementation | Manages relationship between users and their tasks |

**Additional Query Methods**:

| Class | Method | Description |
|-------|--------|-------------|
| UserTable | `find_by_username(username)` | Find a user by username |
| UserTasksTable | `find_by_user_id(user_id)` | Find all task associations for a user |
| UserTasksTable | `find_by_task_id(task_id)` | Find all user associations for a task |
| UserTasksTable | `delete_by_user_id(user_id)` | Delete all associations for a user |
| UserTasksTable | `delete_by_task_id(task_id)` | Delete all associations for a task |

**Data Storage**:
- Uses Python's built-in `list` and `dict` data structures
- No external database or persistence layer

**Benefits**:
- **Abstraction**: DBTable abstract class defines a consistent interface for all tables
- **Consistency**: Common operations (add, update, delete, find) are defined in the base class
- **Simplicity**: Using built-in datatypes eliminates external dependencies
- **Testability**: In-memory storage makes unit testing straightforward
- **Query Flexibility**: Additional finder methods enable efficient data retrieval by different keys

**Design Rationale**:
- Abstract base class (DBTable) follows the Template Method pattern, ensuring consistent behavior across all tables
- Separate UserTasksTable allows for efficient querying of tasks per user
- The table classes act as repositories, providing a clean separation between data access and business logic

---

### 3.4 main.py - CLI and Orchestration

**Purpose**: Handles command-line interface, user interaction, and coordinates all modules.

**Classes** (if complexity warrants separation):

| Class | Responsibility |
|-------|----------------|
| CLI | Handles all user input/output operations |
| Application | Orchestrates the flow between modules |

**Responsibilities**:
- Display startup menu (Login/Register)
- Display main menu with username and task list
- Handle task selection and actions
- Form input with default value support
- Task ordering (Critical first, then by date)

**Benefits**:
- **Separation of Concerns**: CLI handling is separated from business logic
- **User Experience**: Clear menu navigation and input prompts
- **Flexibility**: If CLI grows complex, can be extracted without affecting other modules

**Design Rationale**:
- Keeping CLI in main.py initially avoids over-engineering; separate classes can be introduced if needed
- The orchestrator pattern ensures clean flow between authentication, task management, and display

---

## 4. Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                              │
│  (CLI & Orchestration)                                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    user.py    │    │   task.py     │    │  database.py  │
│               │    │               │    │               │
│ - User        │    │ - Priority    │    │ - UserTable   │
│ - Auth        │    │ - Status      │    │ - TaskTable   │
│ - SimpleAuth  │    │ - Task        │    │ - UserTasks   │
│ - UserManager │    │ - TaskManager │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Flow**:
1. Application starts → main.py presents Login/Register options
2. User registers/logs in → UserManager handles authentication via SimpleAuth
3. After login → TaskManager retrieves user's tasks from database
4. Tasks displayed → Task provides task structure, database tables retrieve data
5. User creates/updates/deletes → TaskManager coordinates CRUD via TaskTable and UserTasksTable
6. Changes reflected → main.py refreshes the display

---

## 5. Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         user.py                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐        ┌─────────────────┐                      │
│  │   User   │        │ Auth (ABC)      │                      │
│  ├──────────┤        ├─────────────────┤                      │
│  │ id       │        │ + hash()        │                      │
│  │ username │        │ + verify()      │                      │
│  │ password │        └────────┬────────┘                      │
│  └──────────┘                 │                                │
│                               │                                │
│                    ┌──────────┴──────────┐                    │
│                    │    SimpleAuth        │                    │
│                    ├──────────────────────┤                    │
│                    │ + hash(password)     │                    │
│                    │ + verify(password)   │                    │
│                    └──────────────────────┘                    │
│                                                                 │
│  ┌──────────────────────────────────────────┐                 │
│  │           UserManager                     │                 │
│  ├──────────────────────────────────────────┤                 │
│  │ + register(username, password)           │                 │
│  │ + login(username, password)               │                 │
│  │ + logout()                                │                 │
│  │ + get_current_user()                     │                 │
│  │ + is_logged_in()                         │                 │
│  │ + delete_user(user_id)                   │                 │
│  │ + get_all_users()                        │                 │
│  └──────────────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         task.py                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────────┐ │
│  │ Priority  │  │  Status  │  │            Task              │ │
│  ├──────────┤  ├──────────┤  ├──────────────────────────────┤ │
│  │ LOW       │  │ TODO     │  │ id: int                      │ │
│  │ MEDIUM    │  │ INPROGRESS│ │ name: str                    │ │
│  │ HIGH      │  │ DONE      │ │ description: str (optional)  │ │
│  │ CRITICAL  │  │ CANCELLED │ │ priority: Priority           │ │
│  └──────────┘  └──────────┘  │ deadline: date (optional)   │ │
│                              │ status: Status               │ │
│                              └──────────────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    TaskManager                             │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │ + create_task(user_id, name, ...)                         │ │
│  │ + get_tasks_by_user(user_id)                             │ │
│  │ + get_task_by_id(task_id)                                │ │
│  │ + update_task(task_id, ...)                              │ │
│  │ + delete_task(task_id)                                   │ │
│  │ + get_tasks_by_status(user_id, status)                   │ │
│  │ + get_tasks_by_priority(user_id, priority)               │ │
│  │ + get_overdue_tasks(user_id)                             │ │
│  │ + mark_as_done(task_id)                                  │ │
│  │ + mark_as_inprogress(task_id)                            │ │
│  │ + mark_as_cancelled(task_id)                            │ │
│  │ + get_all_tasks()                                        │ │
│  │ + delete_user_tasks(user_id)                             │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       database.py                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐                                         │
│  │   DBTable (ABC)  │                                         │
│  ├──────────────────┤                                         │
│  │ + add()          │                                         │
│  │ + update()       │                                         │
│  │ + delete()       │                                         │
│  │ + find_by_id()   │                                         │
│  │ + find_all()     │                                         │
│  └────────┬─────────┘                                         │
│           │                                                   │
│     ┌─────┴─────┬─────────────┐                               │
│     ▼           ▼             ▼                               │
│ ┌─────────┐ ┌─────────┐ ┌─────────────┐                      │
│ │UserTable│ │TaskTable│ │UserTasksTable│                     │
│ │         │ │         │ │             │                      │
│ │+find_by_│ │         │ │+find_by_    │                      │
│ │ username│ │         │ │ user_id     │                      │
│ └─────────┘ └─────────┘ │+find_by_    │                      │
│                         │ task_id     │                      │
│                         │+delete_by_  │                      │
│                         │ user_id     │                      │
│                         │+delete_by_  │                      │
│                         │ task_id     │                      │
│                         └─────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Design Principles Applied

| Principle | Application |
|-----------|-------------|
| **Single Responsibility** | Each module/class has one clear purpose |
| **Open/Closed** | New authentication methods can be added without modifying existing code |
| **Dependency Inversion** | Abstract classes (Auth, DBTable) define interfaces; concrete implementations depend on abstractions |
| **Encapsulation** | User data and password handling are encapsulated in user.py |
| **Separation of Concerns** | User management, task definition, data storage, and CLI are in separate modules |

---

## 7. Advantages of This Architecture

1. **No External Dependencies**: Uses only Python standard library
2. **In-Memory Storage**: Fast read/write operations, no database setup required
3. **Modular**: Each component can be tested and modified independently
4. **Extensible**: Easy to add new features (e.g., different auth methods)
5. **Maintainable**: Clear separation of concerns makes the codebase easy to understand
6. **Testable**: In-memory storage and modular design simplify unit testing

---

## 8. Future Extensibility

The architecture supports easy addition of:
- Different authentication methods (OAuth, JWT) by implementing Auth abstract class
- New database backends (file-based, SQL) by implementing DBTable abstract class
- Additional CLI views or a future GUI by separating presentation from business logic
- Task categories/tags by extending the Task class or adding new tables

</content>
</invoke>

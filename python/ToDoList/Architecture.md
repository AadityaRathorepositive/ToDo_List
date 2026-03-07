# Architecture Document

## 1. Overview

This document outlines the technical architecture of the Todo application. The system is designed as a modular, in-memory application using Python's built-in data structures without external dependencies.

## 2. Module Structure

The application is organized into four main modules:

```
ToDoList/
├── user.py      # User management and authentication
├── item.py      # Task/item definitions and enums
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

**Benefits**:
- **Encapsulation**: All user-related logic is self-contained
- **Abstraction**: Auth abstract class allows future authentication methods to be added easily
- **Security**: Passwords are never stored in plain text; custom hashing protects user credentials
- **Extensibility**: New authentication strategies can be added by implementing the Auth interface

**Design Rationale**:
- Using an abstract base class for Auth follows the Strategy pattern, making the system flexible for future authentication methods (e.g., if later adding OAuth or JWT)
- SimpleAuth provides a lightweight, dependency-free password hashing solution suitable for an in-memory application

---

### 3.2 item.py - Task Management

**Purpose**: Defines the Task entity and related enumerations.

**Classes/Enums**:

| Class/Enum | Type | Responsibility |
|------------|------|----------------|
| Priority | Enum | Defines task priority levels: LOW, MEDIUM, HIGH, CRITICAL |
| Status | Enum | Defines task status: TODO, INPROGRESS, DONE, CANCELLED |
| Item | Entity | Represents a task with all properties (name, description, priority, deadline, status) |

**Item Properties**:
- `name/summary` (string, required)
- `description` (string, optional)
- `priority` (Priority enum, default: LOW)
- `deadline` (date, optional)
- `status` (Status enum, default: TODO)

**Benefits**:
- **Type Safety**: Enums prevent invalid priority or status values
- **Clarity**: Using enums makes code self-documenting
- **Validation**: Enum constraints are enforced at the type level
- **Maintainability**: Changing priority/status values only requires updating the enum definition

**Design Rationale**:
- Enums are used instead of strings to provide type safety and IDE autocomplete support
- Keeping Item as a simple data class with no business logic follows the Single Responsibility Principle

---

### 3.3 database.py - Data Storage

**Purpose**: Provides CRUD (Create, Read, Update, Delete) operations using in-memory data structures.

**Classes**:

| Class | Type | Responsibility |
|-------|------|----------------|
| DBTable | Abstract Base Class | Defines database table interface |
| UserTable | Concrete Implementation | Stores and manages User objects |
| ItemTable | Concrete Implementation | Stores and manages Item objects |
| UserItemsTable | Concrete Implementation | Manages relationship between users and their items |

**Data Storage**:
- Uses Python's built-in `list` and `dict` data structures
- No external database or persistence layer

**Benefits**:
- **Abstraction**: DBTable abstract class defines a consistent interface for all tables
- **Consistency**: Common operations (add, update, delete, find) are defined in the base class
- **Simplicity**: Using built-in datatypes eliminates external dependencies
- **Testability**: In-memory storage makes unit testing straightforward

**Design Rationale**:
- Abstract base class (DBTable) follows the Template Method pattern, ensuring consistent behavior across all tables
- Separate UserItemsTable allows for efficient querying of tasks per user
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
│    user.py    │    │   item.py     │    │  database.py  │
│               │    │               │    │               │
│ - User        │    │ - Priority    │    │ - UserTable   │
│ - Auth        │    │ - Status      │    │ - ItemTable   │
│ - SimpleAuth  │    │ - Item        │    │ - UserItems   │
└───────────────┘    └───────────────┘    └───────────────┘
```

**Flow**:
1. Application starts → main.py presents Login/Register options
2. User registers/logs in → user.py handles authentication
3. After login → main.py retrieves user's tasks from database
4. Tasks displayed → item.py provides task structure, database.py retrieves data
5. User creates/updates/deletes → database.py performs CRUD operations
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
│  │ username │        │ + hash()        │                      │
│  │ password │        │ + verify()      │                      │
│  └──────────┘        └────────┬────────┘                      │
│                               │                                │
│                    ┌──────────┴──────────┐                    │
│                    │    SimpleAuth        │                    │
│                    ├──────────────────────┤                    │
│                    │ + hash(password)     │                    │
│                    │ + verify(password)   │                    │
│                    └──────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         item.py                                │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────────┐ │
│  │ Priority  │  │  Status  │  │            Item              │ │
│  ├──────────┤  ├──────────┤  ├──────────────────────────────┤ │
│  │ LOW       │  │ TODO     │  │ name: str                    │ │
│  │ MEDIUM    │  │ INPROGRESS│ │ description: str (optional)  │ │
│  │ HIGH      │  │ DONE      │ │ priority: Priority           │ │
│  │ CRITICAL  │  │ CANCELLED │ │ deadline: date (optional)   │ │
│  └──────────┘  └──────────┘  │ status: Status               │ │
│                              └──────────────────────────────┘ │
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
│ │UserTable│ │ItemTable│ │UserItemsTable│                     │
│ └─────────┘ └─────────┘ └─────────────┘                      │
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
- Task categories/tags by extending the Item class or adding new tables

</content>
</invoke>

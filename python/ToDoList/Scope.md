# Scope Document

## 1. Project Overview
This is a simple Todo application that allows users to manage their tasks. The application is built with minimal dependencies - no external systems, no packages, and no databases. All data is stored in-memory.

## 2. Functional Requirements

### 2.1 User Management
- **Registration**: Users can register with a unique username and password
- **Login**: Users can authenticate using their credentials
- **Password Storage**: Passwords are stored using a custom simple hash function

### 2.2 Task Management
Users can perform the following operations on their own tasks:
- **Create**: Add new tasks
- **Read**: View tasks
- **Update**: Modify existing tasks
- **Delete**: Remove tasks

### 2.3 Task Properties
Each task contains the following fields:
| Field | Type | Required | Default |
|-------|------|----------|---------|
| name/summary | string | Yes | - |
| description | string | No | null |
| priority | enum | No | LOW |
| deadline | date | No | null |
| status | enum | No | Todo |

### 2.4 Enums

**Priority:**
- LOW (default)
- MEDIUM
- HIGH
- CRITICAL

**Status:**
- TODO (default)
- INPROGRESS
- DONE
- CANCELLED

### 2.5 Task Ordering
On startup, users will see all their tasks ordered by:
- **Critical priority tasks** take precedence over date (appear first)
- **Non-critical tasks** are sorted by date (earliest deadline first)

## 3. Technical Requirements

### 3.1 Architecture
- Single application with in-memory storage
- No external database systems
- No third-party packages/libraries
- Custom implementation for:
  - Password hashing
  - User authentication
  - Data storage

### 3.2 Data Storage
- All data stored in-memory (RAM)
- Data persists only during application runtime
- No file-based persistence

### 3.3 CLI Interface

#### 3.3.1 Startup Flow
- On application start, prompt user to either **Login** or **Register**
- Display welcome message and options for authentication

#### 3.3.2 Main Menu (After Login)
- Display current **username** at the top of the screen
- Display all tasks in the specified order:
  1. Critical priority tasks first (sorted by date)
  2. Non-critical tasks sorted by date (earliest deadline first)
- Show task number/index for each task for selection

#### 3.3.3 Task Interaction
- **View Task Details**: Enter task number to view full details and perform actions
- **Create New Task**: Type 'N' or 'n' to create a new task
- **Form Input Rules**:
  - Empty input (press Enter without value) assigns the default value for that field
  - Required fields (name/summary) must have a value entered

#### 3.3.4 Task Actions
- View task details
- Update task properties
- Delete task
- Change task status
- Navigate back to main menu

## 4. Out of Scope

The following are explicitly **NOT** part of this project:

### 4.1 User Interface
- No GUI components
- No web frontend

### 4.2 Database
- No SQL database (MySQL, PostgreSQL, SQLite, etc.)
- No NoSQL database (MongoDB, Redis, etc.)

### 4.3 Persistence
- No file-based storage
- No data export/import functionality
- No backup mechanisms

### 4.4 Complex Authentication
- No OAuth
- No JWT tokens
- No session management
- No password reset functionality
- No email verification

### 4.5 Additional Features
- No task sharing between users
- No task categories/tags
- No notifications or reminders
- No task dependencies
- No subtasks
- No file attachments
- No collaboration features

## 5. Constraints
- Application must run as a standalone program
- All functionality must be implemented from scratch without external libraries
- User can only access/modify their own tasks


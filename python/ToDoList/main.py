"""
main.py - CLI and Orchestration Module

Handles command-line interface, user interaction, and coordinates all modules.

Classes:
    - CLI: Handles all user input/output operations
    - Application: Orchestrates the flow between modules
"""

import os
from datetime import date
from typing import Optional

from database import UserTable, TaskTable, UserTasksTable
from user import SimpleAuth, UserManager
from task import Priority, Status, Task, TaskManager


class CLI:
    """
    Handles all user input/output operations.
    
    Responsibilities:
    - Display menus and prompts
    - Get user input with validation
    - Format and display data
    """
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str):
        """Print a formatted header."""
        width = 60
        print("=" * width)
        print(f"{title:^{width}}")
        print("=" * width)
    
    @staticmethod
    def print_auth_menu():
        """Display authentication menu."""
        CLI.clear_screen()
        CLI.print_header("WELCOME TO TODO APP")
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        print("-" * 40)
    
    @staticmethod
    def print_main_menu(username: str, tasks: list):
        """Display main menu with username and task list."""
        CLI.clear_screen()
        CLI.print_header(f"TODO LIST - {username}")
        
        if not tasks:
            print("\nNo tasks yet. Create one!")
        else:
            print("\nYOUR TASKS:")
            print("-" * 60)
            
            for i, task in enumerate(tasks, 1):
                # Format deadline display
                deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
                status_symbol = {
                    Status.TODO: "[ ]",
                    Status.INPROGRESS: "[~]",
                    Status.DONE: "[X]",
                    Status.CANCELLED: "[-]"
                }.get(task.status, "[ ]")
                
                # Format priority display
                priority_str = f"*{task.priority.name}*" if task.priority == Priority.CRITICAL else task.priority.name
                
                print(f"{i}. {status_symbol} {task.name}")
                print(f"   Priority: {priority_str:10} | Deadline: {deadline_str} | Status: {task.status.value}")
                print()
        
        print("-" * 60)
        print("N/n - Create New Task")
        print("Q/q - Logout and Exit")
        print("-" * 60)
    
    @staticmethod
    def print_task_details(task: Task):
        """Display full task details."""
        print("\n" + "=" * 60)
        print("TASK DETAILS")
        print("=" * 60)
        print(f"Name:        {task.name}")
        print(f"Description: {task.description if task.description else '(none)'}")
        print(f"Priority:    {task.priority.value}")
        print(f"Deadline:    {task.deadline.strftime('%Y-%m-%d') if task.deadline else '(none)'}")
        print(f"Status:      {task.status.value}")
        print("=" * 60)
    
    @staticmethod
    def get_input(prompt: str, default: Optional[str] = None) -> str:
        """
        Get user input with optional default value.
        
        Args:
            prompt: Input prompt message
            default: Default value if user enters nothing
            
        Returns:
            User input or default value
        """
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    
    @staticmethod
    def get_choice(prompt: str, valid_choices: list) -> str:
        """
        Get validated user choice.
        
        Args:
            prompt: Input prompt message
            valid_choices: List of valid choice strings
            
        Returns:
            Valid user choice
        """
        while True:
            choice = input(prompt).strip().upper() + ": "
            if choice in [c.upper() for c in valid_choices]:
                return choice
            print(f"Invalid choice. Valid options: {', '.join(valid_choices)}")
    
    @staticmethod
    def get_task_form_data() -> dict:
        """
        Collect new task data from user.
        
        Returns:
            Dictionary with task data
        """
        print("\n--- Create New Task ---")
        
        # Name (required)
        name = CLI.get_input("Task name/summary", None)
        while not name:
            print("Task name is required!")
            name = CLI.get_input("Task name/summary", None)
        
        # Description (optional)
        description = CLI.get_input("Description", "(optional)")
        
        # Priority
        print("\nPriority options: LOW, MEDIUM, HIGH, CRITICAL")
        priority_str = CLI.get_input("Priority", "LOW").upper()
        try:
            priority = Priority(priority_str)
        except ValueError:
            print("Invalid priority, defaulting to LOW")
            priority = Priority.LOW
        
        # Deadline
        deadline_str = CLI.get_input("Deadline (YYYY-MM-DD)", "(optional)")
        deadline = None
        if deadline_str and deadline_str != "(optional)":
            try:
                deadline = date.fromisoformat(deadline_str)
            except ValueError:
                print("Invalid date format, skipping deadline")
        
        return {
            'name': name,
            'description': description if description != "(optional)" else None,
            'priority': priority,
            'deadline': deadline
        }
    
    @staticmethod
    def get_task_update_data(task: Task) -> dict:
        """
        Collect updated task data from user.
        
        Args:
            task: Current task to update
            
        Returns:
            Dictionary with updated task data
        """
        print("\n--- Update Task (press Enter to keep current value) ---")
        
        # Name
        new_name = CLI.get_input(f"Name", task.name)
        if not new_name:
            new_name = task.name
        
        # Description
        current_desc = task.description if task.description else ""
        new_desc = CLI.get_input("Description", current_desc)
        
        # Priority
        print(f"\nCurrent priority: {task.priority.value}")
        print("Priority options: LOW, MEDIUM, HIGH, CRITICAL")
        priority_input = CLI.get_input("Priority", task.priority.value)
        try:
            priority = Priority(priority_input.upper())
        except ValueError:
            priority = task.priority
        
        # Deadline
        current_deadline = task.deadline.strftime("%Y-%m-%d") if task.deadline else "(none)"
        deadline_input = CLI.get_input("Deadline (YYYY-MM-DD)", current_deadline)
        deadline = task.deadline
        if deadline_input and deadline_input != "(none)":
            try:
                deadline = date.fromisoformat(deadline_input)
            except ValueError:
                print("Invalid date format, keeping current deadline")
        
        # Status
        print(f"\nCurrent status: {task.status.value}")
        print("Status options: TODO, INPROGRESS, DONE, CANCELLED")
        status_input = CLI.get_input("Status", task.status.value)
        try:
            status = Status(status_input.upper())
        except ValueError:
            status = task.status
        
        return {
            'name': new_name,
            'description': new_desc if new_desc else None,
            'priority': priority,
            'deadline': deadline,
            'status': status
        }
    
    @staticmethod
    def get_status_change() -> Optional[Status]:
        """
        Get new status from user.
        
        Returns:
            New Status or None to cancel
        """
        print("\nChange Status:")
        print("1. TODO")
        print("2. INPROGRESS")
        print("3. DONE")
        print("4. CANCELLED")
        print("0. Cancel")
        
        choice = CLI.get_choice("Select status", ["1", "2", "3", "4", "0"])
        
        status_map = {
            "1": Status.TODO,
            "2": Status.INPROGRESS,
            "3": Status.DONE,
            "4": Status.CANCELLED
        }
        
        return status_map.get(choice)
    
    @staticmethod
    def pause():
        """Wait for user to press Enter."""
        input("\nPress Enter to continue...")
    
    @staticmethod
    def print_message(message: str):
        """Print a message to user."""
        print(f"\n{message}")
    
    @staticmethod
    def print_error(message: str):
        """Print an error message."""
        print(f"\nERROR: {message}")


class Application:
    """
    Orchestrates the flow between modules.
    
    Responsibilities:
    - Initialize database and managers
    - Handle application flow
    - Coordinate between user management and task management
    """
    
    def __init__(self):
        """Initialize the application with database tables and managers."""
        # Initialize database tables
        self._user_table = UserTable()
        self._task_table = TaskTable()
        self._user_tasks_table = UserTasksTable()
        
        # Initialize managers
        self._user_manager = UserManager(self._user_table, SimpleAuth())
        self._task_manager = TaskManager(self._task_table, self._user_tasks_table)
        
        # CLI instance
        self._cli = CLI()
    
    def run(self):
        """Main application loop."""
        while True:
            # Handle authentication
            authenticated = self._handle_auth()
            
            if not authenticated:
                break
            
            # Handle main menu
            self._handle_main_menu()
    
    def _handle_auth(self) -> bool:
        """
        Handle authentication flow (login/register).
        
        Returns:
            True if authenticated, False to exit
        """
        while True:
            self._cli.print_auth_menu()
            choice = self._cli.get_choice("Choose option", ["1", "2", "3"])
            
            if choice == "3":
                # Exit
                self._cli.print_message("Goodbye!")
                return False
            
            if choice == "1":
                # Login
                if self._login():
                    return True
            elif choice == "2":
                # Register
                self._register()
    
    def _login(self) -> bool:
        """
        Handle login process.
        
        Returns:
            True if login successful
        """
        self._cli.clear_screen()
        self._cli.print_header("LOGIN")
        
        username = self._cli.get_input("Username")
        password = self._cli.get_input("Password")
        
        user = self._user_manager.login(username, password)
        
        if user:
            self._cli.print_message(f"Welcome back, {user.username}!")
            self._cli.pause()
            return True
        else:
            self._cli.print_error("Invalid username or password")
            self._cli.pause()
            return False
    
    def _register(self):
        """Handle registration process."""
        self._cli.clear_screen()
        self._cli.print_header("REGISTER")
        
        while True:
            username = self._cli.get_input("Choose username")
            password = self._cli.get_input("Choose password")
            
            try:
                user = self._user_manager.register(username, password)
                self._cli.print_message(f"Registration successful! Welcome, {user.username}!")
                self._cli.pause()
                break
            except ValueError as e:
                self._cli.print_error(str(e))
                # Let user try again
    
    def _handle_main_menu(self):
        """Handle main menu after successful login."""
        user = self._user_manager.get_current_user()
        
        while True:
            # Get and order tasks
            tasks = self._task_manager.get_tasks_by_user(user.id)
            ordered_tasks = self._order_tasks(tasks)
            
            # Display main menu
            self._cli.print_main_menu(user.username, ordered_tasks)
            
            choice = input("\nEnter task number to view/edit, or option: ").strip()
            
            if choice.upper() == "Q":
                # Logout
                self._user_manager.logout()
                self._cli.print_message("Logged out successfully!")
                return
            
            if choice.upper() == "N":
                # Create new task
                self._handle_task_create(user.id)
                continue
            
            # Try to parse as task number
            try:
                task_index = int(choice) - 1
                if 0 <= task_index < len(ordered_tasks):
                    self._handle_task_view(ordered_tasks[task_index])
                else:
                    self._cli.print_error("Invalid task number")
                    self._cli.pause()
            except ValueError:
                self._cli.print_error("Invalid input")
                self._cli.pause()
    
    def _handle_task_view(self, task: Task):
        """
        Display task details and handle actions.
        
        Args:
            task: Task to view
        """
        while True:
            self._cli.clear_screen()
            self._cli.print_task_details(task)
            
            print("\nActions:")
            print("1. Update Task")
            print("2. Change Status")
            print("3. Delete Task")
            print("0. Back to Main Menu")
            
            choice = self._cli.get_choice("Select action", ["1", "2", "3", "0"])
            
            if choice == "0":
                return
            
            if choice == "1":
                self._handle_task_update(task)
                # Refresh task data
                task = self._task_manager.get_task_by_id(task.id)
            elif choice == "2":
                new_status = self._cli.get_status_change()
                if new_status:
                    success = self._task_manager.update_task(task.id, status=new_status)
                    if success:
                        self._cli.print_message("Status updated!")
                        task = self._task_manager.get_task_by_id(task.id)
                    else:
                        self._cli.print_error("Failed to update status")
                self._cli.pause()
            elif choice == "3":
                confirm = self._cli.get_choice("Are you sure? (y/n)", ["y", "n"])
                if confirm == "Y":
                    success = self._task_manager.delete_task(task.id)
                    if success:
                        self._cli.print_message("Task deleted!")
                        self._cli.pause()
                        return
                    else:
                        self._cli.print_error("Failed to delete task")
                        self._cli.pause()
    
    def _handle_task_create(self, user_id: int):
        """
        Create a new task.
        
        Args:
            user_id: ID of user creating the task
        """
        task_data = self._cli.get_task_form_data()
        
        try:
            task = self._task_manager.create_task(
                user_id=user_id,
                name=task_data['name'],
                description=task_data['description'],
                priority=task_data['priority'],
                deadline=task_data['deadline'],
                status=Status.TODO
            )
            self._cli.print_message(f"Task '{task.name}' created successfully!")
            self._cli.pause()
        except ValueError as e:
            self._cli.print_error(str(e))
            self._cli.pause()
    
    def _handle_task_update(self, task: Task):
        """
        Update an existing task.
        
        Args:
            task: Task to update
        """
        update_data = self._cli.get_task_update_data(task)
        
        success = self._task_manager.update_task(
            task_id=task.id,
            name=update_data['name'],
            description=update_data['description'],
            priority=update_data['priority'],
            deadline=update_data['deadline'],
            status=update_data['status']
        )
        
        if success:
            self._cli.print_message("Task updated successfully!")
        else:
            self._cli.print_error("Failed to update task")
        
        self._cli.pause()
    
    def _order_tasks(self, tasks: list) -> list:
        """
        Order tasks per Scope requirements:
        1. CRITICAL priority tasks first (sorted by date)
        2. Non-critical tasks sorted by date (earliest deadline first)
        
        Args:
            tasks: List of Task objects
            
        Returns:
            Ordered list of tasks
        """
        # Separate critical and non-critical tasks
        critical_tasks = [t for t in tasks if t.priority == Priority.CRITICAL]
        non_critical_tasks = [t for t in tasks if t.priority != Priority.CRITICAL]
        
        # Sort critical tasks by deadline (None at end)
        critical_tasks.sort(key=lambda t: (t.deadline is None, t.deadline or date.max))
        
        # Sort non-critical tasks by deadline (None at end)
        non_critical_tasks.sort(key=lambda t: (t.deadline is None, t.deadline or date.max))
        
        # Combine: critical first, then non-critical
        return critical_tasks + non_critical_tasks


def main():
    """Entry point for the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()


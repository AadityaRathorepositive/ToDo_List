"""
task.py - Task Management Module

Defines the Task entity and related enumerations for the Todo application.

Classes/Enums:
    - Priority: Enum for task priority levels
    - Status: Enum for task status
    - Task: Entity representing a task
    - TaskManager: Manages task operations
"""

from enum import Enum
from typing import Optional
from datetime import date


class Priority(Enum):
    """
    Enum representing task priority levels.
    
    Attributes:
        LOW: Low priority tasks
        MEDIUM: Medium priority tasks
        HIGH: High priority tasks
        CRITICAL: Critical priority tasks
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Status(Enum):
    """
    Enum representing task status.
    
    Attributes:
        TODO: Task needs to be done
        INPROGRESS: Task is currently being worked on
        DONE: Task has been completed
        CANCELLED: Task has been cancelled
    """
    TODO = "TODO"
    INPROGRESS = "INPROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class Task:
    """
    Entity class representing a task in the system.
    
    Attributes:
        id: Unique identifier for the task
        name: Name/summary of the task (required)
        description: Detailed description (optional)
        priority: Priority level (default: Priority.LOW)
        deadline: Due date (optional)
        status: Current status (default: Status.TODO)
    """
    
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: Optional[str] = None,
        priority: Priority = Priority.LOW,
        deadline: Optional[date] = None,
        status: Status = Status.TODO
    ):
        """
        Initialize a Task instance.
        
        Args:
            id: Unique task ID (None for new tasks)
            name: Task name/summary (required)
            description: Task description (optional)
            priority: Priority level (default: LOW)
            deadline: Due date (optional)
            status: Current status (default: TODO)
        """
        self.id = id
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = status
    
    def __repr__(self) -> str:
        """Return string representation of Task."""
        return f"Task(id={self.id}, name='{self.name}', priority={self.priority.name}, status={self.status.name})"
    
    def to_dict(self) -> dict:
        """
        Convert Task to dictionary.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority.value if isinstance(self.priority, Priority) else self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status.value if isinstance(self.status, Status) else self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create Task instance from dictionary.
        
        Args:
            data: Dictionary with task data
            
        Returns:
            Task instance
        """
        # Get name (required field)
        name = data.get('name', '')
        if not name:
            raise ValueError("Task name is required")
        
        # Convert priority string to Priority enum
        priority_value = data.get('priority', 'LOW')
        if isinstance(priority_value, str):
            priority = Priority(priority_value.upper())
        else:
            priority = priority_value
        
        # Convert status string to Status enum
        status_value = data.get('status', 'TODO')
        if isinstance(status_value, str):
            status = Status(status_value.upper())
        else:
            status = status_value
        
        # Parse deadline if present
        deadline_value = data.get('deadline')
        if deadline_value and isinstance(deadline_value, str):
            deadline = date.fromisoformat(deadline_value)
        else:
            deadline = deadline_value
        
        return cls(
            id=data.get('id'),
            name=name,
            description=data.get('description'),
            priority=priority,
            deadline=deadline,
            status=status
        )
    
    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        deadline: Optional[date] = None,
        status: Optional[Status] = None
    ) -> None:
        """
        Update task properties.
        
        Args:
            name: New task name (optional)
            description: New description (optional)
            priority: New priority level (optional)
            deadline: New deadline (optional)
            status: New status (optional)
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if priority is not None:
            self.priority = priority
        if deadline is not None:
            self.deadline = deadline
        if status is not None:
            self.status = status


class TaskManager:
    """
    Manages task operations including creation, retrieval, update, and deletion.
    
    This class coordinates between Task entity and database, providing
    a high-level interface for task management.
    """
    
    def __init__(self, task_table, user_tasks_table):
        """
        Initialize TaskManager.
        
        Args:
            task_table: Database table for tasks (TaskTable instance)
            user_tasks_table: Database table for user-task associations (UserTasksTable instance)
        """
        self._task_table = task_table
        self._user_tasks_table = user_tasks_table
    
    def create_task(
        self,
        user_id: int,
        name: str,
        description: Optional[str] = None,
        priority: Priority = Priority.LOW,
        deadline: Optional[date] = None,
        status: Status = Status.TODO
    ) -> Task:
        """
        Create a new task for a user.
        
        Args:
            user_id: ID of the user who owns this task
            name: Task name/summary (required)
            description: Task description (optional)
            priority: Priority level (default: LOW)
            deadline: Due date (optional)
            status: Initial status (default: TODO)
            
        Returns:
            Created Task instance
            
        Raises:
            ValueError: If name is empty or invalid
        """
        # Validate inputs
        if not name or not name.strip():
            raise ValueError("Task name cannot be empty")
        
        # Create task record
        task_data = {
            'name': name.strip(),
            'description': description.strip() if description else None,
            'priority': priority.value,
            'deadline': deadline.isoformat() if deadline else None,
            'status': status.value
        }
        
        # Add to task table
        created_task = self._task_table.add(task_data)
        
        # Create user-task association
        self._user_tasks_table.add({
            'user_id': user_id,
            'task_id': created_task.get('id')
        })
        
        return Task.from_dict(created_task)
    
    def get_tasks_by_user(self, user_id: int) -> list[Task]:
        """
        Get all tasks for a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of Task instances owned by the user
        """
        # Get all task associations for this user
        associations = self._user_tasks_table.find_by_user_id(user_id)
        
        tasks = []
        for assoc in associations:
            task_id = assoc.get('task_id')
            task_data = self._task_table.find_by_id(task_id)
            if task_data:
                tasks.append(Task.from_dict(task_data))
        
        return tasks
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task instance or None if not found
        """
        task_data = self._task_table.find_by_id(task_id)
        return Task.from_dict(task_data) if task_data else None
    
    def update_task(
        self,
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        deadline: Optional[date] = None,
        status: Optional[Status] = None
    ) -> bool:
        """
        Update a task.
        
        Args:
            task_id: Task ID
            name: New name (optional)
            description: New description (optional)
            priority: New priority (optional)
            deadline: New deadline (optional)
            status: New status (optional)
            
        Returns:
            True if update successful, False otherwise
        """
        update_data = {}
        
        if name is not None:
            if not name.strip():
                raise ValueError("Task name cannot be empty")
            update_data['name'] = name.strip()
        
        if description is not None:
            update_data['description'] = description.strip() if description else None
        
        if priority is not None:
            update_data['priority'] = priority.value
        
        if deadline is not None:
            update_data['deadline'] = deadline.isoformat() if deadline else None
        
        if status is not None:
            update_data['status'] = status.value
        
        if not update_data:
            return False
        
        return self._task_table.update(task_id, update_data)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if deletion successful, False otherwise
        """
        # Delete user-task associations first
        self._user_tasks_table.delete_by_task_id(task_id)
        
        # Delete the task itself
        return self._task_table.delete(task_id)
    
    def get_tasks_by_status(self, user_id: int, status: Status) -> list[Task]:
        """
        Get all tasks for a user with a specific status.
        
        Args:
            user_id: User ID
            status: Status to filter by
            
        Returns:
            List of Task instances with the specified status
        """
        all_tasks = self.get_tasks_by_user(user_id)
        return [task for task in all_tasks if task.status == status]
    
    def get_tasks_by_priority(self, user_id: int, priority: Priority) -> list[Task]:
        """
        Get all tasks for a user with a specific priority.
        
        Args:
            user_id: User ID
            priority: Priority to filter by
            
        Returns:
            List of Task instances with the specified priority
        """
        all_tasks = self.get_tasks_by_user(user_id)
        return [task for task in all_tasks if task.priority == priority]
    
    def get_overdue_tasks(self, user_id: int) -> list[Task]:
        """
        Get all overdue tasks for a user (deadline passed and not done/cancelled).
        
        Args:
            user_id: User ID
            
        Returns:
            List of overdue Task instances
        """
        today = date.today()
        all_tasks = self.get_tasks_by_user(user_id)
        
        overdue = []
        for task in all_tasks:
            if (task.deadline and 
                task.deadline < today and 
                task.status not in [Status.DONE, Status.CANCELLED]):
                overdue.append(task)
        
        return overdue
    
    def mark_as_done(self, task_id: int) -> bool:
        """
        Mark a task as done.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_task(task_id, status=Status.DONE)
    
    def mark_as_inprogress(self, task_id: int) -> bool:
        """
        Mark a task as in progress.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_task(task_id, status=Status.INPROGRESS)
    
    def mark_as_cancelled(self, task_id: int) -> bool:
        """
        Mark a task as cancelled.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful, False otherwise
        """
        return self.update_task(task_id, status=Status.CANCELLED)
    
    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks in the system (admin function).
        
        Returns:
            List of all Task instances
        """
        tasks_data = self._task_table.find_all()
        return [Task.from_dict(task) for task in tasks_data]
    
    def delete_user_tasks(self, user_id: int) -> int:
        """
        Delete all tasks for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of tasks deleted
        """
        associations = self._user_tasks_table.find_by_user_id(user_id)
        count = 0
        for assoc in associations:
            task_id = assoc.get('task_id')
            self._task_table.delete(task_id)
            count += 1
        
        self._user_tasks_table.delete_by_user_id(user_id)
        return count


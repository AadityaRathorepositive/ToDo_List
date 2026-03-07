from abc import ABC, abstractmethod
from typing import Any

class DatabaseTable(ABC):
    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def query(self, **criteria)-> list[Any]:
        pass

    @abstractmethod
    def update(self, data, **criteria):
        pass

    @abstractmethod
    def delete(self, **criteria):
        pass

class UserTable(DatabaseTable):

    def __init__(self):
        self.create_table()

    def create_table(self):
        # Code to create user table
        self.Users = []
        # self.Users = ["User1", "User2", "User3"]
        

    def insert(self, data):
        # Code to insert user data
        self.Users.append(data)

    def query(self, **criteria):
        # Code to query user data based on criteria
        results = []
        for user in self.Users:
            if all(user.get(key) == value for key, value in criteria.items()):
                results.append(user)
        return results

    def update(self, data, **criteria):
        for user in self.Users:
            if all(user.get(key) == value for key, value in criteria.items()):
                user.update(data)
                break

    def delete(self, **criteria):
        # Code to delete user data based on criteria
        for user in self.Users:
            if all(user.get(key) == value for key, value in criteria.items()):
                self.Users.remove(user)
                break

class TaskTable(DatabaseTable):

    def __init__(self):
        self.create_table()

    def create_table(self):
        # Code to create task table
        self.Tasks = []
        # self.Tasks = ["Task1", "Task2", "Task3"]

    def insert(self, data):
        # Code to insert task data
        self.Tasks.append(data)

    def query(self, **criteria):
        # Code to query task data based on criteria
        results = []
        for task in self.Tasks:
            if all(task.get(key) == value for key, value in criteria.items()):
                results.append(task)
        return results

    def update(self, data, **criteria):
        for task in self.Tasks:
            if all(task.get(key) == value for key, value in criteria.items()):
                task.update(data)
                break

    def delete(self, **criteria):
        # Code to delete task data based on criteria
        for task in self.Tasks:
            if all(task.get(key) == value for key, value in criteria.items()):
                self.Tasks.remove(task)
                break

class UserTasksTable(DatabaseTable):

    def __init__(self):
        self.create_table()

    def create_table(self):
        # Code to create user-tasks relationship table
        self.UserTasks = []
        # self.UserTasks = [{"user": "User1", "task": "Task1"}, {"user": "User2", "task": "Task2"}]

    def insert(self, data):
        # Code to insert user-task relationship data
        self.UserTasks.append(data)

    def query(self, **criteria):
        # Code to query user-task relationship data based on criteria
        results = []
        for user_task in self.UserTasks:
            if all(user_task.get(key) == value for key, value in criteria.items()):
                results.append(user_task)
        return results

    def update(self, data, **criteria):
        for user_task in self.UserTasks:
            if all(user_task.get(key) == value for key, value in criteria.items()):
                user_task.update(data)
                break

    def delete(self, **criteria):
        # Code to delete user-task relationship data based on criteria
        for user_task in self.UserTasks:
            if all(user_task.get(key) == value for key, value in criteria.items()):
                self.UserTasks.remove(user_task)
                break
        
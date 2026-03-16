from operator import ge


DB = []
# [
#     {'username': 'user1',
#     'age': 18,
#     'tasks': [
#         {'title': 'some task',
#         'priority': 'high',
#         'status': 'In Progress'},
        # {'title': 'task',
#         'priority': 'low',
#         'status': 'Done'}
#     ]},
#     {'username': 'user2',
#     'age': 8,
#     'tasks': [
#         {'title': 'task',
#         'priority': 'low',
#         'status': 'Done'}
#     ]}
# ]


def user_exists(username):
    for user in DB:
        if user['username'] ==  username:
            return True
    return False    

def add_user(username):
    age = int(input(f'Enter age for {username}: '))
    DB.append({'username': username, 'age': age, 'tasks': []})

def print_user_menu(menu):
    print('--'*5)
    print('Menu:')
    for i,item in enumerate(menu):
        print(f'{i+1}. {item}')
    print('--'*5)

def get_user(username):
    for user in DB:
        if user['username'] == username:
            return user

def get_task_from_user():
    title = input('Enter task title: ')
    priority = input('Enter task priority: ')
    task = {'title': title, 'priority': priority, 'status': 'In Progress'}
    return task

def add_task(user, task):
    user['tasks'].append(task)
    print(f'Task added for {user['username']}')

def view_tasks(user):
    tasks = user['tasks']
    print('##'*20)
    for i, item in enumerate(tasks):
            print(f'{i+1}. {item}')
    print('##'*5)

def update_task(user, task_title, new_task):
    tasks = user['tasks']
    for task in tasks:
        if task['title'] == task_title:
            task = new_task
    print('updated') 

def task_exists(task_title, user):
    tasks = user['tasks']
    for task in tasks:
        if task['title'] == task_title:
            return True
    return False

def updated_values_from_user(task_title, user):
    for task in user['tasks']:
        if task['title'] == task_title:
            current_task = task
            break
    print('update task, enter new value or enter to keep old value')
    new_title = input(f"title: {current_task['title']} -->")
    if new_title.strip() == '':
        new_title = current_task['title']
    
    new_priority = input(f"priority: {current_task['priority']} -->")
    if new_priority.strip() == '':
        new_priority = current_task['priority']
    
    new_status = input(f"status: {current_task['status']} -->")
    if new_status.strip() == '':
        new_status = current_task['status']
    
    return {'title': new_title, 'priority': new_priority, 'status': new_status}

def task_manager(username):
    user = get_user(username)
    while True:
        menu = [
            "view all tasks", #0
            'add task', #1
            'mark as done', #2 # 3 #4
            'quit' #5
        ]
        print_user_menu(menu)
        user_selection = int(input('Enter your choice: '))
        command = menu[user_selection-1]
        
        if command == 'add task':
            task = get_task_from_user()
            add_task(user, task)
        elif command == 'view all tasks':
            view_tasks(user)
        elif command == 'mark as done':
            view_tasks(user)
            task_title = input("Enter title of task to update: ")
            if task_exists(task_title, user):
                new_task = updated_values_from_user(task_title, user)
                update_task(user, task_title, new_task)
            else:
                print('task does not exist')
        elif command == 'quit':
            break

def user_manager():
    while True:
        username = input('Enter your username: ')
        if user_exists(username):
            task_manager(username)
        else:
            add_new_user = input("User not found. Add this user? y/n: ")
            if not add_new_user.lower().strip()=='y':
                break
            else:
                add_user(username)
                task_manager(username)
        switch_user = input('switch to new user? y/n: ')
        if switch_user.lower().strip() == 'y':
            continue
        else:
            break


def main():
    user_manager()

main()
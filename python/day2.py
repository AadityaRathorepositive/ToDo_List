# to do list


menu = [
    "show tasks", #0
    'add task', #1
    'mark as done', #2
    'delete task', # 3
    'show completed', #4
    'quit' #5
]

# added in memory db
db = {}

'''db = {'user1': {
            'todo': [], 
            'done': []
            }, 
            
        'user2':{
            'todo': [],
            'done': []
        }
    }
'''

# function to fetch username
def get_user():
    username = input('Username: ')
    return username

# function to fetch todo_list and done_list for user
def get_todo_list_for_user(user):
    todo_list = db[user]['todo']
    done_list = db[user]['done']
    return todo_list, done_list

# add user and intialize todo, done list 
def add_user(user):
    if not user in db.keys():
        db[user]= {
            'todo': [],
            'done': []
        }
        print('User added')
    else:
        print('user already exists')

def print_menu():
    print('--'*5)
    print('Menu:')

    for i,item in enumerate(menu):
        print(f'{i+1}. {item}')


def print_array(array, message=''):
    print(message)
    print('#'*10)
    for i, item in enumerate(array):
        print(f'{i+1}: {item}')
    print('#'*10)

#  updated fucntion to manage all todo commands for one user
def manage_todo_for_user(username):
    todo, done = get_todo_list_for_user(username)
    # continue loop for one user until unser exists
    while True:
        print_menu()
        
        user_input = int(input('Enter your choice: '))

        if user_input > len(menu): #6 
            print('Invalid Input')

        command = menu[user_input-1] 

        if command == 'show tasks':
            if not todo:
                print('No tasks to show')
            else:
                print_array(todo, "To Do Tasks:")

        elif command == 'add task':
            new_task = input('task : ')
            todo.append(new_task)
            print_array(todo, 'Your todo list')

        elif command == 'mark as done':
            task_position = int(input('enter your task position: '))
            task = todo.pop(task_position-1)
            done.append(task)
            print_array(done, "completed tasks:")
            print_array(todo, 'Pending tasks')

        elif command == 'delete task':
            delete_task = input("delete task name: ")
            if delete_task in todo:
                todo.remove(delete_task)
                print_array(todo, 'deleted from todo. todo list is: ')

            if delete_task in done:
                done.remove(delete_task)
                print_array(done,'deleted from done. done list is: ' )

        elif command == 'show completed':
            if not done:
                print('No tasks to show')
            print_array(done)

        elif command == 'quit':
            return

def main():
    while True:
        # fetch user
        user1 = get_user()
        # check if user exists
        if not user1 in db.keys():
            add_new_user = input("User not found. Add this user? y/n: ")
            if not add_new_user.lower().strip()=='y':
                break
            else:
                # addd user if not exists and user wants to add
                add_user(user1)
        # start function for that user
        manage_todo_for_user(user1)
        # after user quits ask if new user to manage
        switch_user = input('switch to new user? y/n: ')
        if switch_user.lower().strip() == 'y':
            # continue loop if yes
            continue
        else:
            # exit loop if no
            break


main()





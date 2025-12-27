# to do list

# menu as a lgloabl ist
# to provide common interface for entire program
# easy to update and add new items
menu = [
    "show tasks", #0
    'add task', #1
    'mark as done', #2
    'delete task', # 3
    'show completed', #4
    'quit' #5
]

# created a function to print menu
# to avoid rewriting code
# and easy to change format everywhere
def print_menu(menu):
    print('--'*5)
    print('Menu:')
    # index works as dynamic sl. no
    # no need to change sl no of items id new items are added 
    for i,item in enumerate(menu):
        print(f'{i+1}. {item}')

# since printing an array was a repetetive operation
# created a fucntion to print items in an array
def print_array(array, message=''):
    print(message)
    print('#'*10)
    for i, item in enumerate(array):
        print(f'{i+1}: {item}')
    print('#'*10)

# function to handle todo operations
# all items provided as parameters
# so easier to handle for different menus and users
# scalable and resuable
def todo(user_input, menu, todo, done):
    
    user_input = int(user_input)

    if user_input > len(menu): #6 
        print('Invalid Input')

    # if user input = 3
    # menu[3-1] = menu[2]
    # command = menu[2]
    # command = 'mark as done'
    command = menu[user_input-1] 

    # checking against actual commands rather than sl.no
    # avoids changing conditions when new items are added in menu
    if command == 'show tasks':
        if not todo:
            print('No tasks to show')
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
        exit()

def main():
    todo_list =[]
    done_list = []
    
    while True:
        print_menu(menu)
        user_input = input('Enter your choice: ')

        todo(user_input, menu, todo_list, done_list)

main()





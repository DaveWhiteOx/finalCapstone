# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
max_task_no = 0 
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    curr_t['task_no'] = task_components[6]

    task_list.append(curr_t)

    # Update max_task_no with current highest value so when adding task we do not repeat used number
    if int(task_components[6]) > max_task_no:
        max_task_no = int(task_components[6])


# Define functions for registering user, adding and viewing tasks.
def reg_user():
        '''Add a new user to the user.txt file'''
        # - Set control variable for loop
        user_exists = True

        # - Request input of a new username and check if exists in user.txt
        while user_exists:
            new_username = input("New Username: ")
            with open("user.txt", "r") as f:
                if new_username not in f.read():
                    user_exists = False
                else:
                    print("Username already exists, please try again")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")


def add_task():
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        

        # Get current max_task_no value and increment by 1
        global max_task_no 
        max_task_no = max_task_no +1
        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
            "task_no": str(max_task_no)
        }

        # Add new task to the list and write to task file
        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No",
                    t['task_no']
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


def view_all():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Task No: \t {t['task_no']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)


def view_mine():
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        for t in task_list:
            if t['username'] == curr_user:
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Task No: \t {t['task_no']}\n"
                disp_str += f"Assigned to: \t {t['username']}\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \n {t['description']}\n"
                print(disp_str)

        vm_choice = 0
        while vm_choice != -1:
            vm_choice = input("To view a specific task enter the task number or enter -1 to return to main menu: ")
            if vm_choice == '-1':
                break
            task_found = False
            for idx, t in enumerate(task_list):
                if t['username'] == curr_user and t['task_no'] == vm_choice:
                    disp_str = f"Task: \t\t {t['title']}\n"
                    disp_str += f"Task No: \t {t['task_no']}\n"
                    disp_str += f"Assigned to: \t {t['username']}\n"
                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Task Description: \n {t['description']}\n"
                    print(disp_str)
                    task_found = True

                    # Prompt user with editing options
                    edit_option = int(input("Enter 1 to mark task as complete, 2 to update the task or 3 to return: "))
                    if edit_option == 1:
                        t['completed'] = True
                        task_list[idx] = t
                    elif edit_option == 2:
                        if t['completed'] == True:
                            print("This task cannot be edited as it is marked as complete.")
                            continue
                        choice = int(input("Enter 1 to update assignment or 2 to change the Due Date: "))
                        if choice == 1:
                            assign = input("Enter user to assign task to: ").lower()
                            t['username'] = assign
                            task_list[idx] = t
                        elif choice == 2:
                            while True:
                                try:
                                    date_due = input("Due date of task (YYYY-MM-DD): ")
                                    due_date_time = datetime.strptime(date_due, DATETIME_STRING_FORMAT)
                                    break

                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")

                                t['due_date'] = due_date_time
                                task_list[idx] = t

                    else:
                        continue
                    
                    # Write any updates made to user tasks to the task file
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No",
                                t['task_no']
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                    print("Task successfully updated.")
                
                # Display message to user if no task with the given task number was found
                # and we have reached the end of our list
                elif task_found == False and idx == len(task_list)-1:
                    print("Task Not Found")


def gen_reports():
    # Generate the task overview report file
    num_tasks = len(task_list)
    now = datetime.now()
    num_tasks_compl = 0
    num_tasks_incompl = 0
    num_tasks_overdue = 0
    perc_tasks_incompl = 0
    perc_tasks_overdue = 0
    for t in task_list:
        num_tasks_compl += sum(1 for value in t.values() if value == True)
        num_tasks_incompl += sum(1 for value in t.values() if value == False)
        if t['due_date'] < now and t['completed'] == False:
            num_tasks_overdue += 1

    if num_tasks_incompl > 0:
        perc_tasks_incompl = round(num_tasks_incompl/(num_tasks - num_tasks_compl) * 100, 2)
    
    if num_tasks_overdue > 0:
        perc_tasks_overdue = round(num_tasks_overdue/(num_tasks - num_tasks_compl) * 100, 2)

    # Open task_overview.txt or create it if it doesn't exist
    with open("task_overview.txt", 'w+') as task_view:
        task_view.write(f"============== Task Overview Report ==============\n")
        task_view.write(f"Total Number of Tasks: {num_tasks}\n")
        task_view.write(f"Total Number of Completed Tasks: {num_tasks_compl}\n")
        task_view.write(f"Total Number of Incomplete Tasks: {num_tasks_incompl}\n")
        task_view.write(f"Total Number of Tasks Currently Overdue: {num_tasks_overdue}\n")
        task_view.write(f"Percentage of Tasks Incomplete: {perc_tasks_incompl}%\n")
        task_view.write(f"Percentage of Tasks Overdue: {perc_tasks_overdue}%\n")        
        task_view.write("===================================================")
        
    # Generate the user overview report file
    with open("user_overview.txt", 'w+') as user_view:
        num_users = len(username_password.keys())
        user_view.write("============== User Overview Report ===============\n")
        user_view.write(f"Total Number of Users: {num_users}\n")
        user_view.write(f"Total Number of Tasks: {num_tasks}\n")
        
        for user in username_password.keys():
            user_tasks = 0
            user_tasks_overdue = 0
            user_task_compl = 0
            perc_user_compl = 0
            perc_user_incompl = 0
            perc_user_overdue = 0
            for t in task_list:     
                if t['username'] == user:
                    user_tasks += 1
                    if t['completed'] == True:
                        user_task_compl += 1
                    elif t['due_date'] < now and t['completed'] == False:
                        user_tasks_overdue += 1
            
            user_task_perc = round(user_tasks/num_tasks * 100, 2)
            
            if user_task_compl > 0:
                perc_user_compl = user_task_compl/user_tasks * 100

            if user_tasks > 0:
                perc_user_incompl = round((user_tasks - user_task_compl)/user_tasks * 100, 2)

            if user_tasks_overdue > 0:
                perc_user_overdue = user_tasks_overdue/user_tasks * 100

            
            user_view.write(f"User Stats for {user}\n")
            user_view.write(f"Total Number of Tasks Assigned: {user_tasks}\n")
            user_view.write(f"Percentage of Overall Tasks Assigned: {user_task_perc}%\n")
            user_view.write(f"Percentage of Tasks Completed: {perc_user_compl}%\n")
            user_view.write(f"Percentage of Tasks Incomplete: {perc_user_incompl}%\n")
            user_view.write(f"Percentage of Tasks Overdue: {perc_user_overdue}%\n")
            user_view.write("===================================================\n")


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

        ''' Reports only available to admin user,
        first the function is called to generate the reports to individual files,
        following this we read the file contents to display on screen to the user
        '''
    elif menu == 'gr' and curr_user == 'admin':
        gen_reports()
        with open("task_overview.txt", 'r') as task_report:
            lines = task_report.read()
            print(lines)

        with open("user_overview.txt", 'r') as user_report:
            lines = user_report.read()
            print(lines)

    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
# Q1. What will the following code display?
numbers = [1, 2, 3, 4, 5]
print(numbers[1:-5])
# answer_q1: it will return an empty list [],
# in order to return the entire list, we can do numbers[:] or numbers[0:5]
print(numbers[:],'or',numbers[0:5])

# Q2.  Design a program that asks the user to enter a store’s sales for each day of the
#  week. The amounts should be stored in a list. Use a loop to calculate the total sales for
#  the week and display the result
import calendar
from datetime import datetime
from tabulate import tabulate

i = 0
store_sales=[]
weekday_num = datetime.today().weekday()
#I will use while loop
while i < 7:
    weekday_name = calendar.day_name[i]
    store_sales_day = float(input(f'Enter the store sales for {weekday_name}: '))
    sub_list = [weekday_name, store_sales_day]
    store_sales.append(sub_list)
    i += 1

print(f'A list with sublist was created {store_sales}')
# Now I will calculate the total sales for the week
total_sales = sum(sale[1] for sale in store_sales)
store_sales.append(["Total Sales",total_sales])

#for better visualization I will print the list as a table
print(tabulate(store_sales, headers=['Week Day','Sales']))

# Q3. Create a list with at least 5 places you’d like to travel to.   Make sure the list isn’t in
# alphabetical order
# ● Print your list in its original order.
# ● Use the sort() function to arrange your list in order and reprint your list.
# ● Use the sort(reverse=True) and reprint your list

place_to_travel = ['India','Italy','Switzerland','Spain','Colombia']
print(f' No sort {place_to_travel}')
place_to_travel.sort()
print(f' Using sort {place_to_travel}')
place_to_travel.sort(reverse=True)
print(f' Using sort with reverse=True {place_to_travel}')

#Q4. Write a program that creates a dictionary containing course numbers and the room
# numbers of the rooms where the courses meet. The program should also create a
# dictionary containing course numbers and the names of the instructors that teach each
# course. After that, the program should let the user enter a course number, then it should
# display the course’s room number, instructor, and meeting time
program_course_room = {
    1: ['DATA1', '301'],
    2: ['DATA2', '303'],
    3: ['DATA3', '305'],
    4: ['DATA4', '304'],
    5: ['DATA5', '307']
}
program_course_professor = {
    1: ['DATA1', 'Brian'],
    2: ['DATA2', 'Mike'],
    3: ['DATA3', 'Stefan'],
    4: ['DATA4', 'Juan'],
    5: ['DATA5', 'Robert']
}
course_number = str(input('Enter a course number: ')).upper()
found = False

for key, value in program_course_room.items():
    if course_number in value:
        print(f'The course {course_number} room is {program_course_room[key][1]}')
        found = True
        for key2, value2 in program_course_professor.items():
            if course_number in value2:
                print(f'The professor is {program_course_professor[key2][1]}')
                break
        break

if found == False:
    print(f'The course {course_number} was not found')

# Q5. Write a program that keeps names and email addresses in a dictionary as
# key-value pairs. The program should then demonstrate the four options:
# ● look up a person’s email address,
# ● add a new name and email address,
# ● change an existing email address, and
# ● delete an existing name and email address


personal_email= {
    "name": ['Juan'],
    "email": ['s@s.com']
}

# I will create a menu with the 4 options
def options_menu():
    print('Select one of the following options:')
    print('1. Look up a person’s email address')
    print('2. Add a new name and email address')
    print('3. Change an existing email address')
    print('4. Delete an existing name and email address')

def option1():
    print('You selected look up a person’s email address')
    name = str(input('Enter the name: '))
    if name in personal_email["name"]:
            email = personal_email["email"][personal_email["name"].index(name)]
            print(f'The email address for {name} is {email}')

    else:
            print(f'The name {name} was not found')

def option2():
    print('You selected Add a new name and email address')
    name = str(input('Enter the name: '))
    email = str(input('Enter the email: '))
    personal_email['name'].append(name)
    personal_email['email'].append(email)
    print(f' The new name and email address was added.\n Current names:\n {personal_email}')

def option3():
    print('You selected Change an existing email address')
    name = str(input('Enter the name: '))
    if name in personal_email["name"]:
            email = str(input('Enter the new email: '))
            personal_email["email"][personal_email["name"].index(name)]=email
            print(f'The person’s email address was updated to {email}')
    else:
            print(f'The name {name} was not found')

def option4():
    print('You selected Delete an existing name and email address')
    name = str(input('Enter the name: '))
    if name in personal_email["name"]:
            index_d = personal_email["name"].index(name)
            del personal_email["name"][index_d]
            del personal_email["email"][index_d]
            print(f'The person’s information was deleted.\n Current names:\n {personal_email}')
    else:
            print(f'The name {name} was not found')



def main():
    while True:
        options_menu()
        option = int(input('Enter the number of the option: '))
        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        else:
            print('Invalid option')

if __name__ == "__main__":
    main()

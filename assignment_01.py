# Q1 Fix all the syntax and logical errors in the given source code
# add comments to explain your reasoning

# This program gets three test scores and displays their average.  It congratulates the user if the
# average is a high score. The high score variable holds the value that is considered a high score.

HIGH_SCORE = 95

# Get the test scores.
# AS: I added int(), so I can convert the input to an integer and store the calculation in the variable
test1 = int(input('Enter the score for test 1: '))
test2 = int(input('Enter the score for test 2: '))
test3 = int(input('Enter the score for test 3: '))
# Calculate the average test score.
# AS: I added () to the calculation, so the SUM is done first and then divided by 3
average = (test1 + test2 + test3) / 3
# Print the average.
print('The average score is', average)
# If the average is a high score,
# congratulate the user.
# AS: the correct name of the variable is upper case HIGH_SCORE, also I added a tab to the second print statement so it's only printing if the condition is met
if average >= HIGH_SCORE:
    print('Congratulations!')
    print('That is a great average!')

# Q2
# The area of a rectangle is the rectangle’s length times its width. Write a program that asks for the length and width of two rectangles and prints to the user the area of both rectangles.
rectangle1_length = int(input("Enter the length of the first rectangle: "))
rectangle1_width = int(input("Enter the width of the first rectangle: "))
rectangle2_length = int(input("Enter the length of the second rectangle: "))
rectangle2_width = int(input("Enter the width of the second rectangle: "))

rectangle1_area = rectangle1_length * rectangle1_width
rectangle2_area = rectangle2_length * rectangle2_width

print(f"The area of the first rectangle is {rectangle1_area} and the area of the second rectangle is {rectangle2_area}")

# Q3
# Ask a user to enter their first name and their age and assign it to the variables name and age.
# The variable name should be a string and the variable age should be an int.
name = input("Enter your first name: ")
age = int(input("Enter your age: "))
print("Name is type:", type(name))
print("Age is type:", type(age))

# Using the variables name and age, print a message to the user stating something along the lines of:
# "Happy birthday, name!  You are age years old today!"
print("Happy birthday,", name, "!", "You are", age, "years old today!")
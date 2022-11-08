def userGreeting(password = 'defaultPassword'):
    """
    This function greets the user, and calls passwordCheck() to check for password match.

    Parameter: The selected password for the function.
    """

    print('Welcome back! Please enter your name.')
    userName = input()
    print(f'Thank you {userName}. Please enter your password.')
    passwordCheck(input(), password)

def passwordCheck(userPassword, storedPassword):
    """
    This function is used to validate if correct password has been entered. Will keep repeating until correct pw is entered.

    Parameters: The input entered by the user, and the optional argument passed through userGreeting.
    """

    if userPassword == storedPassword:
        print('Login has been authorized')
    else: 
        print('The password entered was incorrect. Please enter the correct password')
        passwordCheck(input(), storedPassword)

userGreeting()

# I wanted the function to keep attempting to validate the password. I initially tried using a loop,
# but decided to create another function, which could then repeatedly call itself upon wrong input.
# I wanted to use local variables, and thus i needed to pass the (optional) password argument through to passwordCheck as well.
# I used conditional statements for controlling the flow. 

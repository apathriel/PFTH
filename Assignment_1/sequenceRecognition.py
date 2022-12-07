"""
    Title: Sequence recognition + sequence generation
    Author: Gabriel Høst Andersen
    Date: 13/09/22
"""

def sequenceGenerator():

    """
    This function will generate a sequence of fibonacci numbers, length is determined by the parameter.
    """

    number = int(input('Input number: '))
    
    fibString = ''
    a, b = 0, 1
    for _ in range(number):
        fibString += str(a)
        fibString += '0'
        a, b = b, a + b
    fibString = fibString[:-1]
    return fibString

def main():
    print(sequenceGenerator())

if __name__ == '__main__':
    main()

# I was able to identify the sequence as the fibonacci sequence,
# but i am bad at math and was unsure of how to begin.
# I use int(input()) in order to convert the datatype to an integer, since input() always returns a string.  
# I largely followed this tutorial from stackoverflow https://stackoverflow.com/questions/3953749/python-fibonacci-generator
# I then modifidied it to return add 0 efter every number sequence using string concatenation, and to return a string instead of a list
# Line 14 is used to remove the last 0, which is not present in the example sequence, decreased indent so it only occurs once. 
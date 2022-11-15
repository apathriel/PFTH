import sys, time

def patternGen(delay = 0.1, size = 10, iterationCount=5):
    """
    This function is used to generate a pattern.

    Parameters: Delay controls the speed at which the pattern is printed. Size controls when the pattern will start decreasing. iterationCount defines 
    """
    patternString = '*'
    stringIncreasing = True
    iterationCounter = 0
  
    try:
        while iterationCounter < iterationCount:
            print(patternString)
            time.sleep(delay)

            if stringIncreasing == True:
                patternString += '*'
                if len(patternString) == size:
                    stringIncreasing = not stringIncreasing

            else: 
                patternString = patternString[:-1]
                if len(patternString) == 1:
                    print(patternString)
                    stringIncreasing = not stringIncreasing 
                    iterationCounter += 1

    except KeyboardInterrupt:
        sys.exit()

    print(f'The pattern has finished after {iterationCount} iterations!')

patternGen(delay=0.2, size=10, iterationCount=3)

# Used this to figure out how to slice last index of string https://geekflare.com/python-remove-last-character/
# Largely followed the example from the Automating the Boring Stuff book. I include the try / except keywords to prevent an infinite loop.
# the sleep() function from the time module is included to manipulate the speed of the pattern (how fast its drawn)
# When the string length reaches either 1 or 10, the boolean is flipped, effectively manipulating the conditional statements.
# Line 28 is included to include double lines of singular * to match the provided pattern. 
# Used global variables, because i figured they might be reassigned everytime the program would return to first line of loop. 
# Made it into a function so you can control the delay and the size of the pattern. 
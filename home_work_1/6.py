class NegativeNumberError(Exception):
    pass

try:
    import math
except ImportError:
    print("error: math module cannot be imported")
    exit(1)

try:
    number = float(input("enter a number: "))
    
    if number < 0:
        raise NegativeNumberError()
    
    result = math.sqrt(number)
    print(f"square root: {result}")
except NegativeNumberError:
    print("error: cannot calculate square root of negative number")
    exit(1)
except ValueError as e:
    print(f"value error: {e}")
    exit(1)

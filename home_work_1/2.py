try:
    a = float(input("enter first number: "))
    b = float(input("enter second number: "))
    result = a / b
except ZeroDivisionError:
    print("error: division by zero is not possible")
    exit(1)
except ValueError:
    print("error: please enter valid numbers")
    exit(1)
else:
    print(f"result: {result}")

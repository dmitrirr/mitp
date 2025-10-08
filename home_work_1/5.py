try:
    user_input = input("enter a number: ")
    number = float(user_input)
    print(f"converted value: {number}")
except ValueError:
    print("error: cannot convert input to number")

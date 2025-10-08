numbers = [10, 20, 30, 40, 50]

try:
    index = int(input("enter index: "))

    if index < 0:
        raise ValueError("index is out of range")

    value = numbers[index]
    print(f"value at index {index}: {value}")
except IndexError:
    print("error: index is out of range")
except ValueError:
    print("error: please enter a valid integer")

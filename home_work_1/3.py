class EvenNumberError(Exception):
    pass

class NegativeNumberError(Exception):
    pass

def validate_and_sum(numbers):
    for num in numbers:
        if num % 2 == 0:
            raise EvenNumberError()
        if num < 0:
            raise NegativeNumberError()
    return sum(numbers)

numbers = [-1, 3, 5, 7, 2]
try:
    sum = validate_and_sum(numbers)
    print(f"sum: {sum}")
except EvenNumberError as e:
    print("list contains an even number:", str(e))
except NegativeNumberError as e:
    print("list contains a negative number:", str(e))
except Exception as e:
    print("error:", str(e))

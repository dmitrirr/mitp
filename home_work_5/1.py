import threading


def print_squares(start: int, end: int) -> None:
    for i in range(start, end + 1):
        print(f"square({i}) = {i * i}")


def print_cubes(start: int, end: int) -> None:
    for i in range(start, end + 1):
        print(f"cube({i}) = {i * i * i}")


if __name__ == "__main__":
    t1 = threading.Thread(target=print_squares, args=(1, 10))
    t2 = threading.Thread(target=print_cubes, args=(1, 10))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

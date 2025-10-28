import threading
import time


def print_numbers() -> None:
    for i in range(1, 11):
        print(i)
        time.sleep(1)


if __name__ == "__main__":
    threads: list[threading.Thread] = []

    for _ in range(2):
        t = threading.Thread(target=print_numbers)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()



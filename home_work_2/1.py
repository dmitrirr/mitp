try:
    with open("source.txt", "r") as file:
        content = file.read()

    with open("destination.txt", "w") as file:
        file.write(content)
except Exception as e:
    print(f"error: {str(e)}")
    exit(1)

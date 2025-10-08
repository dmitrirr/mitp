try:
    with open("text_file.txt", "r") as file:
        content = file.read()
        words = content.split()
        word_count = len(words)
        
        print(f"word count: {word_count}")
except Exception as e:
    print(f"error: {str(e)}")
    exit(1)

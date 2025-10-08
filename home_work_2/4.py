try:
    with open("input.txt", "r") as file:
        lines = file.readlines()
    
    unique_lines = set()
    
    for line in lines:
        unique_lines.add(line)
    
    with open("unique_output.txt", "w") as file:
        file.writelines(unique_lines)
    
    print(f"unique lines saved: {len(unique_lines)}")
except Exception as e:
    print(f"error: {str(e)}")
    exit(1)

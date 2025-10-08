try:
    with open("prices.txt", "r") as file:
        total_cost = 0
        
        for line in file:
            if line:
                parts = line.split("\t")

                name = parts[0]
                quantity = int(parts[1])
                price = int(parts[2])

                cost = quantity * price
                total_cost += cost

                print(f"{name}: {quantity} x {price} = {cost}")
        
        print(f"total cost: {total_cost}")
except Exception as e:
    print(f"error: {str(e)}")
    exit(1)

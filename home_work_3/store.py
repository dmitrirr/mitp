class Product:
    def __init__(self, name: str, price: float, stock: int) -> None:
        if price < 0:
            raise ValueError("price cannot be negative")

        if stock < 0:
            raise ValueError("stock cannot be negative")

        self.name = name
        self.price = price
        self.stock = stock
    
    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("stock cannot be negative")
        
        self.stock = quantity


class Order:
    def __init__(self):
        self.products = {}
    
    def add_product(self, product: Product, quantity: int) -> None:
        if quantity == 0:
            return

        if quantity < 0:
            raise ValueError("quantity cannot be negative")

        if product.stock < quantity:
            raise ValueError("insufficient stock")
        
        if product not in self.products:
            self.products[product] = 0
        
        self.products[product] += quantity
        product.update_stock(product.stock - quantity)
    
    def calculate_total(self) -> float:
        total = 0
        for product, quantity in self.products.items():
            total += product.price * quantity
        return total


class Store:
    def __init__(self):
        self.products = []
    
    def add_product(self, product: Product):
        self.products.append(product)
    
    def list_products(self) -> None:
        for product in self.products:
            print(f"{product.name}: {product.price} руб., в наличии: {product.stock} шт.")
    
    def create_order(self) -> Order:
        return Order()

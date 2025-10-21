class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
    
    def update_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Ошибка: количество не может быть отрицательным")
        
        self.stock = quantity


class Order:
    def __init__(self):
        self.products = {}
    
    def add_product(self, product, quantity):
        if product.stock < quantity:
            raise ValueError("Ошибка: недостаточно товара на складе")
        
        if product not in self.products:
            self.products[product] = 0
        
        self.products[product] += quantity
        product.update_stock(product.stock - quantity)
    
    def calculate_total(self):
        total = 0
        for product, quantity in self.products.items():
            total += product.price * quantity
        return total


class Store:
    def __init__(self):
        self.products = []
    
    def add_product(self, product):
        self.products.append(product)
    
    def list_products(self):
        for product in self.products:
            print(f"{product.name}: {product.price} руб., в наличии: {product.stock} шт.")
    
    def create_order(self):
        return Order()

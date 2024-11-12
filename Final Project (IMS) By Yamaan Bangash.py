class Product:
    LOW_STOCK_THRESHOLD = 5 

    def __init__(self):
        self.inventory = {}

    def add_product(self, product_id, name, category, price, stock_quantity):
        if product_id in self.inventory:
            print("This Product ID already exists in the inventory.")
        else:
            self.inventory[product_id] = {
                "name": name,
                "category": category,
                "price": price,
                "stock_quantity": stock_quantity
            }
            print(f"Product '{name}' has been added to the inventory successfully.")
            self.check_low_stock(product_id)

    def edit_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        if product_id in self.inventory:
            if name:
                self.inventory[product_id]["name"] = name
            if category:
                self.inventory[product_id]["category"] = category
            if price:
                self.inventory[product_id]["price"] = price
            if stock_quantity is not None:
                self.inventory[product_id]["stock_quantity"] = stock_quantity
                self.check_low_stock(product_id)
            print(f"Product ID {product_id} has been updated.")
        else:
            print("Couldn't find the Product ID in the inventory.")

    def delete_product(self, product_id):
        if product_id in self.inventory:
            del self.inventory[product_id]
            print(f"Product ID {product_id} has been removed from the inventory.")
        else:
            print("Couldn't find the Product ID in the inventory.")

    def display_inventory(self):
        if self.inventory:
            for product_id, details in self.inventory.items():
                print(f"ID: {product_id}, Name: {details['name']}, "
                      f"Category: {details['category']}, Price: Rs{details['price']}, "
                      f"Stock: {details['stock_quantity']}")
        else:
            print("The inventory is currently empty.")

    def check_low_stock(self, product_id):
        if self.inventory[product_id]['stock_quantity'] <= self.LOW_STOCK_THRESHOLD:
            print(f"Note: Product ID {product_id} ('{self.inventory[product_id]['name']}') is running low on stock.")


class Cart:
    def __init__(self, inventory):
        self.cart_items = {}
        self.inventory = inventory

    def add_to_cart(self, product_id, quantity):
        if product_id in self.inventory.inventory:
            product = self.inventory.inventory[product_id]
            if product["stock_quantity"] >= quantity:
                self.cart_items[product_id] = {
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity
                }
                print(f"Added {quantity} of '{product['name']}' to your cart.")
            else:
                print(f"Sorry, only {product['stock_quantity']} of '{product['name']}' is available.")
        else:
            print("Couldn't find this Product ID in the inventory.")

    def calculate_total(self):
        total = sum(item["price"] * item["quantity"] for item in self.cart_items.values())
        return total

    def checkout(self):
        print("\n--- Final Bill ---")
        total_amount = self.calculate_total()
        for item_id, item in self.cart_items.items():
            print(f"{item['name']} (x{item['quantity']}): Rs{item['price']} each - Rs{item['price'] * item['quantity']}")
            self.inventory.inventory[item_id]['stock_quantity'] -= item['quantity']
        
        print(f"\nTotal Amount: Rs{total_amount}")
        while True:
            try:
                amount_given = float(input("Enter the payment amount: Rs"))
                if amount_given >= total_amount:
                    change = amount_given - total_amount
                    print(f"Change to return: Rs{change}")
                    print("Thanks for shopping with us!")
                    break
                else:
                    print(f"Insufficient amount. Please enter at least Rs{total_amount}.")
            except ValueError:
                print("Invalid input. Please enter a valid amount.")

    def clear_cart(self):
        self.cart_items = {}


class AuthenticationSystem:
    def __init__(self):
        self.username = "Yamaan"
        self.password = "123"

    def login(self):
        while True:
            print("\n--- User Login ---")
            role = input("Please enter your role Admin or User : ").strip().capitalize()
            
            if role == "Admin":
                return self.admin_login()
            elif role == "User":
                return "User"
            else:
                print("Invalid input. Please enter 'Admin' or 'User'.")

    def admin_login(self):
        while True:
            user = input("Enter your Admin Username: ")
            pwd = input("Enter your Admin Password: ")
            if user == self.username and pwd == self.password:
                print("Welcome, Admin!")
                return "Admin"
            else:
                print("Incorrect credentials. Please try again.")



inventory = Product()
auth_system = AuthenticationSystem()


sample_products = [
    (1, "Laptop", "Electronics", 1500, 10),
    (2, "Smartphone", "Electronics", 700, 3),
    (3, "Headphones", "Accessories", 150, 2),
    (4, "Chair", "Furniture", 80, 15),
    (5, "Desk Lamp", "Lighting", 40, 1),
    (6, "Backpack", "Bags", 35, 20),
    (7, "Notebook", "Stationery", 5, 200),
    (8, "Coffee Maker", "Kitchen", 60, 8),
    (9, "Water Bottle", "Accessories", 10, 4),
    (10, "Bluetooth Speaker", "Electronics", 120, 6)
]

for product in sample_products:
    inventory.add_product(*product)

role = auth_system.login()

if role == "Admin":
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add a New Product")
        print("2. Update an Existing Product")
        print("3. Delete a Product")
        print("4. View Inventory")
        print("5. Logout")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            product_id = int(input("Enter Product ID: "))
            name = input("Enter Product Name: ")
            category = input("Enter Product Category: ")
            price = float(input("Enter Product Price: "))
            stock_quantity = int(input("Enter Stock Quantity: "))
            inventory.add_product(product_id, name, category, price, stock_quantity)

        elif choice == "2":
            product_id = int(input("Enter Product ID to update: "))
            name = input("Enter new Product Name (or press Enter to keep current): ") or None
            category = input("Enter new Product Category (or press Enter to keep current): ") or None
            price = input("Enter new Product Price (or press Enter to keep current): ")
            price = float(price) if price else None
            stock_quantity = input("Enter new Stock Quantity (or press Enter to keep current): ")
            stock_quantity = int(stock_quantity) if stock_quantity else None
            inventory.edit_product(product_id, name, category, price, stock_quantity)

        elif choice == "3":
            product_id = int(input("Enter Product ID to delete: "))
            inventory.delete_product(product_id)

        elif choice == "4":
            inventory.display_inventory()

        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Please select a valid option (1-5).")

elif role == "User":
    user_cart = Cart(inventory)
    print("\n--- Product List ---")
    inventory.display_inventory()
    
    while True:
        print("\n--- User Menu ---")
        print("1. Add an Item to Your Cart")
        print("2. Proceed to Checkout")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            product_id = int(input("Enter Product ID to add to your cart: "))
            quantity = int(input("Enter quantity: "))
            user_cart.add_to_cart(product_id, quantity)

        elif choice == "2":
            user_cart.checkout()
            user_cart.clear_cart()
            break

        elif choice == "3":
            print("Thanks for visiting our store!")
            break
        else:
            print("Please select a valid option (1-3).")

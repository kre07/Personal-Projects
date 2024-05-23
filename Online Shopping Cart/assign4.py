# Kritagya Sharma

class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other): 
         if isinstance(other, Product):
             if  ((self._name == other._name and self._price == other._price) and (self._category==other._category)):
                return True
             else:
                return False
         else:
            return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep

class Inventory:

    # Initialize an empty inventory dictionary
    def __init__ (self):
        self._inventory = {}

     # Add a product to the inventory with price and quantity   
    def add_to_productInventory(self, productName, productPrice, productQuantity):
        self._inventory[productName] = {"Price": int(productPrice), "Quantity": int(productQuantity) }

    # Add quantity to a product in the inventory
    def add_productQuantity(self, nameProduct, addQuantity):
        self._inventory[nameProduct]["Quantity"] += addQuantity # nameProduct is a key for "price" and "quantity"

    # Remove quantity from a product in the inventory
    def remove_productQuantity(self, nameProduct, removeQuantity):
        self._inventory[nameProduct]["Quantity"] -= removeQuantity 
         
    # Get the price of product in the inventory 
    def get_productPrice(self, nameProduct):
        return self._inventory[nameProduct]["Price"]

    # Get quantity of a product in the inventory
    def get_productQuantity(self, nameProduct):
        return self._inventory[nameProduct]["Quantity"]
    
    # Display inventory with product names, prices, and quantities
    def display_Inventory(self): 
        for productName,productValues in self._inventory.items(): # .items returns key and value 
            print(f"{productName}, {productValues['Price']}, {productValues['Quantity']}")


class ShoppingCart:
    # Initialize a shopping cart with a buyer's name and an inventory
    def __init__(self, buyerName, inventory):
        self._buyerName = buyerName
        self._inventory = inventory
        self._shopCart = {}
        

    # Add a product to the shopping cart with a requested quantity    
    def add_to_cart(self, nameProduct, requestedQuantity):
        quantityAvailaible = self._inventory.get_productQuantity(nameProduct) # adjusting the product quantity in the inventory to match what's available for the customer
        if quantityAvailaible >= requestedQuantity:
            if nameProduct in self._shopCart:
                    self._shopCart[nameProduct] = self._shopCart[nameProduct] + requestedQuantity 
            else:
                self._shopCart[nameProduct] = requestedQuantity # If product is not already in the cart
            self._inventory.remove_productQuantity( nameProduct, requestedQuantity) # The requested quantity is the amount you will remove from the order.

            return "Filled the order"

        else:
            return "Can not fill the order"   

    # Remove a product from the shopping cart with a requested quantity
    def remove_from_cart(self, nameProduct, requestedQuantity):
        if nameProduct not in self._shopCart:
            return "Product not in the cart"
        if requestedQuantity > self._shopCart[nameProduct]:
            return "The requested quantity to be removed from cart exceeds what is in the cart"
        self._shopCart[nameProduct] = self._shopCart[nameProduct] - requestedQuantity # Removing from Cart
        self._inventory.add_productQuantity(nameProduct, requestedQuantity) # Adding to inventory
        return "Successful"

    # View the information of the cart with total price and buyer's name
    def view_cart(self):
        totalPrice = 0
        for nameProduct, amountQuantity in self._shopCart.items():
            currentPrice = self._inventory.get_productPrice(nameProduct)
            totalPrice = totalPrice + currentPrice * amountQuantity 
            print(nameProduct, amountQuantity)

        print(f"Total: {totalPrice}" )
        print(f"Buyer Name: {self._buyerName}")


class Catalog:
    # Initialize an  catalog with sets for different prices
    def __init__(self):
        self._products = []
        self._highPrice = set()
        self._mediumPrice = set()
        self._lowPrice = set()

    # Add product to catalog
    def addProduct(self, product):
        self._products.append(product)


    # Categorize products into low, medium, and high price sets
    def price_category(self):
        for products in self._products:
            if products.get_price() >= 0 and  products.get_price() <= 99 : # Going through each product in list and getting their price
                self._lowPrice.add(products.get_name()) # Going through each product in list and seeing what it's name is 
            if products.get_price() >= 100 and  products.get_price() <= 499:
                self._mediumPrice.add(products.get_name())
            if products.get_price() >= 500:
                self._highPrice.add(products.get_name())
        print (f"Number of low price items: {len(self._lowPrice)}")
        print (f"Number of medium price items: {len(self._mediumPrice)}")
        print (f"Number of high price items: {len(self._highPrice)}")


    # Display the catalog with product names, prices, and categories
    def display_catalog(self):
        for products in self._products:
            print (f"Product: {products.get_name()} Price: {products.get_price()} Category: {products.get_category()}")


# Populate inventory from file
def populate_inventory(filename):
    try:
        inventory = Inventory()
        with open(filename, 'r') as file:
            for readLine in file:
                productInfo = readLine.strip().split(",") # .Strip removes spaces, .split puts everything that in a line into a list
                name, price, quantity, notUsedCategory = productInfo 
                inventory.add_to_productInventory(name, int(price), int(quantity))
        return inventory
    except FileNotFoundError:
        print(f"Could not read file: {filename}")
        return None

# Initialize a catalog from file
def populate_catalog(fileName):
    try:
        newCatalog = Catalog()
        with open(fileName, 'r') as file:
            for readLine in file:
                productInfo = readLine.strip().split(",") 
                name, price, notUsedQuantity, category = productInfo 
                oneProduct = Product(name, int(price), category)
                newCatalog.addProduct(oneProduct)
        return newCatalog
    except FileNotFoundError:
        print(f"Could not read file: {fileName}")
        return None

import socket
import json

# Constants
HOST = '127.0.0.1'  # Localhost
PORT = 5555  # Arbitrary port

# Dummy menu data
menu_data = {}

# Owner authentication
def owner_auth(username, password):
    return json.dumps({'type': 'owner_auth', 'username': username, 'password': password})

# Add item to menu
def add_item(item_name, item_price):
    return json.dumps({'type': 'add_item', 'item_name': item_name, 'item_price': item_price})

# Get menu from server
def get_menu():
    return json.dumps({'type': 'get_menu'})

# Customer order
def customer_order(order, delivery_address):
    return json.dumps({'type': 'customer_order', 'order': order, 'delivery_address': delivery_address})

# Main function
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")

        while True:
            role = input("Are you an owner or a customer? (owner/customer): ").lower()
            if role == 'owner' or role == 'customer':  # Corrected input validation
                if role == 'owner':
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    s.sendall(owner_auth(username, password).encode())
                    response = s.recv(1024).decode()
                    print(response)
                    if response == 'Authenticated as owner':
                        while True:
                            action = input("Enter 'add' to add item to menu, 'exit' to exit: ")
                            if action == 'add':
                                item_name = input("Enter item name: ")
                                item_price = float(input("Enter item price: "))
                                s.sendall(add_item(item_name, item_price).encode())
                                print(s.recv(1024).decode())  # Feedback from the server
                            elif action == 'exit':
                                break
                elif role == 'customer':
                    s.sendall(get_menu().encode())
                    menu_data = json.loads(s.recv(1024).decode())
                    print("Menu:")
                    for item, price in menu_data.items():
                        print(f"{item}: ${price}")
                    order = {}
                    while True:
                        item_name = input("Enter item name to order (or type 'done' to finish): ")
                        if item_name == 'done':
                            break
                        quantity = int(input("Enter quantity: "))
                        order[item_name] = quantity
                    delivery_address = input("Enter delivery address: ")
                    s.sendall(customer_order(order, delivery_address).encode())
                    print(s.recv(1024).decode())  # Feedback from the server
            else:
                print("Invalid role. Please enter 'owner' or 'customer'.")

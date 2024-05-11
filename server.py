import socket
import json

# Constants
HOST = '127.0.0.1'  # Localhost
PORT = 5555  # Arbitrary port

# Load menu data from file
def load_menu():
    try:
        with open('menu.json', 'r') as menu_file:
            menu_data = json.load(menu_file)
    except FileNotFoundError:
        menu_data = {}
    return menu_data

# Save menu data to file
def save_menu(menu_data):
    with open('menu.json', 'w') as menu_file:
        json.dump(menu_data, menu_file)

# Authenticate owner
def authenticate_owner(username, password):
    # Dummy authentication, you should implement a secure authentication mechanism
    owners_credentials = {'owner1': 'password1', 'owner2': 'password2'}
    return owners_credentials.get(username) == password

# Handle client connection
# Inside the handle_client function

# Inside the handle_client function

# Inside the handle_client function

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        data = json.loads(data)
        if data['type'] == 'owner_auth':
            username = data['username']
            password = data['password']
            if authenticate_owner(username, password):
                conn.sendall(b'Authenticated as owner')
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    data = json.loads(data)
                    if data['type'] == 'add_item':
                        item_name = data['item_name']
                        item_price = data['item_price']
                        menu_data[item_name] = item_price
                        save_menu(menu_data)
                        conn.sendall(b'Item added successfully')
                    elif data['type'] == 'exit':
                        break
            else:
                conn.sendall(b'Authentication failed')
        elif data['type'] == 'get_menu':
            conn.sendall(json.dumps(menu_data).encode())
        elif data['type'] == 'customer_order':
            order = data['order']
            total_price = sum(menu_data[item] * quantity for item, quantity in order.items())
            delivery_address = data['delivery_address']
            conn.sendall(f'Total price: {total_price}, Delivery address: {delivery_address}'.encode())

    conn.close()




# Main function
if __name__ == "__main__":
    menu_data = load_menu()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

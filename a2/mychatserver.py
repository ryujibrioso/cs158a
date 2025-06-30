import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Dictionary to store client sockets and their addresses
        self.lock = threading.Lock()  # Lock for thread-safe operations on clients dictionary

    def start(self):
        """Start the chat server and listen for incoming connections"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                
                # Add client to dictionary
                with self.lock:
                    self.clients[client_address] = client_socket
                
                # Start a new thread to handle the client
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        """Handle communication with a single client"""
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                if message.lower() == 'exit':
                    self.remove_client(client_socket, client_address)
                    break
                
                # Relay message to all other clients
                self.broadcast(message, client_address)
        except ConnectionResetError:
            print(f"Client {client_address} disconnected unexpectedly")
        finally:
            self.remove_client(client_socket, client_address)

    def broadcast(self, message, sender_address):
        """Send a message to all clients except the sender"""
        with self.lock:
            for address, socket in self.clients.items():
                if address != sender_address:
                    try:
                        formatted_message = f"{sender_address[1]}: {message}"
                        socket.send(formatted_message.encode('utf-8'))
                    except ConnectionError:
                        # Remove client if unable to send
                        self.remove_client(socket, address)

    def remove_client(self, client_socket, client_address):
        """Remove a client from the clients dictionary and close the socket"""
        with self.lock:
            if client_address in self.clients:
                print(f"Client {client_address} disconnected")
                del self.clients[client_address]
                client_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
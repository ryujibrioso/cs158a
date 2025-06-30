import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def start(self):
        """Connect to the server and start send/receive threads"""
        try:
            self.client_socket.connect((self.host, self.port))
            self.running = True
            print("Connected to chat server. Type 'exit' to leave.")
            
            # Start receive thread
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            # Handle user input in main thread
            self.send_messages()
        except ConnectionRefusedError:
            print("Could not connect to the server")
        finally:
            self.client_socket.close()

    def receive_messages(self):
        """Receive messages from server and print them"""
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(message)
            except ConnectionError:
                print("Disconnected from server")
                self.running = False
                break

    def send_messages(self):
        """Get user input and send to server"""
        while self.running:
            message = input()
            try:
                self.client_socket.send(message.encode('utf-8'))
                if message.lower() == 'exit':
                    print("Disconnected from server")
                    self.running = False
                    break
            except ConnectionError:
                print("Disconnected from server")
                self.running = False
                break

if __name__ == "__main__":
    client = ChatClient()
    client.start()
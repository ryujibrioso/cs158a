import uuid
import socket
import threading
import json
import time
from datetime import datetime

class Message:
    def __init__(self, uuid_str, flag=0):
        self.uuid = uuid_str
        self.flag = flag
    
    def to_json(self):
        return json.dumps({'uuid': self.uuid, 'flag': self.flag})
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['uuid'], data['flag'])

class Node:
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.leader_id = None
        self.state = 0  # 0: election in progress, 1: leader elected
        self.left_neighbor = None  # Server connection (we receive from left)
        self.right_neighbor = None  # Client connection (we send to right)
        self.server_socket = None
        self.log_file = open('log.txt', 'a')
        
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        self.log_file.write(log_message)
        self.log_file.flush()
        print(log_message, end='')
    
    def load_config(self, filename='config.txt'):
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.server_ip, self.server_port = lines[0].strip().split(',')
            self.server_port = int(self.server_port)
            self.client_ip, self.client_port = lines[1].strip().split(',')
            self.client_port = int(self.client_port)
    
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)
        self.log(f"Server started on {self.server_ip}:{self.server_port}")
        
        def accept_connection():
            conn, addr = self.server_socket.accept()
            self.left_neighbor = conn
            self.log(f"Accepted connection from {addr}")
            
            # Start receiving messages from left neighbor
            self.receive_messages()
        
        server_thread = threading.Thread(target=accept_connection)
        server_thread.start()
    
    def connect_to_client(self):
        time.sleep(2)  # Wait for server to be ready
        self.right_neighbor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        max_retries = 5
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                self.right_neighbor.connect((self.client_ip, self.client_port))
                self.log(f"Connected to client at {self.client_ip}:{self.client_port}")
                
                # Send initial message with our UUID
                initial_msg = Message(self.uuid, 0)
                self.send_message(initial_msg)
                return
            except ConnectionRefusedError:
                if attempt < max_retries - 1:
                    self.log(f"Connection attempt {attempt + 1} failed, retrying...")
                    time.sleep(retry_delay)
                else:
                    self.log("Failed to connect to client after multiple attempts")
                    raise
    
    def send_message(self, message):
        if self.right_neighbor:
            json_str = message.to_json() + "\n"
            self.right_neighbor.sendall(json_str.encode('utf-8'))
            self.log(f"Sent: uuid={message.uuid}, flag={message.flag}")
    
    def receive_messages(self):
        buffer = ""
        while True:
            try:
                data = self.left_neighbor.recv(1024).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    message_str, buffer = buffer.split("\n", 1)
                    self.process_message(message_str)
            except ConnectionResetError:
                break
    
    def process_message(self, message_str):
        try:
            message = Message.from_json(message_str)
            
            if self.state == 1:
                # Leader already elected, ignore message
                self.log(f"Ignored message (leader already elected): uuid={message.uuid}, flag={message.flag}")
                return
            
            if message.flag == 1:
                # Leader elected message
                self.state = 1
                self.leader_id = message.uuid
                self.log(f"Received leader election: uuid={message.uuid}, flag={message.flag}, leader is {self.leader_id}")
                
                # Forward the message to the right neighbor
                self.send_message(message)
                return
            
            # Compare UUIDs
            comparison = ""
            if message.uuid > self.uuid:
                comparison = "greater"
            elif message.uuid == self.uuid:
                comparison = "same"
            else:
                comparison = "less"
            
            self.log(f"Received: uuid={message.uuid}, flag={message.flag}, {comparison}, {self.state}")
            
            if message.uuid == self.uuid:
                # I am the leader
                self.state = 1
                self.leader_id = self.uuid
                self.log(f"Leader is decided to {self.leader_id}")
                
                # Send leader elected message
                leader_msg = Message(self.uuid, 1)
                self.send_message(leader_msg)
            elif message.uuid > self.uuid:
                # Forward the message
                self.send_message(message)
            else:
                # Ignore messages with smaller UUID
                self.log(f"Ignored message (smaller UUID): uuid={message.uuid}")
        except json.JSONDecodeError:
            self.log(f"Invalid message received: {message_str}")
    
    def run(self):
        self.load_config()
        self.start_server()
        self.connect_to_client()
        
        # Keep the main thread alive
        while True:
            if self.state == 1 and self.leader_id:
                self.log(f"Terminating: leader is {self.leader_id}")
                time.sleep(2)  # Give time for messages to propagate
                break
            time.sleep(1)
        
        # Clean up
        if self.left_neighbor:
            self.left_neighbor.close()
        if self.right_neighbor:
            self.right_neighbor.close()
        if self.server_socket:
            self.server_socket.close()
        self.log_file.close()

if __name__ == "__main__":
    node = Node()
    node.run()
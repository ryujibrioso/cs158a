import socket

def run_client(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        message = input("Input lowercase sentence:")
        
        try:
            msg_len = int(message[:2])
            actual_message = message[2:]
            
            if len(actual_message) != msg_len:
                print("Error: Message length doesn't match the prefix")
                return
        except ValueError:
            print("Error: First two characters must be digits representing length")
            return
        
        s.sendall(msg_len.to_bytes(2, byteorder='big'))
        s.sendall(actual_message.encode('utf-8'))
        
        msg_len_bytes = s.recv(2)
        if not msg_len_bytes:
            print("Connection closed by server")
            return
            
        response_len = int.from_bytes(msg_len_bytes, byteorder='big')
        
        received = 0
        chunks = []
        while received < response_len:
            chunk = s.recv(min(64, response_len - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
        
        response = b''.join(chunks).decode('utf-8')
        print(f"From Server: {response}")

if __name__ == "__main__":
    run_client()
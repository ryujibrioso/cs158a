import socket
import threading

def handle_client(conn, addr):
    with conn:
        print(f"Connected from {addr}")
        
        # Receive the 2-byte length prefix
        msg_len_bytes = conn.recv(2)
        if not msg_len_bytes:
            return
        
        msg_len = int.from_bytes(msg_len_bytes, byteorder='big')
        print(f"msg_len: {msg_len}")
        
        # Receive message in chunks
        received = 0
        chunks = []
        while received < msg_len:
            chunk = conn.recv(min(64, msg_len - received))
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
        
        message = b''.join(chunks).decode('utf-8')
        print(f"processed: {message}")
        
        # Process and respond
        response = message.upper()
        response_len = len(response)
        
        conn.sendall(response_len.to_bytes(2, byteorder='big'))
        conn.sendall(response.encode('utf-8'))
        print(f"msg_len_sent: {response_len}")
    
    print(f"Connection with {addr} closed")

def run_server(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Multi-threaded server listening on {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            client_thread.start()
            print(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    run_server()
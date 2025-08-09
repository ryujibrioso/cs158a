#!/usr/bin/env python
# coding: utf-8

# In[1]:


# secureget.py
import socket
import ssl

HOST = "www.google.com"
PORT = 443
OUTPUT_FILE = "response.html"

def main():
    # Create default SSL context
    context = ssl.create_default_context()

    # Create a TCP connection and wrap it with SSL
    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            print(f"Connected to {HOST} with SSL.")

            # Send HTTP GET request
            request = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
            ssock.sendall(request.encode("utf-8"))

            # Receive the response in chunks
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data

    # Decode HTTP response
    response_str = response.decode("utf-8", errors="replace")

    # Separate headers from body
    headers, html = response_str.split("\r\n\r\n", 1)

    # Save the HTML content to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Response saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


# In[ ]:





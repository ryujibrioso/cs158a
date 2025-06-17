\# Variable-Length Message TCP Client-Server

A Python implementation of TCP client and server that exchange messages with length prefixes (2-byte header).

\#\# Features  
\- Handles messages of arbitrary length (1-99 characters)  
\- Uses fixed 64-byte buffers for network operations  
\- Server echoes back messages in uppercase  
\- Properly handles message chunking and reassembly

\#\# Requirements  
\- Python 3.x

\#\# How to Run

Start the Server in a terminal

python server.py

Run the Client

In a separate terminal:

python client.py

nput Format

When prompted, enter messages in the format:

\[length\]\[message\]

Example: 10helloworld

\#\# Test Cases

Test 1: Short sentence with coder's  

![lijJO0H](https://github.com/user-attachments/assets/399b9544-6832-4f5b-a64e-f4fbdf23ee6f)

Test 2: long sentence with coder's  

![v1Rbexu](https://github.com/user-attachments/assets/23aa5acc-0d18-4aa3-bff7-2f04517476ac)

Test 3: Short sentence with reviewer's  

![pyUnMQy](https://github.com/user-attachments/assets/e69fd2ae-16f0-4715-850c-27f9749618f1)

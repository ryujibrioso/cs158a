A simple Python implementation of leader election in a ring network.

## How to Run

For a 3-node demo on your local machine:

1. Open **three separate terminal windows**

2. In each terminal, run one of these commands (order doesn't matter):

**Terminal 1** (Node 1):

python leader_election.py config.txt

repeat for 2 other terminals

## Output

Terminal 1:
C:\Users\ryuji\Desktop\Coding\cs158a\a3\config1>python leader_election.py config.txt
[2025-07-09 10:02:22] Server started on 127.0.0.1:5001
[2025-07-09 10:02:26] Connection attempt 1 failed, retrying...
[2025-07-09 10:02:30] Connection attempt 2 failed, retrying...
[2025-07-09 10:02:32] Connected to client at 127.0.0.1:5002
[2025-07-09 10:02:32] Sent: uuid=386d2458-04d6-43bb-9852-74300896776f, flag=0
[2025-07-09 10:02:51] Accepted connection from ('127.0.0.1', 53424)
[2025-07-09 10:02:51] Received: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0, greater, 0
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0
[2025-07-09 10:02:51] Received leader election: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1, leader is 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1
[2025-07-09 10:02:52] Terminating: leader is 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e
Exception in thread Thread-1:
Traceback (most recent call last):
  File "C:\Users\ryuji\AppData\Local\Programs\Python\Python39\lib\threading.py", line 980, in _bootstrap_inner
    self.run()
  File "C:\Users\ryuji\AppData\Local\Programs\Python\Python39\lib\threading.py", line 917, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\ryuji\Desktop\Coding\cs158a\a3\config1\leader_election.py", line 58, in accept_connection
    self.receive_messages()
  File "C:\Users\ryuji\Desktop\Coding\cs158a\a3\config1\leader_election.py", line 97, in receive_messages
    data = self.left_neighbor.recv(1024).decode('utf-8')
ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine

Terminal 2:
C:\Users\ryuji\Desktop\Coding\cs158a\a3\config2>python leader_election.py config.txt
[2025-07-09 10:02:32] Server started on 127.0.0.1:5002
[2025-07-09 10:02:32] Accepted connection from ('127.0.0.1', 53419)
[2025-07-09 10:02:32] Received: uuid=386d2458-04d6-43bb-9852-74300896776f, flag=0, greater, 0
[2025-07-09 10:02:36] Connection attempt 1 failed, retrying...
[2025-07-09 10:02:41] Connection attempt 2 failed, retrying...
[2025-07-09 10:02:45] Connection attempt 3 failed, retrying...
[2025-07-09 10:02:49] Connected to client at 127.0.0.1:5003
[2025-07-09 10:02:49] Sent: uuid=0037cfc9-4ed9-4b62-9ff3-658ce09cc257, flag=0
[2025-07-09 10:02:51] Received: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0, greater, 0
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0
[2025-07-09 10:02:51] Received leader election: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1, leader is 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1
[2025-07-09 10:02:51] Terminating: leader is 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e
Exception in thread Thread-1:
Traceback (most recent call last):
  File "C:\Users\ryuji\AppData\Local\Programs\Python\Python39\lib\threading.py", line 980, in _bootstrap_inner
    self.run()
  File "C:\Users\ryuji\AppData\Local\Programs\Python\Python39\lib\threading.py", line 917, in run
    self._target(*self._args, **self._kwargs)
  File "C:\Users\ryuji\Desktop\Coding\cs158a\a3\config2\leader_election.py", line 58, in accept_connection
    self.receive_messages()
  File "C:\Users\ryuji\Desktop\Coding\cs158a\a3\config2\leader_election.py", line 97, in receive_messages
    data = self.left_neighbor.recv(1024).decode('utf-8')
ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine

Terminal 3:
C:\Users\ryuji\Desktop\Coding\cs158a\a3\config3>python leader_election.py config.txt
[2025-07-09 10:02:49] Server started on 127.0.0.1:5003
[2025-07-09 10:02:49] Accepted connection from ('127.0.0.1', 53421)
[2025-07-09 10:02:49] Received: uuid=0037cfc9-4ed9-4b62-9ff3-658ce09cc257, flag=0, less, 0
[2025-07-09 10:02:49] Ignored message (smaller UUID): uuid=0037cfc9-4ed9-4b62-9ff3-658ce09cc257
[2025-07-09 10:02:51] Connected to client at 127.0.0.1:5001
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0
[2025-07-09 10:02:51] Received: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=0, same, 0
[2025-07-09 10:02:51] Leader is decided to 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e
[2025-07-09 10:02:51] Sent: uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1
[2025-07-09 10:02:51] Ignored message (leader already elected): uuid=5d14330a-0e4c-44ec-b700-6c6ee0af5b4e, flag=1
[2025-07-09 10:02:52] Terminating: leader is 5d14330a-0e4c-44ec-b700-6c6ee0af5b4e

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.29.95.14", 5000))
sock.send("hi".encode())

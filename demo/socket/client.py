import socket
import sys

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chost = socket.gethostname()
cport = 9999
c.connect((chost, cport))
cmsg = c.recv(1024)

c.close()
print(cmsg.decode('utf-8'))

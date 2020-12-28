import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
shost = socket.gethostname()
sport = 9999
s.bind((shost, sport))
s.listen(5)

while True:
    addr = s.accept()
    print(addr)
    msg='welcome'
    s.send(msg.encode('utf-8'))
    s.close()
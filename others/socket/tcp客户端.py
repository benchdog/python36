# import socket
# phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# phone.connect(('127.0.0.1',8000)) #建立连接
# phone.send('I AM CLIENT'.encode('utf-8')) #发送消息
# data=phone.recv(1024)
# print('收到服务端返回的信息',data)
#phone.close()



import socket
#from socket import *
ip_port=('127.0.0.1',8000)
buffer_size=1024
tcp_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_client.connect(ip_port)

while True:
    msg=input('客户端输入>>>:').strip()
    if not msg:continue
    tcp_client.send(msg.encode('utf-8'))
    print('客户端已经发送消息!')
    data=tcp_client.recv(buffer_size)
    print('来自服务端信息:',data.decode('utf-8'))

tcp_client.close()


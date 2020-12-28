# from socket import *
#
# ip_port=('127.0.0.1',8080)
# buffer_size=1024
# udp_server=socket(AF_INET,SOCK_DGRAM)
# udp_server.bind(ip_port)
#
# while True:
#
#     data=udp_server.recvfrom(buffer_size) #返回的是元组
#     print('来自客户端：',data)
#     # msg=input('服务端输入>>>:')
#     udp_server.sendto(data[0].upper(),data[1])




from socket import *
import time
ip_port=('127.0.0.1',8080)
buffer_size=1024
udp_server=socket(AF_INET,SOCK_DGRAM)
udp_server.bind(ip_port)

while True:
    fmt='%Y-%m-%d %X'
    data,addr=udp_server.recvfrom(buffer_size) #返回的是元组
    print('来自客户端：',data)
    server_time=time.strftime(fmt)
    udp_server.sendto(server_time.encode('utf-8'),addr)
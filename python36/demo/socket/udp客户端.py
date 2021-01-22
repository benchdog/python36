# from socket import *
# ip_port=('127.0.0.1',8080)
# buffer_size=1024
#
# udp_client=socket(AF_INET,SOCK_DGRAM)
# while True:
#     msg = input('客户端输入：>>>').strip()
#     udp_client.sendto(msg.encode('utf-8'),ip_port) #无面向连接，所以要指定IP_port
#     data=udp_client.recvfrom(buffer_size)
#     print('来自服务端：',data)




from socket import *
ip_port=('127.0.0.1',8080)
buffer_size=1024

udp_client=socket(AF_INET,SOCK_DGRAM)
while True:
    msg = input('客户端输入：>>>').strip()
    udp_client.sendto(msg.encode('utf-8'),ip_port) #无面向连接，所以要指定IP_port
    data,addr=udp_client.recvfrom(buffer_size)
    print('来自服务端的时间：',data)
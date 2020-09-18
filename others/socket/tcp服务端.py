# import socket
# phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# phone.bind(('127.0.0.1',8000))
# phone.listen(5)
# print("等待客户端发来消息:\n")
# conn,addr=phone.accept() #返回元组 #三次握手
# rec_msg=conn.recv(1024) #1024代表接收多少字节信息
# print('客户端IP和port：',addr) #客户端IP和port信息
# print('客户端发来的消息是：',rec_msg.upper())
# send_msg='I AM SERVER'
# conn.send(send_msg.encode('utf-8'))
# conn.close() #关闭连接 #四次挥手
# phone.close() #关闭socket #关闭此程序



import socket
#from socket import *

ip_port=('127.0.0.1',8000)
back_log=5
buffer_size=1024
tcp_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #socket.SOL_SOCKET,socket.SO_REUSEADDR,1
tcp_server.bind(ip_port)
tcp_server.listen(back_log)
print('服务端开始运行！')
while True:
    conn,addr=tcp_server.accept()
    print('双向连接：',conn)
    print('客户端地址：',addr)

    while True:
        try:
            data=conn.recv(buffer_size)
            print('来自客户端的消息：',data.decode('utf-8'))
            msg=input('服务端输入>>>：')
            if not msg:continue
            conn.send(msg.encode('utf-8'))
        except Exception:
            break
    conn.close()
tcp_server.close()


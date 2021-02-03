from socket import *
ip_port=('127.0.0.1',20000)
buffer_size=1024

ssh_client=socket(AF_INET,SOCK_STREAM)
ssh_client.connect(ip_port)

while True:
    cmd=input('客户端输入远程命令：>>>').strip()
    if not cmd:continue
    if cmd == 'quit' or 'q':break
    ssh_client.send(cmd.encode('utf-8'))
    cmd_res=ssh_client.recv(buffer_size)
    print('远程命令执行结果如下：\n',cmd_res.decode('gbk'))
ssh_client.close()
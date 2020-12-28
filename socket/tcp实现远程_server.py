from socket import *
import subprocess
ip_port=('127.0.0.1',20000)
back_log=5
buffer_size=1024

ssh_server=socket(AF_INET,SOCK_STREAM)
ssh_server.bind(ip_port)
ssh_server.listen(back_log)

while True:
    conn,addr=ssh_server.accept()
    print('新的客户端连接：',addr)
    while True:
        try:
            cmd=conn.recv(buffer_size)
            print('收到客户端的命令：',cmd.decode('gbk'))
            res=subprocess.Popen(cmd.decode('gbk'),shell=True,
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            err=res.stderr.read()
            if err:
                cmd_res=err
            else:
                cmd_res=res.stdout.read()

            conn.send(cmd_res)
        except Exception as e:
            print(e)
            break
    conn.close()
ssh_server.close()
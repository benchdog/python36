#cat /var/log/secure| awk -F'reset by' '{print $2}'| awk -F'port' '{print $1 $2}'| awk '{print $1}'|sed "/^$/d"| sort -n |uniq -c|sort -n
import socket
def get_ip_status(ip,port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.connect((ip,port))
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        #print('{0} port {1} is not open'.format(ip,port))
        pass
    finally:
        server.close()

if __name__ == '__main__':
    host = '27.1.18.12'
    for port in range(10,65535):
        get_ip_status(host,port)


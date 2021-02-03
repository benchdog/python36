import telnetlib
import threading

def get_ip_status(ip,port):
    server = telnetlib.Telnet()
    try:
        server.open(ip,port)
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        print('{0} port {1} is not open'.format(ip,port))
        pass
    finally:
        server.close()

if __name__ == '__main__':
    host = '114.116.151.226'
    # host = '124.207.149.130'
    threads = []
    for port in range(20,65535):
        t = threading.Thread(target=get_ip_status,args=(host,port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
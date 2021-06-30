import socket, random, threading

serverip='127.0.0.1'
queueip='127.0.0.1'
serverports=range(40000,40100)
queueport=42069

def manageconn():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        try:
            sock.bind((serverip,newport))
            sock.listen(0)
            sock.settimeout(15)
        except socket.timeout as e:
            print(e)
            portmgr.free(newport)
            sock.close()
        print(sock)
        conn,addr=sock.accept()
        with conn:
            conn.sendall(bytes(f'Connected to {serverip}:{newport}', 'UTF-8'))

class portmanager():
    def __init__(self, portlist:range):
        self.ports=[*portlist]

    def get(self):
        return self.ports.pop(random.randint(0,len(self.ports)-1))

    def free(self, port):
        self.ports.append(port)
        self.ports.sort()

    def test(self):
        None

portmgr=portmanager(serverports)
while True:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((queueip, queueport))
        s.listen(10)
        x,y=s.accept()
        with x:
            newport=portmgr.get()
            print(newport)
            x.sendall(bytes(str(f'{serverip}, {str(newport)}'), 'UTF-16'))
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
                try:
                    sock.bind((serverip,newport))
                    sock.listen(0)
                    sock.settimeout(15)
                except socket.timeout as e:
                    print(e)
                    portmgr.free(newport)
                    sock.close()
                print(sock)
                conn,addr=sock.accept()
                with conn:
                    conn.sendall(bytes(f'Connected to {serverip}:{newport}', 'UTF-8'))
import socket, random, threading

serverip='127.0.0.1'                    # ip of message server (to be implemented/do it yourself)
queueip='127.0.0.1'                     # ip of queue server (client connects to get server + port)
serverports=range(40000,40100)          # range of available server ports
queueport=42069                         # queue port for connections
threads=[]                              # active threads
messagelimit=50                         # messages to remember

def connmanager(serverip, newport):
    global commmgr, portmgr
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        try:
            sock.bind((serverip,newport))
            sock.listen(0)
            sock.settimeout(15)
        except socket.timeout as e:
            print(e)
            portmgr.free(newport)
            sock.close()
        conn,addr=sock.accept()
        with conn:
            conn.settimeout(None)
            conn.sendall(bytes(f'Connected to {serverip}:{newport}', 'UTF-8'))
            commmgr.add(newport,conn)
            while conn:
                try:
                    data=conn.recv(2048)
                    if data:commmgr.addtoqueue(f'msg [{addr[0]}:{addr[1]}]: {str(data,"UTF-8")}', str(addr))
                except (ConnectionResetError, ConnectionAbortedError):
                    print('Connection aborted (Disconnected by client)')
                    break
            commmgr.remove(newport)
            portmgr.free(newport)


class commmanager():
    def __init__(self):
        self.queue=[]
        self.conns={}
        self.queueempty=True

    def add(self, port, conn):
        self.conns[port]=conn

    def remove(self, port):
        self.conns.pop(port)

    def addtoqueue(self, item:str, origin:str):
        self.queue.append([item, origin])
        print(self.queue)
        nextitem:list=self.queue.pop(0)
        i=nextitem[0]
        if i.startswith('msg '):
            for conn in self.conns.keys():
                print(repr(str(i[4:])), self.conns[conn])
                self.sendmsg(str(i[4:]), self.conns[conn])
        elif i.startswith('cmd ') & nextitem[1]=='SERVER':
            pass

    def sendmsg(self, message, conn:socket.socket, *args):
        conn.sendall(bytes(message, 'UTF-8'))


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


commmgr=commmanager()
portmgr=portmanager(serverports) #init a port manager
while True:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((queueip, queueport))
        s.listen(10) #listen for connections on the queue server (port)
        x,y=s.accept()
        with x:
            newport=portmgr.get() #get a new port to connect to
            x.sendall(bytes(str(f'{serverip}, {str(newport)}'), 'UTF-8')) #send new ip and port to client
            newthread=threading.Thread(target=connmanager,args=(serverip, newport),name=f'{serverip}:{newport}') #start new thread to handle imminent client connection
            newthread.start() #start the thread
            threads.append(newthread)

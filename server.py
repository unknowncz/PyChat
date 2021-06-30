import socket, random, threading

print('Starting...')

sendserverip='127.0.0.1'                # ip of message server (to be sent to client)
actualserverip=''                       # ip of server to be bound
queueip=''                              # ip of queue server (client connects to get server + port)
serverports=range(40000,42068)          # range of available server ports
queueport=42069                         # queue port for connections
threads=[]                              # active threads

def connmanager(serverip, newport, sentserverip):
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
            conn.sendall(bytes(f'Connected to {sentserverip}:{newport}', 'UTF-8'))
            commmgr.add(newport,conn)
            commmgr.addtoqueue(f'msg {addr[0]}:{addr[1]} Connected', 'SERVER')
            while conn:
                try:
                    data=conn.recv(2048)
                    if data:commmgr.addtoqueue(f'msg [{addr[0]}:{addr[1]}]: {str(data,"UTF-8")}', str(addr))
                except (ConnectionResetError, ConnectionAbortedError):
                    commmgr.addtoqueue(f'msg {addr[0]}:{addr[1]} Disconnected', 'SERVER')
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
        nextitem:list=self.queue.pop(0)
        i=nextitem[0]
        if i.startswith('msg '):
            print(str(i[4:]))
            for conn in self.conns.keys():
                self.sendmsg(str(i[4:]), self.conns[conn])
        elif i.startswith('! ') and nextitem[1]=='SERVER':
            pass

    def sendmsg(self, message, conn:socket.socket, *args):
        try:conn.sendall(bytes(message, 'UTF-8'))
        except:pass


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
print(f'Server started on {sendserverip}.')
while True:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((queueip, queueport))
        s.listen(100) #listen for connections on the queue server (port)
        x,y=s.accept()
        with x:
            newport=portmgr.get() #get a new port to connect to
            x.sendall(bytes(str(f'{sendserverip}, {str(newport)}'), 'UTF-8')) #send new ip and port to client
            newthread=threading.Thread(target=connmanager,args=(actualserverip, newport, sendserverip),name=f'{sendserverip}:{newport}') #start new thread to handle imminent client connection
            newthread.start() #start the thread
            threads.append(newthread)

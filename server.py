import socket, random, threading

print('Starting...')

with open(f'{__file__}/../server.properties') as f:
    options={}
    lines=f.readlines()
    for i in lines:
        i=','.join(i.split(',')[:-1])
        option=i.split(':')
        if option[1].startswith("'"):parsed=option[1].strip("',")
        elif option[1].startswith("["):parsed=[]
        elif option[1].startswith('range('):
            nums=option[1].split('(')[1].split(')')[0].split(', ')
            parsed=range(int(nums[0]),int(nums[1]))
        elif len(option[1])>0:
            try:parsed=int(option[1])
            except:
                try:parsed=bool(option[1])
                except:pass
        options[option[0]]=parsed
    f.close()

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
portmgr=portmanager(options['serverports']) #init a port manager
print(f'Server started on {options["sendserverip"]}.')
while True:
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((options['queueip'], options['queueport']))
        s.listen(100) #listen for connections on the queue server (port)
        x,y=s.accept()
        with x:
            newport=portmgr.get() #get a new port to connect to
            x.sendall(bytes(str(f'{options["sendserverip"]}, {str(newport)}'), 'UTF-8')) #send new ip and port to client
            newthread=threading.Thread(target=connmanager,args=(options['actualserverip'], newport, options['sendserverip']),name=f'{options["sendserverip"]}:{newport}') #start new thread to handle imminent client connection
            newthread.start() #start the thread
            options['threads'].append(newthread)

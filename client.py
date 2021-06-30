import socket, time, threading

connip='127.0.0.1'#input('Connect to: ')
connport=42069#int(input('On port: '))

def recv(socke:socket.socket):
    while True:
        try:print(str(socke.recv(2048), 'UTF-8'))
        except (ConnectionResetError, ConnectionAbortedError):
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((connip, connport))
    time.sleep(0.2)
    newconn=s.recv(256).decode('UTF-8').split(', ')
    time.sleep(0.2)
    s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((str(newconn[0]), int(newconn[1])))
        print(sock.recv(256).decode('UTF-8'))
        pname, pport=sock.getpeername()
        threading.Thread(target=recv, args=(sock,)).start()
        while sock:
            try:
                msg=f'{input()}'
                sock.sendall(bytes(msg, 'UTF-8'))
            except (ConnectionResetError, ConnectionAbortedError):
                print('Connection aborted by server')
                break


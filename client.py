import socket, time

connip='127.0.0.1'#input('Connect to: ')
connport=42069#int(input('On port: '))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((connip, connport))
    time.sleep(0.2)
    newconn=s.recv(256).decode('UTF-16').split(', ')
    time.sleep(0.2)
    s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((str(newconn[0]), int(newconn[1])))
        print(sock.recv(256).decode('UTF-8'))
        input()

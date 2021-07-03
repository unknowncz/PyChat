import socket, time, threading, sys, subprocess
def tryimport():import getkey
try: import msvcrt
except:
    try: tryimport()
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'getkey'])
        try:tryimport()
        except:
            print('Module getkey failed to import.')
            exit()

with open(f'{__file__}/../client.properties') as f:
    options={}
    lines=f.readlines()
    for i in lines:
        i=','.join(i.split(',')[:-1])
        option=i.split('=')
        print(i, option)
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

flushing=False
msg=''

def getinput():
    global newmessage
    sys.stdout.write('> ')
    sys.stdout.flush()
    input = ''
    if msvcrt:
        while True:
            if msvcrt.kbhit():
                byte_arr = msvcrt.getch()
                if ord(byte_arr) == 13: # enter_key
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    return input
                elif ord(byte_arr) >= 32: #space_char
                    input += "".join(map(chr,byte_arr))
                    sys.stdout.write(byte_arr.decode())
                    sys.stdout.flush()
                elif ord(byte_arr) == 8:
                    input = input[:-1]
                    sys.stdout.write(f'{byte_arr.decode()} {byte_arr.decode()}')
                    sys.stdout.flush()
            if newmessage:
                sys.stdout.write('\b \b'*(len(input)+2))
                print(str(newmessage, 'UTF-8'))
                newmessage=''
                sys.stdout.write(f'> {input}')
                sys.stdout.flush()
    else:
        while True:
            char = getkey.getkey(blocking=False)
            if char == getkey.keys.ENTER:
                sys.stdout.write('\n')
                sys.stdout.flush()
                return input
            elif char == getkey.keys.BACKSPACE:
                input = input[:-1]
                sys.stdout.write(f'{char} {char}')
                sys.stdout.flush()
                char=''
            elif char == getkey.keys.SPACE:
                input += ' '
                char=''
            elif char!='':
                input+=char
                sys.stdout.write(char)
                char=''
            if newmessage:
                sys.stdout.write('\b \b'*(len(input)+2))
                print(str(newmessage, 'UTF-8'))
                newmessage=''
                sys.stdout.write(f'> {input}')
                sys.stdout.flush()

def sendmsg(socke:socket.socket, *args):
    while socke:
        try:
            msg=getinput()
            socke.send(bytes(msg, 'UTF-8'))
        except (ConnectionAbortedError, ConnectionResetError):break
        except Exception as e:
            print(e)
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((options['connip'], options['connport']))
    time.sleep(0.2)
    newconn=s.recv(256).decode('UTF-8').split(', ')
    time.sleep(0.2)
    s.close()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if options['alternateconnect']:
            sock.connect((options['alternateip'], int(newconn[1])))
        else:
            sock.connect((str(newconn[0]), int(newconn[1])))
        print(sock.recv(256).decode('UTF-8'))
        sendthread=threading.Thread(target=sendmsg, args=(sock,)).start()
        while True:
            try:
                newmessage:bytes=sock.recv(2048)
            except (ConnectionResetError, ConnectionAbortedError):
                break

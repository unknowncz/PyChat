PyChat
=====

This is a simple ip-based chat app, meant to be used internally.

Editable variables:
------
------
### Server.py ###
serverip - str - IP of server, which will handle messages (if actualserverip is set this ip will only be passed to the client)

queueip - str - IP of queue server, which the client will first connect to

actualserverip - if set, will be bound as the listening socket for the assigned client

serverports - int - Range of ports, which will be assigned to the client

queueport - int - Port of queue server, which the client will first connect to

threads - list - Leave empty

-----
### Client.py ###
connip - str - IP of queue server

connport - int - Port of queue server

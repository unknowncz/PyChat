PyChat
=====

This is a simple ip-based chat app, meant to be used internally.

Editable variables:
------
------
### Server.py ###
serverip - str - IP of server, which will handle messages

queueip - str - IP of queue server, which the client will first connect to

serverports - int - Range of ports, which will be assigned to the client

queueport - int - Port of queue server, which the client will first connect to

-----
### Client.py ###
connip - str - IP of queue server

connport - int - Port of queue server

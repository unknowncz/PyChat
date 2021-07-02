PyChat
=====

This is a simple ip-based chat app, meant to be used internally and / or with friends

Editable variables:
------
------
### Server.properties ###
serverip - str - IP of server, which will handle messages (if actualserverip is set this ip will be only passed to the client)

queueip - str - IP of queue server, which the client will first connect to

actualserverip - if set, will be bound as the listening socket for the assigned client

serverports - int - Range of ports, which will be assigned to the client

queueport - int - Port of queue server, which the client will first connect to

threads - list - Leave empty

-----
### Client.properties ###
connip - str - IP of queue server

connport - int - Port of queue server

alternateconnect - bool - Used for local connections when hosting on external ip

alternateip - str - Ip used for internal connections (usually localhost)


Share your external IP with only trusted people, seriously, I am not responsible for any damage that occurs as a result of this action.
-----

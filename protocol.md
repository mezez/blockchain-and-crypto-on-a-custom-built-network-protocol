# PROTOCOL DOCUMENT  
This is the protocol documentation for a cryptocurrency blockchain based on a peer to peer network  

This Network consists of a tracker which simply keeps track of peers connected on the cheesechain network


NOTE: ALL SAMPLE CODES ARE WRITTEN IN PYTHON
* A TRACKER runs constantly on localhost (at the time of writing)
* PEERS can connect to the tracker on port 9999  


#-CONNECT TO TRACKER
This demonstrates sample code in python for connecting to the tracker by a peer
* Connection Request: 
* TRACKER_HOST = 'localhost'
* TRACKER_PORT = 9999
* s = socket.create_connection((TRACKER_HOST, TRACKER_PORT))  


* Connection Response: 
* type = byte string
* response string = Connection Successful

#-REQUEST TO JOIN CHAIN
This demonstrates protocol/sample code in python for requesting to join a cheesechain to the tracker by a peer. Returns peer_id of the peer
* PEER_HOST = 'localhost' - This is needed for other peers to connect to this peer
* PEER_PORT = 9009 - This is need for other peers to connect to this peer

* request_message: JOIN_CHAIN:PEER_HOST:PEER_PORT
* type = byte string
* JOIN_CHAIN is the request command
* PEER_HOST is the connecting peer host
* PEER_PORT is the connecting peer port
* s.send(request_message.encode()) where is the socket created during connection  


* Response: 
* type = byte string
* response string = PIDxxxxxxxxxxxxxxxxx

#-REQUEST LIST OF PEERS IN THE CHAIN
This demonstrates protocol/sample code in python for requesting list of peers in a cheesechain to the tracker by a peer. Returns peer_id of the peer

* request_message: GET_PEERS:PEER_ID
* GET_PEERS is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte string
* response string = CPSS[{"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, ...]

#-CONNECT TO PEER
This demonstrates sample code in python for connecting to the a peer by another peer
* Connection Request: 
* s = socket.create_connection((PEER_HOST, PEER_PORT))  


* Connection Response: 
* type = byte string
* response string = Connection to peer [PEER_ID]


#-INFORM PEERS OF NEW CHEESE
#-SHARE CHEESE TO PEER(S)  


#-GET CHEESES FROM PEER(S)
This demonstrates protocol/sample code in python for requesting cheeses by a peer from another peer. Returns peer_id of the peer

* request_message: GET_CHAIN:PEER_ID
* GET_PEERS is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte string
* response string = CHAIN[{"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0}, ...]  


#-GET OPEN TRANSACTIONS FROM PEER(S)
This demonstrates protocol/sample code in python for requesting open transactions by a peer from another peer. Returns peer_id of the peer

* request_message: GET_OPEN_TRANSACTIONS:PEER_ID
* GET_OPEN_TRANSACTIONS is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte string
* response string = TR[{"sender": "sender public key", "recipient": "recipient public key", "amount": XXX}, ...]  


# CHECK IF PEER IS STILL CONNECTED TO TRACKER

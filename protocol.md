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

* request_message: PCONNECT:PEER_HOST:PEER_PORT
* type = byte string
* PCONNECT is the request command
* PEER_HOST is the connecting peer host
* PEER_PORT is the connecting peer port
* s.send(request_message.encode()) where s is the socket created during connection  


* Response: 
* type = byte string
* response string = TCONNECTACK:PEER_ID
* PEER_ID is created by tracker for identifying the peer subsequently

#-REQUEST LIST OF PEERS IN THE CHAIN
This demonstrates protocol/sample code in python for requesting list of peers in a cheesechain to the tracker by a peer.

* request_message: GETPEERS:PEER_ID
* GETPEERS is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = GETPEERSACK[{"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X", "socket":" SOCKET OBJECT"}, ...]

#-CONNECT TO PEER
This demonstrates sample code in python for connecting to a peer by another peer.
* Connection Request: 
* s = socket.create_connection((PEER_HOST, PEER_PORT))  


* Connection Response: 
* type = byte string
* response string = PCONNECTACK:PEER_ID
* PEER_ID is the peer id of the remote peer connected to 


#-INFORM PEERS OF NEW CHEESE  
This demonstrates protocol/sample code in python for broadcasting cheesechain with new cheese by a peer to other peer(s).

* request_message: BRCHEESE[{"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0}, ...]
* BRCHEESE is the request command
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = HCKACK
* BRCHEESE is the confirmation of reception of broadcast by peer(s)
* s.send(response.encode()) where s is the socket created during connection  


#-INFORM PEERS OF NEW OPEN TRANSACTION  
This demonstrates protocol/sample code in python for broadcasting newly added transaction by a peer to other peer(s).

* request_message: BRTRANSACTION{"sender": "sender public key", "recipient": "recipient public key", "amount": XXX}
* BRTRANSACTION is the request command
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = BRTRANSACTIONACK
* BRTRANSACTIONACK is the confirmation of reception of broadcast by peer(s)
* s.send(response.encode()) where s is the socket created during connection


#-GET CHEESES FROM PEER(S)
This demonstrates protocol/sample code in python for requesting cheeses by a peer from another peer.

* request_message: GETCHAIN:PEER_ID
* GETCHAIN is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = GETCHAINACK[{"sequence_number": 0, "parent_smell": "", "transactions": [], "nonce": 100, "timestamp": 0}, ...]  


#-GET OPEN TRANSACTIONS FROM PEER(S)
This demonstrates protocol/sample code in python for requesting open transactions by a peer from another peer.

* request_message: GETOPENTRANSACTIONS:PEER_ID
* GETOPENTRANSACTIONS is the request command
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = GETOPENTRANSACTIONSACK[{"sender": "sender public key", "recipient": "recipient public key", "amount": XXX}, ...]  


# CHECK IF PEER IS STILL CONNECTED TO TRACKER
This demonstrates protocol/sample code in python for confirming if peer is still connected by tracker.

* request_message: HCK
* HCK is the request command
* s.send(request_message.encode()) where s is the socket created during connection
* 
* Response: 
* type = byte string
* response string = HCKACK
* HCKACK is the confirmation of active connection from peer to tracker
* s.send(response.encode()) where s is the socket created during connection
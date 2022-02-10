# PROTOCOL DOCUMENT

NOTE: ALL SAMPLE CODES ARE WRITTEN IN PYTHON
* A TRACKER runs constantly on localhost (at the time of writing)
* PEERS can connect to the tracker on port 9999
* 
#-CONNECT TO TRACKER
This demonstrates sample code in python for connecting to the tracker by a peer
* Connection Request: 
* TRACKER_HOST = 'localhost'
* TRACKER_PORT = 9999
* s = socket.create_connection((TRACKER_HOST, TRACKER_PORT)) 
* 
* Connection Response: 
* type = byte string
* response string = Connection Successful

#-REQUEST TO JOIN CHAIN
This demonstrates sample code in python for requesting to join a cheesechain to the tracker by a peer. Returns peer_id of the peer
* PEER_HOST = 'localhost' - This is needed for other peers to connect to this peer
* PEER_PORT = 9009 - This is need for other peers to connect to this peer

* request_message: JOIN_CHAIN:PEER_HOST:PEER_PORT
* type = byte string
* JOIN_CHAIN is the request action
* PEER_HOST is the connecting peer host
* PEER_PORT is the connecting peer port
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte string
* response string = PIDxxxxxxxxxxxxxxxxx

#-REQUEST LIST OF PEERS IN THE CHAIN
This demonstrates sample code in python for requesting list of peers in a cheesechain to the tracker by a peer. Returns peer_id of the peer

* request_message: GET_PEERS:PEER_ID
* GET_PEERS is the request action
* PEER_ID is the ID of requesting peer
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte string
* response string = CPSS[{"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X"}, {"peer_id":"PIDbbbbb", "host":"0.9.X.X","port":"0.9.X.X"}, ...]

#-CONNECT TO PEER
#-INFORM PEERS OF NEW CHEESE
#-SHARE CHEESE TO PEER(S)
#-GET CHEESE FROM PEER(S)

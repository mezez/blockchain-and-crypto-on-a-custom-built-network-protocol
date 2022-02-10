# PROTOCOL DOCUMENT

NOTE: ALL SAMPLE CODES ARE WRITTEN IN PYTHON
* A TRACKER runs constantly on localhost (at the time of writing)
* PEERS can connect to the tracker on port 9999
* 
#-CONNECT TO TRACKER
This demonstrates sample code in python for connecting to the tracker by a peer
* Connection Request: 
* TRACKER_URL = 'localhost'
* TRACKER_PORT = 9999
* s = socket.create_connection((TRACKER_URL, TRACKER_PORT)) 
* 
* Connection Response: 
* type = byte
* response string = Connection Successful

#-REQUEST TO JOIN CHAIN
This demonstrates sample code in python for requesting to join a cheesechain to the tracker by a peer. Returns peer_id of the peer

* request_message: JOIN_CHAIN
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte
* response string = PIDxxxxxxxxxxxxxxxxxx

#-REQUEST LIST OF PEERS IN THE CHAIN
This demonstrates sample code in python for requesting list of peers in a cheesechain to the tracker by a peer. Returns peer_id of the peer

* request_message: GET_PEERS
* s.send(request_message.encode()) where is the socket created during connection
* 
* Response: 
* type = byte
* response string = CPSS["PIDbbbbb", "PIDbbbbf", "PIDbbbby", ...]

#-CONNECT TO PEER
#-INFORM PEERS OF NEW CHEESE
#-SHARE CHEESE TO PEER(S)
#-GET CHEESE FROM PEER(S)

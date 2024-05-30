# 2022-net-i

## Subject description:

The idea of this project is to implement a blockchain peer to peer system inspired by Bitcoin, essentially, a cryptocurrency, cheesecoins running on a cheesechain (blockchain). Additionally, the interconnection between the peers in the system was to be done via a custom designed and built network protocol. The system comprises a tracker which keeps information of peers currently connected to the network and peer which keeps a copy of a cheesechain as well as performs a transaction, mines a cheese and interacts with other peers in the network.

Our peer to peer system should work either as multiple instances on the same device or on different computers on a network. These peers should be able to communicate with each other and exchange information between each other without central server.

## How to run:

*Libraries installation:*

To run the project you must have python version 3.9.*. Inside a terminal, you need to run these commands in this order to setup all required libraries:

1. python -m venv venv to create a virtual environment (if not already automatically created by using environments such as pycharm)
2. venv\Scripts\activate
3. pip install -r requirements.txt  
(Steps 1 and 2 above can be skipped if already handled by your IDE or dev environment. The ultimate goal is to be able to install the requirements in the requirements.txt file)

*Running the project:*

To run the project in beginning you must set TRACKER_URL variable at the top of the cheese_network/cheese_protocol.py file to your IP address. For running all tests on a single computer, this can be set to "localhost".  

For different computers over a network e.g. on a mobile hotspot:

1. Connect your tracker computer as well as the peers computers to the applicable hotspot
2. Go to your hotspot settings to find the allocated IP address of the tracker computer
3. Set the IP address as the value for the TRACKER_URL.

After this step you can start to run the tracker and peers. *Important* (tracker must be started before peers). Also,  Inside of terminal write these commands:

1. python tracker.py (or just press run button) This will start a tracker.
2. python node.py -p [PORT_NUMBER] (python node.py -p 5000. skipping the -p tag will default to a port number of 5005. Different nodes should have different port numbers as this is used to identify their various wallets and copy of cheesechain). This command will start a peer server. A peer server enables us to use subsequently spin up a peer from the GUI which will connect to and interact with the tracker and other peers in our custom peer to peer network.

Repeat the second step as many times as you wish to increase number of peers which will be connected to the network. *Important* (Always set unique port numbers when spinning up a new peer server).

*Usage of system:*

After spinning up running a peer you will see a text in terminal "Running on [IP Address and Port of peer server]". Click on your this URL  while holding ctrl button. It will open browser where you can see the UI instance for that peer node. Alternatively, you can just manually copy and paste this in the browser to startup the GUI.

If you are running this peer for the first time you need to press "Create new Wallet" which will generate your own wallet with your public and private keys. So you will be able to start mining your cheeses or send and receive coins to other peers. The wallet file can be found at chain_database/wallets folder. You can always clear this data, alongside that in chain_database/cheese_chains to start afresh.

If you already have a wallet you need to press "Load Wallet" button. After that your wallet will be loaded.

When you have your wallet ready you need to load the cheesechain by pressing "Load Cheesechain" button. Afterwards, you can mine cheeses by pressing "Mine Coins" button. Or transfer your cheeses to other people by providing other persons public key in "Recipient key" field and providing the amount of cheeses you want to transfer. It will create open transaction which you can be seen in "Open Transactions" tab and pressing "Load Transactions" button. For transaction to be fulfilled, it must be mined.  

NOTE: 
* AFTER OTHER PEERS ARE CONNECTED ON THE NETWORK, YOU MAY NEED TO (MANUALLY) DISCONNECT AND RECONNECT THE FIRST PEER ON THE NETWORK, ESPECIALLY IF UPDATING CHEESECHAIN OR OPEN TRANSACTIONS FROM OTHER PEERS DOES NOT WORK.
* LOADING CHEESECHAIN OR OPEN TRANSACTIONS MAY TAKE LONG SOMETIMES, DEPENDING ON NETWORK SPEED, COMPUTING TIME FOR PROOF OF WORK AND VERIFICATIONS. YOU CAN MONITOR THE STATUS OF SUCH REQUESTS ON THE NETWORK TAB OF YOUR DEVELOPER TOOLS

## Architecture description:

For the project we used the MVC architecture M(model), V(view), C(controller).

* M - cheesechain.py (model of cheesechain), wallet.py (model of users wallet) transactions.py (model of transactions).
* V - ui/node.html (user interface, UI, of our system).
* C - node.py (peer server which is powered by python flask, for receiving requests from the UI as well as sending responses and updates).

Data storage:
* Cheesechain is stored as json string.
* Wallet is stored as string.

System's UI interacts with the peer flask server via HTTP Protocol.
For communication and interaction between peers and between peer and tracker we created our own custom protocol. Everything about this can be found in the cheese_network module folder. This contains the following files: cheese_protocol.py, my_helpers.py, tracker.py and peer.py

cheese_protocol.py class is responsible for request and response actions and request validation to ensure that peer is part of network to protect the network from invalid external connection.
my_helpers.py class is used for handling task that are auxiliary to the core functions of the network protocol, such as getting part of the connected peers, open transactions, etc.
tracker.py is the implementation of the tracker
peer.py class is the implementation of the peer.

At the beginning, we need to start the tracker which tracks all peers connected to network. The tracker spins up a new thread for handling interaction with each of it's connected peers when necessary.

With the tracker running, we can start peers which creates wallet and sends connection request to tracker. Tracker responds to connection. Upon successful connection to the tracker, the peer spins creates a socket to listen to connections from other peers. It then sends requests to join the network to the tracker, alongside it's socket information for listening to requests. The tracker acknowledges this, assigns an id to this peer and saves all these info. Afterwards, the peer can ask the tracker for information on other connected peers. If there are no more than 10 connected peers in the network tracker returns all peers connected to system, otherwise, if there are more than 10 peers connected to network it returns subset of 10 random peers in a list. When a peer gets a list of connected peers, it can connect to these peers to request and exchange resources. As mentioned earlier, it also listens for connections from peers and their interactions are handled concurrently via multithreading.

When peer is connected to other peers, it can request or share cheesechain, open transactions or new cheese:

* When a peer requests for cheesechain from other peers, to ensure that it takes the right cheesechain, it tries to validate all the chains received and always keeps the longest chain that is valid.
* For loading open transactions,to ensure that the peer keeps an accurate list of valid transactions, it validates if sender/receiver are valid peers (or if the sender is the cheesechain reward system, in the case of a successful mine), if transaction doesn't already exist in list of transactions to avoid creating duplicates and if transaction was not already mined.
* Note: To ensure synchronisation, peers continuously request list of connected peers from tracker when they want to get these updated information in other to resolve issues such as the first peer on the network having no peers to interact with, etc.

After mining is complete or transactions are created, a broadcast is made to other connected peers to ensure that they have the newest information of cheesechain or transactions depending on our action. It is important to note however that the User interface is not reactive to these changes and the applicable buttons need to be clicked to reflect these changes made by other peers  

## EXTRAS:  

* Unit tests were written for testing different functional units of the system necessary for proper functioning of the project such as hashing and other helper functions, etc
* These tests are found under the custom_tests folder
* FOR THE CHEESE_NETWORK_TESTS TO RUN COMPLETELY, YOU NEED TO HAVE THE TRACKER RUNNING
* To run the tests files, it is best to use environments such as pycharm and run the file (using the IDE run button). This will help prevent python loadmodule errors when running from command line

## References:

* The building blocks of the blockchain(cheesechain) of this project was from the tutorial found at https://www.youtube.com/watch?v=KARxDX5DTgY.
* This was subsequently built upon/modified and adapted to suit the requirements of this project

# 2022-net-i

## Subject description:

Our task was to create peer-to-peer blockchain(chesechain) system inspired by Bitcoin. The system is containing tracker which is tracking all the peers currently connected to the system and peer which allows users to conect to cheesechain.
Our system must work on different computers and allow them to communicate with each other and exchange information between each other without central server.

## How to run:

**Libraries instalation:**

To run the project you must have python version 3.9.7. Inside of a terminal you need to run these commands in this order to setup all required libraries:

1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt

**Runing the project:**

To run the project in beginning you must set TRACKER_URL inside of cheese_protocol.py file to your IP address. After this step you can start to run the tracker and peers. **Important** (tracker must be started before peers). Inside of terminal write these commands:

1. python tracker.py (or just press run button) This will start a tracker.
2. python node.py -p 5000 (5000 is a port in which you are planning to run your peer) this will start a peer.

Repeat second steps to increase number of peers which are connected to the network. **Important** (If peers are ran on the same IP, do not forget to change port number for each peer and open independant terminal for each peer).

**Usage of system:**

After runing a peer you will see a text in terminal "Running on [Your IP address]" click on your IP address while holding ctrl button. It will open browser where you can see our UI. or just write your IP address and port number in your browser.

If you are running this peer for the first time you need to press "Create new Wallet" which will generate your own wallet with your public and private keys. So you will be able to start mining your cheeses or transfer your own cheeses to other users.

If you already have a wallet you need to press "Load Wallet" button. After that your wallet will be loaded.

When you have your wallet ready you need to load the cheesechain by pressing "Load Cheesechain" button. Afterwards you can mine cheeses by pressing "Mine Coins" button. Or transfer your cheeses to other people by providing other persons public key in "Recipient key" field and providing the ammount of cheeses you want to transfer. It will create open transation which you can be seen in "Open Transactions" tab and pressing "Load Transactions" button. For transaction to be fullfilled it must be mined.

## Architecture description:

For project we are using MVC architecture M(model), V(view), C(controller).

* M - cheesechain.py (model of cheesechain), wallet.py(model of users wallet) transactions.py (model of transactions).
* V - node.html UI of our system.
* C -  node.py (peer) which is powered by python flask.

Data storage:
* Cheese chain is storred as json string.
* Wallet is stored as string.

cheese_protocol.py class is responsible for request and response actions and request validation to ensure that peer is part of network to protect from external connection.

System's UI with peer is contacting thrue http protocol.
For cummunication between Peers and between peer and tracker we created our own custom protocol.

At the beggining we need to start our tracker which is tracking all peers connected to network. Tracker is creating a new thread for each peer connected to ensure flawless connection.

After tracker is running we can start peers which creates wallet and sends connection request to tracker. Tracked respond to connection. Afterwards peer is asking tracker for other connected peers. If there are no more then 10 connected peers in the network tracker is returning all peers connected to system. If tracker has more then 10 peers connected to network it returns subset of 10 random peers in a list. When peer got a list of connected peers it create a new thread for each peer.

When peer is connected to other peers it can chooses to load a cheesechain or load transactions:

* If we want to load a cheeschain. We are asking again for all connected peers just in case if in the beggining there was no other connected peers and someone joined afterwards that we will include them. To ensure that we are taking a correct cheesechain we start from the longest chain and validat each cheese in the chain if they are valid. The longest chain with all valid cheeses is set as current cheesechain.
* If we want to load transactions. We are asking again for all connected peers just in case if in the beggining there was no other connected peers and someone joined afterwards that we will include them. To ensure that we are taking a correct transactions we need to validate if sender is one of the peers, if transaction doesn't already exist in our transactions to do not create duplicates and if transaction was not already mined to do not open a transaction which was already mined.

After we mine a cheese or open a transaction we are broadcasting this information to all of our connected peers to ensure that they have the newest information of cheesechain or transactions depending of our action.
**Our initial objectives**

Our goal was to implement a blockchain peer to peer system inspired by Bitcoin, essentially, a cryptocurrency, cheesecoins running on a cheesechain (blockchain). Additionally, the interconnection between the peers in the system was to be done via a custom designed and built network protocol.

**What works:**

- Tracker:

* Maintains an updated list of all peers
* Uses a multithreading approach to listen to and interact with each connected peer in the network
* It provides a list of other peers to a peer which demand a peer to connect to

- Peer:

* Can be instantiated from a call to a web server, triggered by a GUI on the browser
* Can function effectively whether as multiple instances on the same computer or as instances on different computers alongside the tracker on a network
* Starts by reloading saved cheeses from a file on disk, or instantiating a raclette cheese, where it has no currently saved data
* Stores a copy of the cheesechain
* Keeps the longest valid cheesechain
* Can do mining
* Synchronising a cheese chain with others peers
* Exchanges information with other peers (e.g. cheesechain, new cheese, list of open transactions)
* Can perform transactions(send and receive cheesecoins to and from other peer using a public key)
* Uses a multithreading approach to interact with it's connected peers

- Cheesechain:

* Is a thoroughly validated shared database
* The sequence number of each cheese is correct
* Tampering of any sort with the information on a valid cheesechain invalidates it

- GUI:

* Web interface for running and managing a peer
* Helps for easy visualisation of processing
* Can create/load existing wallet, load (update) cheesechain and open transactions, create transaction, trigger a mining process

**What doesn't work compared to our objectives:**

- Some high level exceptions occur in the network communication process which we had not the time to properly handle
- There is a likelihood that the first peer connected on the network may need to disconnect and reconnect again after other peers may have joined to be able to properly share resources

**Parts and time spent by each member:**

Team leader: Chimezirim Victor EKEMAM

| Group members name(Developers) | Time Spent (Hours) | Parts |

| Chimezirim Victor EKEMAM | | Cheesechain Design and Implementation/GUI, Network Protocol/Tracker & Peer, Integration Testing |
| Ignas BARAKAUSKAS | | Cheesechain Debugging and Modifications, Integration Testing, Documentation (Readme.md)|
| Soumya KUMBAR | | Cheesechain Debugging and Modification Unit Testing implementation, Integration Testing |
| Sara Assefa ALEMAYEHU | | Cheesechain Debugging and Modification, Documentation (Auto Evaluation,Retrospective), Integration Testing |

**Good Development Practices we followed and an evaluation**

We followed a product roadmap which is initialised in very beginning of our project with milestones for each week to fulfil. We implemented and tested all the features we defined above according to the project description and our objectives. We tried to stick to an MVC architecture and an object-oriented approach to building our system. This enabled us make for code readability, separation of concerns, code reusability etc. We also maintained a dev branch for keeping our most stable code version for testing before merging to main. Other local tasks by team members where done on different branches before being merged to dev

**Week 1 and 2 (January 21-27):**

- Initial Discussions, Idea sharing and Validation
  We had meetings during this week to discuss and understand the project clearly. Everyone got the proper understanding about what is going to be implemented in upcoming weeks and what will be our product finally.

* conduct a proper retrospective for this sprint.

**Week 3 (January 28- February 4):**

- System and protocol design
  We did our first draft design of system architecture and protocol. We had meetings with our meta-group members(3 different groups). Different groups came up with their protocol design. We discussed and tried to reconcile the differences in the protocols (mostly a case of differences in nomenclature and presentation at the time). We finalised the detailed design of the system, to submit the protocol.md file on 15/02/2022.

* conduct a proper retrospective for this sprint.

**Week 4 and 5 (February 5 – February 19):**

- Implementation phase
  Group members individual or collaboratively tried to progressively implement the different modules of the project. We started with the cheesechain part, then to the protocol and back to the cheesechain. This was followed by implementation of unit tests and integration testing. In this implementation phase we tried to follow a good working practice e.g:

* Committing/provide good commit messages especially in cases where we did pair-programming
* Indentation based on PEP8 formatting
* Tried to form consistent abstractions
* Tried to encapsulate implementation details
* Tried to keep our code clean
* Commenting
* Error handling
* conduct a proper retrospective for this sprint

**Week 6 (February 20- February 27):**

- Testing  
  We did testing together and noticed some necessary modifications and improvements needed and tried to implement them

* Perform various tests and code reviews e.g:
  - We had a stress tests
  - Implementation and running of unit test suites
* conduct a retrospective for this sprint.

**Week 7 (February 28- March 7):**

- Testing and Documentation
  We performed testing in this week also and did some modifications. Complete documentation.

* conduct final retrospective for this sprint

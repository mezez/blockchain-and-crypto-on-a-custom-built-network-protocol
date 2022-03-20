**RETROSPECTIVE**

**Difficulties faced**

- Design and implementation of the network (protocol) was quite challenging since this was our first ever attempt at such
- There were some exceptions that proved a little difficult to handle in the network part of the project
- In testing, different computing capabilities of our various computers posed a challenge in terms chain validation, proof of work etc., especially as the chain become longer. This sometimes led to issues like connection timeouts when a node is waiting to receive a resource from a slow node. This led to instances where a reconnection has to be made and resource requested afresh
- Managing complexity got more and more difficult as project grew
- We faced problems with syncronization of data, especially in open transactions majorly because of varied number of other connected peers available to each peer. (Initially the number of connected peers available to the first peer in a network will always be 0. The last peer to connect to the network will usually have the highest number of connected peers, in a network of 10 peers or less)
-

**Lessons learned**

- Taking more time to clearly understand the requirements before trying to implement will ultimately save more time and prevent repetition of efforts later
- Checking the work done in the domain give good insight about the project
- Making a good commit and comments help to back trace what was done by whom, always keep the work process clean and understandable
- Testing a lot, as a group as much as possible is very useful. This was a bit difficult considering the volume of work we had from other projects, but still a useful takeway
- Acquired skills in TCP sockets(socket Programming), P2P system and the workings and implementation of a blockchain system. These are skills we had little to no knowldge on, prior to this project
- Working with external team can be quite challenging sometimes
- Asking for help other team members more will make the work easier and save time since we all may not have the same understanding in everything
- Keeping track of the project progress is difficult without a use of proper project management tool

**What we would keep next time**

- We would keep team collaboration and spirit
- We would keep the same project roadmap and planning
- Implement basic parts and build upon it over time
- Modular architectures with focus on seperation of concerns
- Constant meeting to get update made by each member on the progress of the project and to stay motivated
- Use GitHub or similar tools for version control and project collaboration
- Sharing ideas between group members during implementing and validating
- We will keep good development practices e.g: MVC Architecture, Object Oriented Programming Concepts commenting, following conventions and perform testing having a different behaviors

**What we would do differently**

- Better planning and management, and also stick with the plan in order to meet the objectivss
- Give more time for architecture and design
- Check what is done and what needs to be added in existing solutions for ideas
- Get ideas fron experienced persons in the domain
- Documentation draft is better done alongside implementation of project
- Use of project management tools for efficient tracking of progress on the project

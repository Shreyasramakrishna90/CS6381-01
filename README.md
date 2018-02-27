Distributed System Principles: Assignment1
We have three codes in this assignment. One each for publisher, broker and subcriber.

***Publisher:*** 
For simplicity we consider having three publishers attached to ports 5600, 5601 and 5602. Similarly each of the publisher can publish under any one of the topics 1, 2, 3 or 4. The user has the freedom to start any of the three publishers and also the topics under which they have to publish.

***Working of publisher:***
After taking the user input, the publisher registers itself to the broker through the register_pub() function. So, this function basically creates a request-reply communication pattern between the publisher and the broker. The publisher queries if the broker is ready for the communication and when it receives a response, it starts sending the publisher details which are registered in the broker and will be later sent to the subscriber.

After the publisher information is registered with the broker, the publisher starts running itself in a thread waiting for a subscriber to connect.

***Broker***
The Broker plays a vital role in handling all the bookkeeping data of the publisher and the subscriber. It recives the publisher information and stores it, till it has to relay this information to a request made by the subscriber. The subscriber basically has request reply kind of communication with the publisher and the subscriber.

***Working of Broker***
After it has been started, the broker receives the publisher information and then relays it to a request made by the subscriber. It is then polled every 10seconds to see any new requests from the publisher or the subscriber. As soon as it receives any request, it stores the information of the publisher in the buffer and waits for a connecting subscriber.

***Subscriber***
The subcriber program again asks the user to choose from any available ports and topics. The user gets the information of all the available publishers and then can connect to any of the available publishers under avaialable topics.

***Working of Subscriber***
After choosing the publisher and topic, the subscriber directly connects to the publisher and receives information from the subscribed publisher. If a publishing subscriber dies it listens to the network to see if there is any other avialble publisher sending out the information. If so it will connect itself to the next publisher according to ownership_strength list.

***Some features we have tried to implement in our work***

1) ***History***
Every subsriber which joins in late will get all the information from the beginning which the publisher has sent. For this we have implemented a buffer which stores in all the information as a list and sends it to the subscriber along with the current information and topic.

To be precise, a publisher will send (current information, topic, history)

The only drawback of our implementation is that every subscriber recives all the previous messages from the beginning, this could be a problem when the publisher intends to send huge amout of data. The publisher sends out the whole history everytime along with the data.

2) ***Ownership strength***
The broker is responsible to maintain the ownership strength. As soon as it gets the available publisher information, the broker makes an ownership strength list. It relays this information to the subscriber too.

This feature has been implemented through a random generator. All the available publisher information is sent to the a shuffle operation and the first publisher in the list will be assigned the highest strength and hence will have the ownership. So, if a publisher dies sometime inbetween the subscriber tries o connct to the next available publisher in order before iterating through the ownership list.

3) ***Dieing Publisher***
The other important feature we have tried to implement is the dieing publisher pattern. So, if a publisher dies or it stops sending information, the subscriber then has to connect or receive information from the other available publishers.

Taking this idea into reference we have built a pattern where, if any of the publisher dies when it is connected to a subscriber, then the subscriber waits for the next avialble publisher. It polls every 10seconds to find out if it has received the information. 

Only disadvantage with our implementation is that the subscriber waits to hear out for something in the network. It just polls every 10seconds to listen for some data on the socket.

***Data exchange***
To avoid any possible network congestion, we decided to implement a brokerless data exchange between the publisher and subscriber. So, the broker is only responsible for managing all the pub/sub data. The actual data transfer takes place directly between the respective pub/sub.


***Possible improvements to our implementation***
1) Currently our publisher can handle only one topic at a time. We are working on improving the capability for it to implement multiple topics concurrantly.

 2)Our implementation is oriented for small networks with maximum of 10 publishers and multiple subscribers. We would like extend its capabilities to perform better for larger networks too.

3) We would also like to add the publisher oriented history feature for our implementation. 

***Test cases***
Some interesting test cases which would suite our implementation are:

1)***One publisher with one subscriber***


2)***One publisher with multiple subscriber***


3)***Three publishers and many subscriber**** 




***Results***

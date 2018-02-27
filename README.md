# CS6381-01
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
The subcriber program again asks the user to choose from any available ports and topics. The user gets the information of all the available publishers and 



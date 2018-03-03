***Distributed System Principles: Assignment1***

We have three codes in this assignment. One each for publisher, broker and subcriber along with a zmq_connections file.

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

4) ***Subscriber Disconnection***
Whenever a subscriber wants to unsubscribe the services of a publisher, it can opt for it. The subscriber at the beginning will be asked about its requirments and the time for which it requires the subscription. The subscriber can choose it at will and then exit after it has received the preriodic service.

***Data exchange***
5)To avoid any possible network congestion, we decided to implement a brokerless data exchange between the publisher and subscriber. So, the broker is only responsible for managing all the pub/sub data. The actual data transfer takes place directly between the respective pub/sub.

However in the other part of our implementation we are trying to involve the broker even for communication. Here we are trying to work on the zmq.proxy(),which we have not implemented in our current implementation. 

***Possible improvements to our implementation***
1) Currently our publisher can handle only one topic at a time. We are working on improving the capability for it to implement multiple topics concurrantly.

 2) Our implementation is oriented for small networks with maximum of 10 publishers and multiple subscribers. We would like extend its capabilities to perform better for larger networks too.

3) We would also like to add the publisher oriented history feature for our implementation. 

***Testing Tips***
```
Since many cases have to be tested, we have taken a few implementation decisions.
1)The publisher is always publishing 20 numbers (for simplicity and reduction of testing time)
2)Kindly give some time delay (atleast 1min) when there are subsequent publishers and subscribers. We have synchronized the implementation with some sleep time inbetween, so that you could undertand the details printed in the terminal.
3)Kindly start the broker.py first. It made sense for us run the broker in the beginning and then the publisher followed by subscriber.
```

***Terminal Test cases***
Some interesting test cases which would suite our implementation are:

1)***One publisher with one subscriber***
```
####################################################################################
1.Start up 3 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script broker.py in the third terminal using ***python broker.py***

***Expected output*** The subscriber receives all the information from publisher in format (topic, current streaming data, History)

###################################################################################
```
2)***One publisher with multiple subscriber***
```
####################################################################################
1.Start up 4 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script sub.py.in the third terminal using ***python sub.py***
5.Run the script broker.py in the fourth terminal using ***python broker.py***
6. Start in the subscriber2 script a little late to understand how the delayed subscriber receives the current streaming data along with history.
***Expected output*** The two subscriber receives the information from publisher in format (topic, current streaming data, History)
###################################################################################
```
3)***Two publishers and many subscriber****
```
####################################################################################
1.Start up 5 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script pub.py in the second terminal using ***python pub.py***
4.Run the script sub.py.in the third terminal using ***python sub.py***
5.Run the script sub.py.in the fourth terminal using ***python sub.py***
6.Run the script broker.py in the fifth terminal using ***python broker.py***

***Expected output*** The whole idea of multiple pub-sub implementation can be obtained by running this test.
###################################################################################
```

4)***Data History***
```
####################################################################################
1.Start up 4 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script sub.py.in the third terminal using ***python sub.py***
5.Run the script broker.py in the fourth terminal using ***python broker.py***

***Expected output*** Run the second subsriber with a little delay to see that the second subscriber would start receiving the current streamed data along with the history list.

###################################################################################
```

5)***Ownership strength***
```
####################################################################################
1.Start up 5 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script pub.py in the second terminal using ***python pub.py***
4.Run the script pub.py.in the Third terminal using ***python pub.py***
5.Run the script sub.py.in the fourth terminal using ***python sub.py***
6.Run the script broker.py in the fifth terminal using ***python broker.py***

***Expected output*** Try to run the two subscribers with some delay to see that a dieing subscriber would look for the next publisher in the ownership order to connect. If the second publisher in the list is not available, then it waits and listens for some time. 
###################################################################################
```

6)***Unsubscription of subscribers at will***
```
####################################################################################
1.Start up 3 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script broker.py in the third terminal using ***python broker.py***

***Expected output*** On behalf of the subscriber, you will be asked to enter the subscription time, anything between (0-20) should be chosen as the subscription number. (For testing simplicity our publisher publishes only 20 numbers, so that you dont have to wait for long testing time)

###################################################################################
```

7)***Pollers to determine the joining of publishers and subscribers***
```
####################################################################################
1.Start up 4 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script sub.py.in the third terminal using ***python sub.py***
5.Run the script broker.py in the fourth terminal using ***python broker.py***
6. Start in the subscriber2 script a little late to understand how the delayed subscriber receives the current streaming data along with history.
***Expected output*** By running the second subscriber little late, it could be seen that the subscriber asks the broker for information about publisher. This data retreival is performed using pollers in zmq.
###################################################################################
```

***Mininet Test cases***

1)***One publisher with one subscriber***
```
####################################################################################
1.Start up 3 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script broker.py in the third terminal using ***python broker.py***

***Expected output*** The subscriber receives all the information from publisher in format (topic, current streaming data, History)

###################################################################################
```

2)***One publisher with multiple subscribers***
```
####################################################################################
1.Start up 4 terminals. 
2.Run the script pub.py in the first terminal using ***python pub.py***
3.Run the script sub.py.in the second terminal using ***python sub.py***
4.Run the script sub.py.in the third terminal using ***python sub.py***
5.Run the script broker.py in the fourth terminal using ***python broker.py***
6. Start in the subscriber2 script a little late to understand how the delayed subscriber receives the current streaming data along with history.
***Expected output*** The two subscriber receives the information from publisher in format (topic, current streaming data, History)
###################################################################################
```



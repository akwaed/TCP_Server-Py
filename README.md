# TCP_Server-Py

Test TCP implementation server done over python and implemented on a Linux Ubuntu12.04 environment. The project has to main parts namley a Main TCP server used as data storage and a Proxy sever also implemented using a TCP arthiecture with main purpose for caching.

<h3> Arthitecture Layout</h3>
This project was impemented using a VMare having three linux computers running Ubuntu1204-64-STD.How is set up is to have a computer serving as a server with another as a router and the last node a client.
![image](https://user-images.githubusercontent.com/37512610/194137272-6479ad7c-b382-43a4-904b-26cca2d47648.png)

<br>The scripts for unnig the server from the client is:
!curl http://<server ip>:8888/<router>:6789/helloworld.html # To check for a file in the server passing through the router!curl http:6789/helloworld.html # To check for a file in the server directly from client

  <h4>sample run</h4>

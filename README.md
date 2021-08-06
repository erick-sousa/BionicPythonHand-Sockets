# BionicPythonHand-Sockets

## Background
Background on this code can be found on this repository: [BionicPythonHand](https://github.com/erick-sousa/BionicPythonHand)

This program builds off that program and enables Python Socket functionality to allow the hand to be controlled remotely through a cloud server. In my case I used [Linode Cloud Hosting Service](https://www.linode.com/lp/free-credit/?locationid=72487&msclkid=f866ba779de113854427db7b22d30395&utm_source=bing&utm_medium=cpc&utm_campaign=Linode%20-%20Brand%20-%20North%20America%20-%20DC&utm_term=linode&utm_content=Linode), but any web host should work. 

## This Repository 
In making this program, the primary challenge I had to overcome was the need for different types of clients. The hand only works when plugged into a computer, and of course I would not be able to directly plug a USB into the cloud server to make the Arduino work. To overcome this, there is a "main client" and "normal clients" as well as the server. The main client is the one who has the Arduino plugged into their computer, in this case, this role is assigned to the first person who connects to the server. All other connections are given the normal client role. Normal clients are same TKinter GUI found on the [BionicPythonHand](https://github.com/erick-sousa/BionicPythonHand) repository. These clients send their requests to the server by pressing the buttons on the GUI. The server will process the request, update variables, and relay the request to the main client. The main client has a program that will automatically set the servo motors to the appropriate angles based on the original request. Below is a simple diagram showing the flow of information through the server.

![Server Diagram](https://github.com/erick-sousa/BionicPythonHand-Sockets/blob/main/pictures/Server%20Diagram.png)

There are three files Python files in this repository. First I'll look at the [server.py](server.py) file. This program is ran on the web server and will initialize the Python socket and await connections from the server. Once there are connections, it will receive data as a pickled dictionary containing all of the information associated with the request of the client. It then updates variables of the angles and stores sends the updated values and their associated finger to the main client. Servo angle variables are stored on the main server to make it easy for multiple users to be connected to the server at once without conflicting angles reaching the main client.

The [main_client.py](main_client.py) file is given to the person who intends on having the Arduino plugged into their computer. This client's program will receive a pickled dictionary with the processed data from the server and set the servo's to the appropriate angles. 

The [clien.py](clien.py) file is for all normal clients and they are able to connect to the server by opening the TKinter GUI. These clients can simply use the buttons and input boxes on the GUI to send their request to the server, and the main client will receive and use this data in a very short amount of time. This allows for quick and efficient use of the hand remotely.

To improve the program, I hope to make the server more robust, for example it does not properly handle people disconnecting from the server and returns and error. The server does not break as a result of the error, but it is still not ideal. Beyond that, a more efficient method of assigning the main client role would be better, as currently it simply assigns this role to the first person to connect which can lead to issues.

# Closing
This program allows for the bionic hand to be controlled remotely using a cloud server which enables quick remote testing of the hand's functionality, or new programs that control the hand. In the current state it works off of the TKinter GUI, but could be altered to send data in any way the user wants. The server is not very robust and relies entirely on the user's knowing which order to connect in, or else the server needs to be restarted. Besides the flaws, it works excellently.

# BionicPythonHand-Sockets

## Background
Background on this code can be found on this repository: [BionicPythonHand](https://github.com/erick-sousa/BionicPythonHand)

This program builds off that program and enables Python Socket functionality to allow the hand to be controlled remotely through a cloud server. In my case I used [Linode Cloud Hosting Service](https://www.linode.com/lp/free-credit/?locationid=72487&msclkid=f866ba779de113854427db7b22d30395&utm_source=bing&utm_medium=cpc&utm_campaign=Linode%20-%20Brand%20-%20North%20America%20-%20DC&utm_term=linode&utm_content=Linode), but any web host should work. 

## This Repository 
In making this program, the primary challenge I had to overcome was the need for different types of clients. The hand only works when plugged into a computer, and of coures I would not be able to directly plug a USB into the cloud server to make the Arduino work. To overcome this, there is a "main client" and "normal clients" as well as the server. The main client is the one who has the Arduino plugged into their computer, in this case, this role is assigned to the first person who connects to the server. All other connections are given the normal client role. Normal clients are same TKinter GUI found on the [BionicPythonHand](https://github.com/erick-sousa/BionicPythonHand) repository. These clients send their requests to the server by pressing the buttons on the GUI. The server will process the request, update variables, and relay the request to the main client. The main client has a program that will automatically set the servo motors to the appropriate angles based on the original request. Below is

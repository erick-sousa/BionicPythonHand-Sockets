from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import random

#pyfirmata setup

indexangle = 0
middleangle = 0
ringangle = 0
pinkyangle = 0
thumbangle = 0
allangles = [indexangle, middleangle, ringangle, pinkyangle, thumbangle]

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

clients = {}
send_to_main = {}
allnames = []

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    print("Initializing Arduino")
    #allfingers = [index, middle, ring, pinky, thumb]
    fingernames = ['Index', 'Middle', 'Ring', 'Pinky', 'Thumb']
    print("Arduino initialized")
    name = str(random.randint(1000, 9999))
    state = False
    for clients1 in clients.values():
        while state == False:
            if name in clients1:
                name = str(random.randint(1000, 9999))
            else:
                state = True
    allnames.append(name)
    clients[client] = name
    print(clients)
    while True:
        msg = client.recv(BUFSIZ)
        data = pickle.loads(msg)
        print(data)

        #Contract/Extend
        if data['button'] == 0:
            allangles[data['finger']] = data['angle']
            send_to_main= {
                'angle': allangles[data['finger']],
                'finger': data['finger'],
                'protocol': 0
            }
            msg = pickle.dumps(send_to_main, 2)
            list(clients.keys())[list(clients.values()).index(allnames[0])].send(bytes(msg))

        #Add/Sub
        def angle_check(x):
            if x>180:
                x = 180
            elif x<0:
                x=0
            return x
        if data['button'] == 1:
            allangles[data['finger']] += data['angle']
            allangles[data['finger']] = angle_check(allangles[data['finger']])
            send_to_main = {
                'angle': allangles[data['finger']],
                'finger': data['finger'],
                'protocol': 0
            }
            msg = pickle.dumps(send_to_main, 2)
            list(clients.keys())[list(clients.values()).index(allnames[0])].send(bytes(msg))

        angles_send = []
        #Presets
        if data['button'] == 2:
            x=0
            for finger in range(5):
                allangles[x] = data['angle'][x]
                angles_send.append(allangles[x])
                x+=1
            send_to_main = {
                'angle': angles_send,
                'finger': '',
                'protocol': 1
            }
            msg = pickle.dumps(send_to_main, 2)
            list(clients.keys())[list(clients.values()).index(allnames[0])].send(bytes(msg))

        angles_send = []
        #Customs
        if data['button'] == 3:
            x=0
            for finger in range(5):
                if data['angle'][x] > 180:
                    angles_send.append(181)
                else:
                    allangles[x] = data['angle'][x]
                    angles_send.append(data['angle'][x])
                x+=1
            send_to_main = {
                'angle': angles_send,
                'finger': '',
                'protocol': 1
            }
            msg = pickle.dumps(send_to_main, 2)
            list(clients.keys())[list(clients.values()).index(allnames[0])].send(bytes(msg))



def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 5555
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
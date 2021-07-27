from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import pyfirmata
from pyfirmata import SERVO
import platform

#pyfirmata setup

board = pyfirmata.Arduino('com3')

index = board.get_pin('d:11:o')
middle = board.get_pin('d:10:o')
ring = board.get_pin('d:9:o')
pinky = board.get_pin('d:6:o')
thumb = board.get_pin('d:5:o')

pins = ['11', '10', '9', '6', '5']
x = 0
board.digital[11].mode = SERVO
for pin in pins:
    board.digital[int(pin)].mode = SERVO
    x += 1

allfingers = [index, middle, ring, pinky, thumb]

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ)
            data = pickle.loads(msg)

            if data['protocol'] == 0:
                print("meh")
                allfingers[data['finger']].write(data['angle'])
                data.clear()

            elif data['protocol'] == 1:
                index = 0
                for angle in data['angle']:
                    if angle == 181:
                        pass
                    else:
                        allfingers[index].write(angle)
                    index+=1
                data.clear()
        except OSError:  # Possibly client has left the chat.
            break


HOST = '45.79.209.57'
PORT = 5555
#45.79.209.57
#192.168.1.111
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
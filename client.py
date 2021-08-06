from tkinter import *
import functools
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
import platform
#test
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
        except OSError:  # Possibly client has left the chat.
            break


class UI_Creation:
    finger_input_list = []

    buttons = []
    buttonNames = ["Contract", "Extend", "Add", "Subtract", "Peace", "Rockstar", "Okay", "Point", "Phone"]     #used for labeling buttons
    buttonRows = [7, 8, 15, 16, 11, 4]      #used for selecting rows of buttons

    labelNames = ["Index", "Middle", "Ring", "Pinky", "Thumb", "Custom Angles", "Quick Moves", "Presets", "Add or Subtract"]
    labelRows = [1, 6, 14, 0, 5, 10, 13]
    labelParams = [None, '#c0c0c2', None, "ridge", 'TkDefaultFont 9 underline']

    def __init__(self):
        pass

    #Method to create the input boxes
    def createinput(self, root, column):
        input = Entry(root, width= 16, borderwidth=1, relief="ridge", justify='center')
        input.grid(row=2, column=column)
        return input

    #Method to create the buttons
    def createbutton(self, root, name, column, row, command):
        button = Button(root, text=name, width=13, command=command)
        button.grid(row=row, column=column)
        return button

    #Method to create the buttons
    def createlabel(self, root, name, color, relief, font, row, column):
        label = Label(root, text=name, width=14, borderwidth=1, bg=color, relief=relief, font=font)
        label.grid(row=row, column=column)


    #Creates all UI elements
    def creatui(self, root, fingers):
        x = 0
        #Adds input boxes to UI
        for finger in fingers:
            associated_inputs = [finger, self.createinput(root, x)]
            self.finger_input_list.append(associated_inputs)
            x+=1

        #Adds buttons to UI
        x, column  = 0, 0
        #Adds Contract/Extend/Add/Sub buttons
        while x <= 3:
            index = 0
            for finger in fingers:
                commands = [finger.contractfinger, finger.extendfinger, finger.addangle, finger.subangle]
                self.createbutton(root, self.buttonNames[x], column, self.buttonRows[x], functools.partial(commands[x], index))
                column += 1
                index+=1
                if index % 5 == 0:
                    index = 0
            column = 0
            x+=1

        #Adds preset buttons
        while x<9:
            index = 0
            for finger in fingers:
                otherbuttons = self.createbutton(root, self.buttonNames[x], column, self.buttonRows[4], functools.partial(finger.preset, index, fingers))
                self.buttons.append(otherbuttons)
                column+=1
                x+=1
                index += 1

        x, index, column = 0, 0, 0
        #Adds Labels
        #Index-Thumb labels
        while x <= 2:
            for finger in fingers:
                self.createlabel(root, self.labelNames[index], self.labelParams[1], self.labelParams[3], self.labelParams[0], self.labelRows[x], column)
                index += 1
                column += 1
            index, column = 0, 0
            x+=1
        index = 5

        #Custom Angles/Quick Moves/Presets/AddSub
        while x < 7:
            otherlabels = self.createlabel(root, self.labelNames[index], self.labelParams[0], self.labelParams[0], self.labelParams[4], self.labelRows[x], 2)
            index += 1
            x += 1

    def getinput(self, fingers):
        angles = []
        invalid_fingers = []
        for finger_input in self.finger_input_list:
            if not finger_input[1].get().isnumeric():
                angles.append(181)
                invalid_fingers.append(finger_input[0].fingers)
            elif int(finger_input[1].get()) > 180:
                angles.append(181)
                invalid_fingers.append(finger_input[0].fingers)
            else:
                angles.append(int(finger_input[1].get()))
        data = {
            'angle': angles,
            'finger': 5,
            'button': 3,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)
        return invalid_fingers

class Assignment_Functions:
    peace = [180, 180, 0 ,0, 0]
    rock = [180, 0, 0, 180 ,180]
    okay = [0, 180, 180, 180 ,0]
    point = [180, 0, 0, 0, 180]
    phone = [0, 0, 0, 180, 180]
    presets = [peace, rock, okay, point, phone]


    labelNames = ["Index", "Middle", "Ring", "Pinky", "Thumb", "Custom Angles", "Quick Moves"]

    def __init__(self, fingers):
        self.fingers = fingers

    def create_finger_list(self, fingers):
        pin_to_finger = {}
        index = 0
        for finger in fingers:
            pin_to_finger[finger.boardname] = self.labelNames[index]
            index += 1

    def extendfinger(self, finger):
        data = {
            'angle': 180,
            'finger': finger,
            'button': 0,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)

    def contractfinger(self, finger):
        data = {
            'angle': 0,
            'finger': finger,
            'button': 0,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)

    def anglecheck(self, angle):
        if angle > 180:
            angle = 180
        elif angle < 0:
            angle = 0
        return angle

    def addangle(self, finger):
        data = {
            'angle': 15,
            'finger': finger,
            'button': 1,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)

    def subangle(self, finger):
        data = {
            'angle': -15,
            'finger': finger,
            'button': 1,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)

    def preset(self, index, fingers):
        data = {
            'angle': self.presets[index],
            'finger': 5,
            'button': 2,
            'user': platform.uname()[1]
        }
        msg = pickle.dumps(data, 2)
        client_socket.send(msg)

    def servowrite(self, index):
        index.write(self.degrees)


# TODO Spacer labels
# TODO possibly implement submit angles to object

#pyfirmata imports


#tkinter import and setup
import tkinter as tk
from tkinter import *
root = tk.Tk()
root.title("Hand Controller")

#pyfirmata setup
#board = pyfirmata.Arduino('com3')

finger_list =['index', 'middle', 'ring', 'pinky', 'thumb']
fingers = []
for finger in finger_list:
    fingers.append(Assignment_Functions(finger))


angles1 = UI_Creation()
angles1.creatui(root, fingers)

#for finger in fingers:
#    finger.boardname.write(180)

my_string_var = tk.StringVar(value="")
def angledata():
    invalids = (angles1.getinput(fingers))

    if len(invalids) == 0:
        my_string_var.set("Angles Set")
    else:
        my_string_var.set("Finger(s) " + ', '.join(invalids) + " contain invalid inputs, enter a value 0-180")
#
    #plot()


#Button
submit = Button(root, text="Submit Angles", width=11, command=angledata).grid(row=3, column=2)

#Spacer
spacerlabel = Label(root, textvariable=my_string_var).grid(row=4, column=0, columnspan=5)

#Spacer
spacerlabel23 = Label(root, text=" ").grid(row=9, column=2)

#Spacer
spacerlabel4 = Label(root, text=" ").grid(row=12, column=2)



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
root.mainloop()  # Starts GUI execution.


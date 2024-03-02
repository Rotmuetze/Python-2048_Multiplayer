import random as r
import time
import customtkinter
import threading
import socket
import os
import signal
import ipaddress

root = customtkinter.CTk()
labels = [] #spielfeld (als Label)
scorelabel = customtkinter.CTkLabel(root, text="Du : 0", font=("Arial",15),width=120 ,height=40)
enemyscorelabel = customtkinter.CTkLabel(root, text="Serversuche läuft...", font=("Arial",15),width=120,height=40)
text = customtkinter.CTkLabel(root, text="2048", font=("Arial",15),width=240,height=40)

keylog = False #verhindert merge bei mehrfacheingabe

#Für socket Kommunication
#####################################
server_selected = False
server_host = None
PORT = 6969
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
last_received_message = ""
#####################################


kill = False #True wenn T1 gekillt werden soll

#trigger bei tastendruck
def handle_key(event):
        if(last_message_gamestate() == "1"):
            if  globals()["keylog"] == False:
                globals()["keylog"] = True
                i = 0
                while i < 3:
                    i = i + 1
                    merge(event.keysym)
                #time.sleep(0.2) #fuers feeling
                newnumber()
                handle_color()
                globals()["keylog"] = False

#fügt neue Zahl hinzu
def newnumber():
    empty_labels = [label for label in labels if label.cget("text") == 0]
    if empty_labels:
        random_label = r.choice(empty_labels)
        random_label.configure(text=1)
    else:
        print()
        text.configure(text= "VERLOREN")
        wiederspielen()

#"drückt" alle Zahlen in gewünschte Richtung 
#und fügt gleiche Zahlen zusammen
def merge(direction):
    if direction == "Up" or direction == "w" or direction == "W":
        i = 0
        while i <= 11:
            if labels[4+i].cget("text") != 0:
                if labels[0+i].cget("text") == 0:
                    labels[0+i].configure(text=labels[4+i].cget("text"))
                    labels[4+i].configure(text=0)
                elif(labels[0+i].cget("text") == labels[4+i].cget("text")):
                    labels[0+i].configure(text=labels[0+i].cget("text")*2)
                    labels[4+i].configure(text=0)
            i = i + 1
    elif direction == "Down" or direction == "s" or direction == "S":
        i = 11
        while i >= 0:
            if labels[0+i].cget("text") != 0:
                if labels[4+i].cget("text") == 0:
                    labels[4+i].configure(text=labels[0+i].cget("text"))
                    labels[0+i].configure(text=0)
                elif(labels[0+i].cget("text") == labels[4+i].cget("text")):
                    labels[4+i].configure(text=labels[4+i].cget("text")*2)
                    labels[0+i].configure(text=0)
            i = i - 1     
    elif direction == "Left" or direction == "a" or direction == "A":
        i = 0
        while i <= 12:
            if labels[1+i].cget("text") != 0:
                if labels[0+i].cget("text") == 0:
                    labels[0+i].configure(text=labels[1+i].cget("text"))
                    labels[1+i].configure(text=0)
                elif(labels[1+i].cget("text") == labels[0+i].cget("text")):
                    labels[0+i].configure(text=labels[0+i].cget("text")*2)
                    labels[1+i].configure(text=0)
            if labels[2+i].cget("text") != 0:
                if labels[1+i].cget("text") == 0:
                    labels[1+i].configure(text=labels[2+i].cget("text"))
                    labels[2+i].configure(text=0)
                elif(labels[2+i].cget("text") == labels[1+i].cget("text")):
                    labels[1+i].configure(text=labels[1+i].cget("text")*2)
                    labels[2+i].configure(text=0)
            if labels[3+i].cget("text") != 0:
                if labels[2+i].cget("text") == 0:
                    labels[2+i].configure(text=labels[3+i].cget("text"))
                    labels[3+i].configure(text=0)
                elif(labels[3+i].cget("text") == labels[2+i].cget("text")):
                    labels[2+i].configure(text=labels[2+i].cget("text")*2)
                    labels[3+i].configure(text=0)
            i = i + 4
    elif direction == "Right" or direction == "d" or direction == "D":
        i = 0
        while i <= 15:
            if labels[2+i].cget("text") != 0:
                if labels[3+i].cget("text") == 0:
                    labels[3+i].configure(text=labels[2+i].cget("text"))
                    labels[2+i].configure(text=0)
                elif(labels[2+i].cget("text") == labels[3+i].cget("text")):
                    labels[3+i].configure(text=labels[3+i].cget("text")*2)
                    labels[2+i].configure(text=0)
            if labels[1+i].cget("text") != 0:
                if labels[2+i].cget("text") == 0:
                    labels[2+i].configure(text=labels[1+i].cget("text"))
                    labels[1+i].configure(text=0)
                elif(labels[1+i].cget("text") == labels[2+i].cget("text")):
                    labels[2+i].configure(text=labels[2+i].cget("text")*2)
                    labels[1+i].configure(text=0)
            if labels[0+i].cget("text") != 0:
                if labels[1+i].cget("text") == 0:
                    labels[1+i].configure(text=labels[0+i].cget("text"))
                    labels[0+i].configure(text=0)
                elif(labels[0+i].cget("text") == labels[1+i].cget("text")):
                    labels[1+i].configure(text=labels[1+i].cget("text")*2)
                    labels[0+i].configure(text=0)
            i = i + 4
    
    handle_color()
    root.update()

#ändert Labelfarbe anhand der Zahl
def handle_color():
    for label in labels:
        if(label.cget("text") == 1):
            label.configure(fg_color="cyan")
        elif(label.cget("text") == 2):
           label.configure(fg_color="light sea green")
        elif(label.cget("text") == 4):
           label.configure(fg_color="dodger blue")
        elif(label.cget("text") == 8):
           label.configure(fg_color="slate blue")
        elif(label.cget("text") == 16):
           label.configure(fg_color="dark slate blue")
        elif(label.cget("text") == 32):
           label.configure(fg_color="DeepPink2")
        elif(label.cget("text") == 64):
            label.configure(fg_color="tomato")
        elif(label.cget("text") == 128):
            label.configure(fg_color="orange")
        elif(label.cget("text") == 256):
            label.configure(fg_color="DarkGoldenrod4")
        elif(label.cget("text") == 512):
            label.configure(fg_color="maroon1")
        elif(label.cget("text") == 1024):
            label.configure(fg_color="maroon4")
        elif(label.cget("text") == 2048):
            label.configure(fg_color="purple4")
        else:
            label.configure(fg_color="white")

def on_closing():
    os.kill(os.getpid(), signal.SIGTERM) #sry ging nicht anders :)

def wiederspielen():
    wiederspielen = customtkinter.CTkToplevel(root)
    wiederspielen.title("Nochmal?")
    wiederspielen.geometry("200x200")
    label = customtkinter.CTkLabel(wiederspielen, text="Nochmal spielen?")
    label.pack(padx=20, pady=20)
    button1 = customtkinter.CTkButton(wiederspielen,text="Ja",command=play_again)
    button1.pack(padx=20,pady=5)
    button2 = customtkinter.CTkButton(wiederspielen,text="Nein",command=on_closing)
    button2.pack(padx=20,pady=5)
    
def play_again():
    restart = threading.Thread(target=newgame, args=())
    restart.start()
    time.sleep(0.2)
    on_closing()

def newgame():
    try:
        os.system('python Python-2048_Multiplayer/2048-Client.py')
    except:
        print("ERROR")
    try:
        os.system('2048-Client.exe')
    except:
        print("ERROR")
#startet spiel
def handle_start():
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("2048")
    root.minsize(500,550)
    root.maxsize(500,550)
    root.config(background="white")
    root.bind("<KeyPress>", handle_key)
    global server_selected

    dialog = customtkinter.CTkInputDialog(text="Server IP-Adresse:", title="Server IP")
    input = dialog.get_input()
    try:
        if ipaddress.ip_address(input):
            global server_host
            server_host = input
            server_selected = True
    except:
        handle_start()

    scorelabel.grid(row=0, column=0)
    text.grid(row=0, column=1, columnspan=2)  
    enemyscorelabel.grid(row=0, column=3)

    #inizialisierung spielfeld
    for i in range(4):
        for j in range(4):
            label = customtkinter.CTkLabel(master=root, text=0, fg_color="white",text_color="black",bg_color="white", font=("Arial",25),width=120,height=120, corner_radius=25)
            label.grid(row=i+1, column=j, padx=2, pady=2)
            labels.append(label)

    #spielanfang
    newnumber()
    newnumber()
    newnumber()
    newnumber()
    newnumber()
    handle_color()
    root.mainloop()

#communication to server, opened in thread t1
def handle_com():
    global server_selected
    global server_host
    while not server_selected:
        time.sleep(1)
    server_connected = False
    try:
        socket.connect((server_host,PORT))
        server_connected = True
    except ConnectionRefusedError:
        print("Server wird gesucht...")
        handle_com()
        time.sleep(2)
    if server_connected:
        enemyscorelabel.configure(text="Spielersuche läuft...")
        while True:
            try:
                socket.send(f":{count_score()}:;{get_highest_number()};".encode('utf-8'))
                global last_received_message
                last_received_message = socket.recv(1024).decode('utf-8')
                if(last_message_gamestate() == "1"):
                    enemyscorelabel.configure(text= f"Gegner: {last_message_enemyheighestcount()}")
                    scorelabel.configure(text= f"Du: {get_highest_number()}")
                elif(last_message_gamestate() == "2"):
                    text.configure(text= "GEWONNEN")
                    wiederspielen()
                    while True:#unschön ik ik
                        time.sleep(0.01)
                elif(last_message_gamestate() == "3"):
                    text.configure(text= "VERLOREN")
                    wiederspielen()
                    while True:#unschön ik ik
                        time.sleep(0.01)
                elif(last_message_gamestate() == "0"):
                    enemyscorelabel.configure(text= "Spielersuche läuft...")
            except ConnectionResetError:
                print("Die Verbindung zum Server wurde verloren")
                print("Versuche erneut in: 2 Sekunden")
                time.sleep(2)
                handle_com()

def count_score():
    counter = 0
    for label in labels:
       counter = counter + label.cget("text")
    return counter

def get_highest_number():
    highest = 0
    for label in labels:
        if label.cget("text") > highest:
            highest = label.cget("text")
    return highest

def last_message_gamestate():
    return (last_received_message[int(last_received_message.find(":"))+1:int(last_received_message.rfind(":"))])

def last_message_enemyscore():
    return (last_received_message[int(last_received_message.find(";"))+1:int(last_received_message.rfind(";"))])

def last_message_enemyheighestcount():
    return (last_received_message[int(last_received_message.find(","))+1:int(last_received_message.rfind(","))])


t1 = threading.Thread(target=handle_com, args=())
t1.start()
handle_start()


#written by Benjamin Wende

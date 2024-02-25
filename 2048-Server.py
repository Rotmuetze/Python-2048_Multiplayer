import socket
import datetime
import time
import threading
import sys

PORT = 6969
HOST = socket.gethostbyname(socket.gethostname())
queue = []
queueaddress = []

def handle_queuecounting():
    time.sleep(1)
    while True:
        print(f"In der Warteschlange: {len(queue)}")
        time.sleep(5)

def handle_match(com1 : socket,add1,com2 : socket,add2):
    timeout = 10
    gamestate1 = 1
    gamestate2 = 1
    print(f"Neues Match mit: {com1} und {com2}")
    while True:
        try:
            message1 = com1.recv(1024).decode('utf-8')
            message2 = com2.recv(1024).decode('utf-8')
            com1.send(f":{gamestate1}:;{lastmessage_score(message2)};,{lastmessage_highestnumber(message2)},".encode('utf-8'))
            com2.send(f":{gamestate2}:;{lastmessage_score(message1)};,{lastmessage_highestnumber(message1)},".encode('utf-8'))
        except:
            print("Kein Verbindung zu einem der Spieler.")
            print(f"Timeout in: {timeout}")
            timeout = timeout - 1
            time.sleep(1)
            if timeout == 0:
                print("-----------------------------------------------")
                print("Timeout...")
                print("Socket wird gelöscht, Sitzung wird gelöscht")
                print("-----------------------------------------------")
                try:
                    queue.remove(com1)
                    queueaddress(com1)
                except:
                    print(f"Spieler {com1} bereits gelöscht. Wird übersprungen")
                
                try:
                    queue.remove(com2)
                    queueaddress(com2)
                except:
                    print(f"Spieler {com2} bereits gelöscht. Wird übersprungen")
                sys.exit()
        if  lastmessage_highestnumber(message1) == "64":
            gamestate1 = 2
            gamestate2 = 3
        if lastmessage_highestnumber(message2) == "64":
            gamestate1 = 3
            gamestate2 = 2

def handle_matchmaking():
    while True:
        if len(queue) >= 2:
            threadmatch = threading.Thread(target=handle_match,args=(queue[0],queueaddress[0],queue[1],queueaddress[1]))
            threadmatch.start()
            del queue[0]
            del queue[0]
            del queueaddress[0]
            del queueaddress[0]

        else:
            print(f"Nur {len(queue)} Spieler da. Spielsuche wird in 5 Sekunden erneut probiert!")
            time.sleep(5)

def lastmessage_score(message):
    return (message[int(message.find(":"))+1:int(message.rfind(":"))])

def lastmessage_highestnumber(message):
    return (message[int(message.find(";"))+1:int(message.rfind(";"))])

    
threadtime = threading.Thread(target=handle_queuecounting)
threadtime.start()

threadmatchmaking = threading.Thread(target=handle_matchmaking)
threadmatchmaking.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5) #fängt an zuzuhören, begrenzt connections

#enthält gamestatus falls da (0 kein spiel am laufen,1 spiel am laufen, 2 spieler hat gewonnen, 3 spieler hat verloren)

while True:
    #time
############################################################################################
    current_datetime = datetime.datetime.now()
    timestamp = current_datetime.timestamp()
    formatted_string = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
############################################################################################
    communicaton_socket, address = server.accept()
    queue.append(communicaton_socket)
    queueaddress.append(address)
    print(f"Verbunden mit {address} um {formatted_string}")
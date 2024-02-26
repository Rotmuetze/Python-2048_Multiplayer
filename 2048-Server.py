import socket
import datetime
import time
import threading
import sys

PORT = 6969
HOST = socket.gethostbyname(socket.gethostname())
queue = []
queueaddress = []

def handle_queue():
        while True:
            time.sleep(2)
            for player in queue:
                try:
                    player.recv(1024).decode('utf-8')
                    player.send(f":{0}:;{0};,{0},".encode('utf-8'))
                except:
                    print("Spieler wird aus Warteschlange entfernt")
                    del queueaddress[queue.index(player)]
                    del queue[queue.index(player)]
            

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
        except ConnectionResetError:
            print("Kein Verbindung zu einem der Spieler.")
            print(f"Timeout in: {timeout}")
            timeout = timeout - 1
            print(timeout)
            time.sleep(1)
            if timeout == 0:
                print("-----------------------------------------------")
                print("Timeout...")
                print("Sitzung wird gelöscht")
                print("-----------------------------------------------")
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
            print(f"Nur {len(queue)} Spieler da. Matchmaking nicht möglich")
            time.sleep(1)

def lastmessage_score(message):
    return (message[int(message.find(":"))+1:int(message.rfind(":"))])

def lastmessage_highestnumber(message):
    return (message[int(message.find(";"))+1:int(message.rfind(";"))])

print("####################################################")
print("                  Server Boot                       ")
print(f"IP: {socket.gethostbyname(socket.gethostname())}")
print()
print("####################################################")

threadtime = threading.Thread(target=handle_queue)
threadtime.start()

threadmatchmaking = threading.Thread(target=handle_matchmaking)
threadmatchmaking.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(20) #fängt an zuzuhören, begrenzt connections

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
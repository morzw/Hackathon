import socket
import _thread
import time
import struct
import threading
import random

FORMAT = "32s 1s 40s 1s 256s 256s"
bufferSize = 1024
points = 0
teams_list = []
array = [1, 1, 2, 2]
random.shuffle(array)
counter1 = 0
counter2 = 0
clients = []
team_1 = []
team_2 = []
index_counter = 0
t_end = time.time() + 10
thread_count = 0


def fun_facts():
    """
    :return: prints randomly a fun fact :)
    """
    list_of_facts = ["More Than 80% of Daily Emails in the U.S. are Spam",
                     "The Parts for the Modern Computer Were First Invented in 1833",
                     "The First Gigabyte Drive Cost $40,000", "MIT Has Computers That can Detect Fake Smiles"]
    fact = random.choice(list_of_facts)
    return ("Fun Fact:\n" + fact)


def play_the_game_thread_group_1(client, address):
    global counter1
    lock = threading.RLock()
    t_end3 = time.time() + 10
    while time.time() < t_end3:
        try:
            key = client.recv(bufferSize)
            keyboard_press = key.decode()
            if keyboard_press != "":
                with lock:
                    counter1 = counter1 + 1
        except:
            continue
    return


def play_the_game_thread_group_2(client, address):
    global counter2
    lock = threading.RLock()
    t_end3 = time.time() + 10
    while time.time() < t_end3:
        try:
            key = client.recv(bufferSize)
            keyboard_press = key.decode()
            if keyboard_press != "":
                with lock:
                    counter2 = counter2 + 1
        except:
            continue
    return


def on_new_client(clientSocket, addr):
    global t_end
    global clients
    global team_1
    global team_2
    global index_counter
    global counter1
    global counter2
    lock = threading.RLock()
    lock1 = threading.RLock()
    lock2 = threading.RLock()
    try:
        group_name = clientSocket.recv(1024).decode()
        if group_name != "":
            with lock:
                clients.append(group_name)
            while len(clients) < 4:
                time.sleep(1)
            index_counter = len(team_1) + len(team_2)
            if index_counter < 4:
                group_num = array[index_counter]
                if group_num == 1:
                    with lock1:
                        team_1.append(group_name)
                if group_num == 2:
                    with lock2:
                        team_2.append(group_name)
            while len(team_1) + len(team_2) < 4:
                time.sleep(1)
        while time.time() < t_end:
            time.sleep(1)
        welcome_game = "Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n" + team_1[0] + team_1[1] \
                       + "Group 2:\n==\n" + team_2[0] + team_2[1] + "\nStart pressing keys on your keyboard as fast as " \
                                                                    "you can!!\n "
        clientSocket.send(welcome_game.encode())
        if group_num == 1:
            _thread.start_new_thread(play_the_game_thread_group_1, (clientSocket, addr))
        if group_num == 2:
            _thread.start_new_thread(play_the_game_thread_group_2, (clientSocket, addr))
        time.sleep(10)
        if counter2 > counter1:
            winning_group = "Group 2"
            team_winners = team_1[0] + team_1[1]
        else:
            winning_group = "Group 1"
            team_winners = team_2[0] + team_2[1]
        finish_message = str(fun_facts()) + "\n" + "\nGame over!\nGroup 1 typed in " + str(
            counter1) + " characters. Group 2 typed in " \
                         + str(counter2) + " characters.\n" + winning_group + " wins!\n\n" \
                         + "Congratulations to the winners:\n==\n" + "" + team_winners
        clientSocket.send(finish_message.encode())
        return
    except:
        print("error occurred")


def group_name_client_thread():
    global counter1
    global counter2
    global thread_count
    lock_thread_count = threading.RLock()
    try:
        global t_end
        TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        TCPServerSocket.bind(("", 10))
        TCPServerSocket.listen(1)
        while time.time() < t_end and thread_count < 4:
            clientSocket, addr = TCPServerSocket.accept()
            group_thread = threading.Thread(target=on_new_client, args=(clientSocket, addr))
            group_thread.start()
            with lock_thread_count:
                thread_count += 1
        return
    except:
        print("Wrong type of message received")


# ########################start of server logic:#################################
# localIP ="127.0.0.1"

localPort = 7700

# Create a UDP socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPServerSocket.bind(('', localPort))
print("Server started' listening on IP address 172.1.0.52")
thread = threading.Thread(target=group_name_client_thread, args=())
thread.start()
while time.time() < t_end:
    try:
        MSG = struct.pack('<3Q', 0xfeedbeef, 0x2, 0xA)
        UDPServerSocket.sendto(MSG, ('<broadcast>', 13117))
        time.sleep(1)
    except:
        time.sleep(1)
while time.time() < t_end:
    time.sleep(1)
time.sleep(10)
print("Game over, sending out offer requests...")
while True:
    MSG = struct.pack('<3Q', 0xfeedbeef, 0x2, 0xA)
    UDPServerSocket.sendto(MSG, ('<broadcast>', 13117))
    time.sleep(1)

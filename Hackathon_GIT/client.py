import socket
import time
import struct
import msvcrt
import string
import random
import _thread as thread

bufferSize = 1024
FORMAT = "32s 1s 40s 1s 256s 256s"

# Create a UDP socket:
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # allow broadcast
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPClientSocket.bind(("", 13117))

print("Client started, listening for offer requests...")
t_end = time.time() + 10
while time.time() < t_end:
    try:
        msg1 = UDPClientSocket.recvfrom(bufferSize)
        msg = struct.unpack('<3Q', msg1[0])
        msg += msg1[1]
        if msg[0] == 4276993775 and msg[1] == 2:
            print("“Received offer from " + msg[3] + ", attempting to connect...")
            tcp_port = msg[2]
            try:
                letters = string.ascii_lowercase #TODO - delete
                result_str = ''.join(random.choice(letters) for i in range(5)) #TODO - delete
                ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TODO - delete
                ClientSock.connect(('localhost', tcp_port))
                team_name = result_str+"\n" #TODO - change for team name
                ClientSock.send(team_name.encode())
            except:
                break
            try:
                game_begins_message = ClientSock.recv(bufferSize).decode()
                if game_begins_message != "":
                    print(game_begins_message)
                    t_end3 = time.time() + 10
                    while time.time() < t_end3:
                        char = msvcrt.getch()
                        pressedKey = char.decode('ASCII')
                        ClientSock.send(pressedKey.encode())
                    results_message = ClientSock.recv(bufferSize).decode()
                    if game_begins_message != "":
                        print(results_message)
            except:
                break
    except:
        break
print("Server disconnected, listening for offer requests...")
while True:
    msg1 = UDPClientSocket.recvfrom(bufferSize)


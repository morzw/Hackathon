import socket
import time
import struct
import threading

FORMAT = "32s 1s 40s 1s 256s 256s"
bufferSize = 1024
clients = []
points = 0


def play_the_game_thread(client, address):
    global points
    lock = threading.RLock()
    t_end3 = time.time() + 10
    while time.time() < t_end3:
        try:
            key = client.recv(bufferSize)
            keyboard_press = key.decode()
            if keyboard_press != "":
                print(keyboard_press)
                with lock:
                    points += 1
        except:
            continue
        print(points)


def group_name_client_thread():
    try:
        TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        TCPServerSocket.bind(("", 10))
        TCPServerSocket.listen(4)
        t_end2 = time.time() + 10
        while time.time() < t_end2:
            clientSocket, addr = TCPServerSocket.accept()
            clients.append((clientSocket, addr))
            sentence = clientSocket.recv(1024).decode()
            if sentence != "":
                print(sentence)
            break
        for (client, addr) in clients:
            sentence = "Game Begins\n"
            client.send(sentence.encode())
            thread = threading.Thread(target=play_the_game_thread, args=(client, addr))
            thread.start()
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

print("Server started' listening on IP address 172.1.0.88")
thread1 = threading.Thread(target=group_name_client_thread, args=())
thread1.start()
t_end = time.time() + 10
while time.time() < t_end:
    try:
        MSG = struct.pack('<3Q', 0xfeedbeef, 0x2, 0xA)
        UDPServerSocket.sendto(MSG, ('<broadcast>', 13117))
        print("message sent!")
        time.sleep(1)
        print(points)
    except:
        time.sleep(1)

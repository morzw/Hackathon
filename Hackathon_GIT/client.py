import socket
import time
import struct
import msvcrt
import _thread as thread

bufferSize = 1024
FORMAT = "32s 1s 40s 1s 256s 256s"

# Create a UDP socket:
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # allow broadcast
UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPClientSocket.bind(("", 13117))

print("Client started' listening for offer requests")
t_end = time.time() + 10
while time.time() < t_end:
    try:
        msg1 = UDPClientSocket.recvfrom(bufferSize)
        msg = struct.unpack('<3Q', msg1[0])
        msg += msg1[1]
        if msg[0] == 4276993775 and msg[1] == 2:
            print("Great success!")
            tcp_port = msg[2]
            print(tcp_port)
            try:
                ClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientSock.connect(('localhost', tcp_port))
                sentence = "Raz\n"
                ClientSock.send(sentence.encode())
            except:
                break
            try:
                game_begins_message = ClientSock.recv(bufferSize).decode()
                if game_begins_message != "":
                    print(game_begins_message)
                while 1:
                    char = msvcrt.getch()
                    pressedKey = char.decode('ASCII')
                    ClientSock.send(pressedKey.encode())
            except:
                break
    except:
        break

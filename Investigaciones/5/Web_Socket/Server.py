import socket
import threading
import random
import string

direcciones_mac_permitidas = ['34-6F-24-BF-C3-E5', '28-7F-CF-CD-62-D4']

HEADER = 64
PORT = 8380
SERVER = '192.168.1.99'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'salir'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            msg = decrypt(msg)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            


            

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            

    conn.close()    


def start():
    server.listen()
    print(f"[LISTEN] Server is listening on address {ADDR}")
    while True:
        conn, addr = server.accept()
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg in direcciones_mac_permitidas:
            conn.send("aceptado".encode(FORMAT))
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        else: 
            print(f"Intento de ingreso (MAC) denegada : {msg}")
            conn.send("Acceso denegado".encode(FORMAT))

def decrypt(msg):
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    chars = list(chars)
    key = chars.copy()
    random.seed(1234)
    random.shuffle(key)
    plain_text = ""
    cipher_text = msg
    for letter in cipher_text:
        index = key.index(letter)
        plain_text += chars[index]
    return plain_text

print("[STARTING] server is running.....")
start()
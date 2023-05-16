import socket
import subprocess
import random
import string

inword = None

HEADER = 64
PORT = 8380
SERVER = '192.168.1.99'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'salir'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conection_status = False


def mac_get():
    output = subprocess.check_output(['ipconfig', '/all'])
    for line in output.splitlines():
        if b'Wi-Fi:' in line:
            mac_address = output.splitlines()[output.splitlines().index(line) + 4].split()[-1].decode()
            break    
    return mac_address

def handshake():
    client.connect(ADDR)
    send(mac_get())
    msg = client.recv(2048).decode(FORMAT)
    return msg

def send(msg):
    message=msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    return 0
    

def talk_rutine():
    inword = None
    while inword != DISCONNECT_MESSAGE:

        inword = input()
        #inword = encrypto(inword)
        send(inword)
        print(f"{client.recv(2048).decode(FORMAT)}")           
    return 0

def encrypto(msg):
    chars = " " + string.punctuation + string.digits + string.ascii_letters
    chars = list(chars)
    key = chars.copy()
    random.seed(1234)
    random.shuffle(key)
    plain_text = msg
    cipher_text = ""

    for letter in plain_text:
        index = chars.index(letter)
        cipher_text += key[index]
    return cipher_text



comand = handshake()
if comand == "aceptado":
    print(f"<<[conectado]>>")
    talk_rutine()
print("<<[Desconectado]>>")
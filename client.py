import socket 
import threading
from colorama import init, Fore

# Iniciar (En Windows)
# init()

username = input("Ingrese su nombre de usuario: ")
print("")

'''
    Función que recibe los mensajes enviados por el servidor y los muestra al usuario
'''
def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error Ocurred")
            client.close()
            break

'''
    Función principal que inicia la conexión del cliente con el servidor y maneja sus mensajes de entrada
'''
def client():
    
    HOST = "127.0.0.1" 
    PORT = 65123 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        msg = input("")
        message = f"\n{Fore.RESET}{username}: {msg}\n"
        client.send(message.encode('utf-8'))

client()

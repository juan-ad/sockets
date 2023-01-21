import socket 
import threading
from colorama import init, Fore

# Iniciar (En Windows)
# init()

HOST = "127.0.0.1" # Dirección IP local o remota
PORT = 65123 # Puerto de escucha (>1023 están libres)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT)) # Asociar el socket con la tarjeta de red del PC
server.listen() # Se pone el socket en modo escucha
print("")
print(Fore.RED + f'Server running on {HOST}:{PORT}')
print(Fore.RESET)

clients = []
usernames = []

'''
    Función que transmite el mensaje a todos los usuarios conectados al servidor
'''
def broadcast(_client, message):
 for client in clients:
    if client != _client:
        try:
            client.send(message)
        except Exception as e:
            print('Error broadcasting message: {e}')
            remove_connection(client)

'''
    Función que remueve una conexión
'''
def remove_connection(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        broadcast(client, f'{Fore.GREEN}ChatBot: {username} se desconectó {Fore.RESET}\n'.encode('utf-8'))
        print(f'{Fore.GREEN}{username} se desconectó')
        print(Fore.RESET)
        clients.remove(client)
        usernames.remove(client)
        client.close()


'''
    Función que recibe los mensajes enviados a través del servidor y los muestra a los usuarios
'''
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(client, message)
            else:
                remove_connection(client)
                break
        except:
            remove_connection(client)
            break

'''
    Función principal que recibe las conexiones de los clientes y comienza un nuevo hilo para manejar sus mensajes
'''
def receive_connections():
    while True:
        client, addr = server.accept() # client guarda la conexión entrante de un socket cliente y addr la dirección de conexión

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')
        
        clients.append(client)
        usernames.append(username)

        print(f"{username} está conectado desde la IP {str(addr[0])}:{str(addr[1])}\n")

        message = f'\n{Fore.GREEN}ChatBot: {username} se unió al chat!{Fore.RESET}\n'.encode('utf-8')
        broadcast(client, message)
        client.send(f'{Fore.GREEN}Conectado al servidor\n{Fore.RESET}'.encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()
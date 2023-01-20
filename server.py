import socket 
import threading

HOST = "127.0.0.1" # Dirección IP local o remota
PORT = 65123 # Puerto de escucha (>1023 están libres)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT)) # Asociar el socket con la tarjeta de red del PC
server.listen() # Se pone el socket en modo escucha
print(f'Server running on {HOST}:{PORT}')

clients = []
usernames = []

# Función que envía el mensaje a todos los clientes
def broadcast(_client, message):
 for client in clients:
    if client != _client:
        client.send(message)


# Función que permite manejar los mensajes de cada cliente
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(client, message)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f'ChatBot: {username} disconnected'.encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(client)
            client.close()
            break

def receive_connection():
    while True:
        client, addr = server.accept() # conn guarda la conexión entrante de un socket cliente y addr la dirección de conexión

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')
        
        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(addr)}")

        message = f'ChatBot: {username} joined the chat!'.encode('utf-8')
        broadcast(client, message)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connection()
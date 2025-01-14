import socket
import threading

# пропишем функцию, в которой обеспечим получение сообщений текущим клиентом от других
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error while receiving a message from the server: {e}")
            break

# создаем клиентский сокет, который отправляет сообщения
# AF_INET - интернет адрес для IPv4, 
# SOCK_STREAM - сокет на основе протокола TCP (обеспечивает двунаправленный поток данных)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 9090)
client_socket.connect(server_address)

username = input("Input your name: ")
client_socket.send(username.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    message = input()
    if message.lower() == 'exit chat':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()
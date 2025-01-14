import socket
# создаем сокет, серверный сокет прослушивает определенный порт
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 9090)
msg = "Hello, server"
client_socket.sendto(msg.encode('utf-8'), server_address)
response, _ = client_socket.recvfrom(2222)
print(f"You have a response from server: {response.decode('utf-8')}")
client_socket.close()
import socket
# создаем сокет, серверный сокет прослушивает определенный порт
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# связываем сокет с хостом "" (т.к. мы делаем его доступным с любого интерфейса) и портом 9090
server_address = ("localhost", 9090)
server_socket.bind(server_address)
# принимем подключение, аргументы: новый сокет и адрес клиента
while True:
    msg, client_address = server_socket.recvfrom(2222)
    print(f"You have a bew message: {msg.decode('utf-8')}")
    response_msg = "Hello, client"
    server_socket.sendto(response_msg.encode('utf-8'), client_address)
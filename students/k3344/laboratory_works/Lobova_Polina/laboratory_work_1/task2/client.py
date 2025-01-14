import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

try:
    print(f"Для подсчета площади трапеции введите следующие данные:")
    a = float(input("Основание a: "))
    b = float(input("Основание b: "))
    h = float(input("Высота h: "))

    message = f"{a},{b},{h}"
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

except Exception as e:
    print(f"Error while communicating with the server: {e}")

finally:
    client_socket.close()
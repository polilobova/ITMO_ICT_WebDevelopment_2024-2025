import socket
import threading
from urllib.parse import parse_qs

# Конфигурация сервера
HOST = '127.0.0.1'  
PORT = 8080         
grouped_grades = {}  

def handle_client(connection, address):
    """
    Обработка запросов от клиента.
    """
    try:
        # Получаем данные от клиента
        request = connection.recv(1024).decode('utf-8')
        if not request:
            return

        # Разбираем HTTP-запрос
        headers, body = request.split('\r\n\r\n', 1)
        request_line = headers.split('\r\n')[0]
        method, path, protocol = request_line.split(' ')

        print(f"Получен {method} запрос от {address}")

        if method == 'GET':
            response_body = provide_with_html()
            send_response(connection, '200 OK', 'Content-Type: text/html', response_body)

        elif method == 'POST':
            content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])
            while len(body.encode('utf-8')) < content_length:
                body += connection.recv(1024).decode('utf-8')

            # Парсим данные POST-запроса
            params = parse_qs(body)
            discipline = params.get('discipline', [''])[0]
            grade = params.get('grade', [''])[0]

            if discipline and grade:
                # Добавляем оценку в словарь
                if discipline not in grouped_grades:
                    grouped_grades[discipline] = []
                grouped_grades[discipline].append(grade)
                send_response(connection, '200 OK', 'Content-Type: text/plain', 'Принято!')
            else:
                send_response(connection, '400 Bad Request', 'Content-Type: text/plain', 'Ошибка: Неверные данные')

        else:
            # Обработка недопустимых методов
            send_response(connection, '405 Method Not Allowed', 'Content-Type: text/plain',
                          'К сожалению, такого метода нет в списке разрешенных')

    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка при обработке запроса: {e}")
        send_response(connection, '500 Internal Server Error', 'Content-Type: text/plain', 'Внутренняя ошибка сервера')

    finally:
        connection.close()

def send_response(connection, status, content_type, body):
    """
    Отправление HTTP-ответа клиенту.
    """
    response = f"HTTP/1.1 {status}\r\n"
    response += f"{content_type}\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body
    connection.sendall(response.encode('utf-8'))

def provide_with_html():
    """
    Генерация HTML-страницы с таблицей оценок.
    """
    rows = ''.join(
        f"<tr><td>{discipline}</td><td>{', '.join(grades)}</td></tr>"
        for discipline, grades in grouped_grades.items()
    )
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Grades</title>
</head>
<body>
    <h1>Grades</h1>
    <table border="1">
        <tr><th>Discipline</th><th>Grade</th></tr>
        {rows}
    </table>
</body>
</html>"""

def start_server():
    """
    Запускает сервер.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")

        while True:
            connection, address = server_socket.accept()
            print(f"Подключен клиент: {address}")
            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()

if __name__ == "__main__":
    start_server()
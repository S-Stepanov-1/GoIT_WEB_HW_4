import json
import pathlib
import urllib.parse
import mimetypes
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime


SOCKET_SERVER = '127.0.0.1', 5000


class MyHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/":
            self._render_html("index.html")
        elif url.path == "/message":
            self._render_html("message.html")
        else:
            if pathlib.Path().joinpath(url.path[1:]).exists():
                self._render_static()
            else:
                self._render_html("error.html")

    def do_POST(self):
        data_bytes = self.rfile.read(int(self.headers["Content-Length"]))

        send_data_to_socket_server(data_bytes)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def _render_html(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())

    def _render_static(self):
        self.send_response(200)

        mimetype = mimetypes.guess_type(self.path)
        if mimetype:
            self.send_header("Content-type", mimetype[0])
        else:
            self.send_header("Content-type", 'text/plain')

        self.end_headers()

        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def send_data_to_socket_server(data_bytes):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(data_bytes, SOCKET_SERVER)
    client_socket.close()


def handle_json_file(data_dict):
    try:
        with open("storage/data.json", "r", encoding="utf-8") as json_file:
            try:
                file_data = json.load(json_file)
            except json.decoder.JSONDecodeError:
                file_data = {}

    except FileNotFoundError:
        file_data = {}

    file_data[str(datetime.now())] = data_dict

    with open("storage/data.json", "w", encoding="utf-8") as json_file:
        json.dump(file_data, json_file, indent=4, ensure_ascii=False)


def run_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(SOCKET_SERVER)

    try:
        while True:
            data_bytes = server_socket.recv(1024)
            decoded_data = urllib.parse.unquote_plus(data_bytes.decode())
            data_dict = {key: value for key, value in [item.split("=") for item in decoded_data.split("&")]}

            handle_json_file(data_dict)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        server_socket.close()


def run_http_server():
    http = HTTPServer(("", 3000), MyHTTPHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run():
    threads = []

    http_server = Thread(target=run_http_server)
    http_server.start()
    threads.append(http_server)

    socket_server = Thread(target=run_server_socket)
    socket_server.start()
    threads.append(socket_server)

    [thread.join() for thread in threads]


if __name__ == '__main__':
    run()

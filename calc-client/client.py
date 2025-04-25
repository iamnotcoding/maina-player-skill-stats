# -*- coding: utf-8 -*-

import socket
from client_config import DEFAULT_PORT, DATA_SIZE_SIZE
import json
import os

def recvall(sock, data_size, flags=0):
    data = b""
    remaining_size = data_size

    while remaining_size > 0:
        buf = sock.recv(remaining_size, flags)

        if not buf:
            raise "recv failed"

        remaining_size -= len(buf)

        data += buf

    return data

def get_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(("localhost", DEFAULT_PORT))

    return client_socket

def get_response(client_socket):
    raw_data_size = recvall(client_socket, DATA_SIZE_SIZE)
    data_size = int(raw_data_size.decode("utf-8"))
    response = recvall(client_socket, data_size).decode("utf-8")

    return json.loads(response)

def send_reqeust(socket, request):
    raw_string = json.dumps(request)
    raw_string += "\0"  # Append null terminator to the message

    socket.sendall(
            (f"{len(raw_string):{DATA_SIZE_SIZE}}" + raw_string).encode("utf-8")
        )

if __name__ == "__main__":
    os.system("chcp 65001") # Set console to UTF-8        

    client_socket = get_client_socket()
    
    while True:
        message = input("Enter message to send to server: ")

        if message.lower() == "exit":
            break

        send_reqeust(client_socket, json.loads(message))
        res = get_response(client_socket)

        if (res["description"] == "server_ended"):
            print("The server has ended")
            client_socket.close()
            break
            


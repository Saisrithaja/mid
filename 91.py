from multiprocessing import Process, Value
import time

def writer(shared_value):
    shared_value.value = 42
    print("Writer process: wrote 42 into shared memory")

def reader(shared_value):
    time.sleep(1)
    print("Reader process: read from shared memory:", shared_value.value)

if __name__ == "__main__":
    shared_value = Value('i', 0)

    writer_process = Process(target=writer, args=(shared_value,))
    reader_process = Process(target=reader, args=(shared_value,))

    writer_process.start()
    reader_process.start()

    writer_process.join()
    reader_process.join()
    
    
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"\n{message.decode()}")
        except:
            print("Disconnected from the server.")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the chat server.")

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input("You: ")
        client_socket.sendall(message.encode())
        if message.strip().lower() == "exit":
            print("Disconnecting from the server...")
            client_socket.close()
            break

if __name__ == "__main__":
    start_client()


import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []

def broadcast(message, sender_client):

    for client in clients:
        if client != sender_client:
            try:
                client.sendall(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message or message.decode().strip().lower() == "exit":
                print("Client disconnected.")
                clients.remove(client_socket)
                client_socket.close()
                break
            print(f"Received message: {message.decode()}")
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()

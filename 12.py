import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
message = "Hello, Server!"
client_socket.send(message.encode())
echoed_message = client_socket.recv(1024).decode()
print(f"Received from server: {echoed_message}")
client_socket.close()


import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))  
server_socket.listen(1)
print("Server is listening...")

conn, addr = server_socket.accept()
print(f"Connected to {addr}")

message = conn.recv(1024).decode()
print(f"Received from client: {message}")
conn.send(message.encode())

conn.close()
server_socket.close()

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
import socket
import json

SERVER_IP = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

request = {"function": "add","args": [10, 5]}
client_socket.sendall(json.dumps(request).encode())

result = client_socket.recv(1024).decode()
print("Result from server:", result)

client_socket.close()


import socket
import json

PORT  = 8080

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

FUNCTIONS = {"add": add,"subtract": subtract}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)
print("Server listening on port", PORT)

conn, addr = server_socket.accept()
print("Connection from:", addr)

data = conn.recv(1024).decode()
request = json.loads(data)

func_name = request["function"]
args = request["args"]
result = FUNCTIONS[func_name](*args)

conn.sendall(str(result).encode())
conn.close()
server_socket.close()
print("Result sent to client.")


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
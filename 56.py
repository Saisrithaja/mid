import socket

SERVER_IP = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

with open("send_file.txt", "rb") as file:
    while True:
        data = file.read(1024)
        if not data:
            break
        client_socket.sendall(data)

client_socket.close()
print("File sent to server.")


import socket

PORT = 8080


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(1)

print("Server listening on port", PORT)
conn, addr = server_socket.accept()
print("Connection from:", addr)

with open("received_file.txt", "wb") as file:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        file.write(data)

conn.close()
server_socket.close()
print("File received and saved as 'received_file.txt'")


from multiprocessing import Process, Pipe

def child_process(conn):
    message_from_parent = conn.recv()
    print(f"Child received: {message_from_parent}")
    response = "Hello from child"
    conn.send(response)
    conn.close()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    message_to_child = input("Enter a message to send to the child: ")
    p = Process(target=child_process, args=(child_conn,))
    p.start()
    parent_conn.send(message_to_child)
    response_from_child = parent_conn.recv()
    print(f"Parent received: {response_from_child}")
    parent_conn.close()
    p.join()

'''
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
    int parent_to_child[2], child_to_parent[2];
    pid_t pid;
    char parent_msg[100];
    char child_msg[100];
    char buffer[100];

    pipe(parent_to_child);
    pipe(child_to_parent);

    pid = fork();

    if (pid > 0) { // Parent process
        close(parent_to_child[0]);
        close(child_to_parent[1]);

        printf("Parent: Enter a message to send to the child: ");
        fgets(parent_msg, sizeof(parent_msg), stdin);
        parent_msg[strcspn(parent_msg, "\n")] = 0;

        write(parent_to_child[1], parent_msg, strlen(parent_msg) + 1);
        printf("Parent sent: %s\n", parent_msg);

        read(child_to_parent[0], buffer, sizeof(buffer));
        printf("Parent received: %s\n", buffer);

        close(parent_to_child[1]);
        close(child_to_parent[0]);
    } 
    else if (pid == 0) { // Child process
        close(parent_to_child[1]);
        close(child_to_parent[0]);

        read(parent_to_child[0], buffer, sizeof(buffer));
        printf("Child received: %s\n", buffer);

        printf("Child: Enter a message to send to the parent: ");
        fgets(child_msg, sizeof(child_msg), stdin);
        child_msg[strcspn(child_msg, "\n")] = 0;  // Remove newline character

        write(child_to_parent[1], child_msg, strlen(child_msg) + 1);

        close(parent_to_child[0]);
        close(child_to_parent[1]);
    }

    return 0;
}'''
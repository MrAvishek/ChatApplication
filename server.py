import socket
import threading
import time
import traceback
import subprocess
import os

HOST = '0.0.0.0'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = {}
lock = threading.Lock()
subprocess.Popen(["python", "commonRoom.py"])
def listen_for_messages(client, username):
    try:
        while True:
            data = client.recv(4096)
            if not data:
                raise ConnectionError("Connection closed by client")
                
            # if data == b'SHUTDOWN':
            #     print("💻: Shutdown signal received from client.")
            #     break  # Exit the loop to gracefully close the connection
            
            if data.startswith(b'FILE:'):
                # print("FILE called")
                handle_file_data(data, username, client)
            try:
                decoded_data = data.decode('ascii')
                if decoded_data == 'exit':
                    print("the exit message got " + decoded_data)
                    exit_message = f"🏃{username} Left "
                    log_to_file(exit_message)
                    send_messages_to_all(exit_message, client)
                    with lock:
                        active_clients.pop(username)
                    client.close()
                    break
            except UnicodeDecodeError:
                pass
                
            else:
                message = data.decode('utf-8')
                if message == '@listfiles':
                        files = list_files()
                        file_list_message = f"📁 File List:\n{os.linesep.join(files)}"
                        send_message_to_client(client, file_list_message)
                        
                if message.startswith("@getfile "):
                    file_name = message.split(" ", 1)[1]
                    file_path = os.path.join("sharedFile", file_name)
                    print("fileName and path got " + file_name + file_path)
                    if os.path.exists(file_path):
                        print("function called")
                        send_file_to_client(client, file_path,file_name)
                    else:
                        print("else called")
                        send_message_to_client(client, f"File '{file_name}' not found.")
                        
                else:
                    log_message = f"{username}: {message}"
                    log_to_file(log_message)
                    send_messages_to_all(log_message, client)
            # print("datareceived from client " +data.decode('utf-8'))
    except ConnectionError as ce:
        print(f"Error in listen_for_messages for client {username}: {ce}")
    except Exception as e:
        print(f"Error in listen_for_messages for client {username}: {e}")
        traceback.print_exc()

def list_files():
    server_directory = "sharedFile"
    files = os.listdir(server_directory)
    return files

# Inside handle_file_data function
def handle_file_data(data, username, client):
    
    try:
        print("file received from ", username)
        server_directory = "sharedFile"
        if not os.path.exists(server_directory):
            os.makedirs(server_directory)
        # Save the file to the sharedFile server_directory
        file_info, file_data = data[len(b'FILE:'):].split(b':', 1)
        file_name = file_info.decode()
        file_path = os.path.join(server_directory, file_name)
        with open(file_path, 'wb') as file:
            file_data = data[len(b'FILE:'):]
            file.write(file_data)
            while True:
                file_data = client.recv(4096)
                if file_data.endswith(b'ENDFILE'):
                    file.write(file_data[:-len(b'ENDFILE')])
                    break
                file.write(file_data)
        print(f"File saved to {file_path}")

        # add_message(f"File '{file_name}' saved successfully in 'sharedFile' directory.")
    except Exception as e:
            print(f"Error handling file data from {username}: {e}")
            traceback.print_exc()
        
def send_file_to_client(client, file_path,file_name):
    try:
        with open(file_path, 'rb') as file:
            client.sendall(f'FILE:{file_name}:'.encode())
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                client.sendall(file_data)
            client.sendall(b'ENDFILE')   
    except Exception as e:
        print(f"Error sending file to client: {e}")
        traceback.print_exc()

        
def handle_file_transfer(data, sender_username):
    # Extract file name and content
    file_data = data[len(b'FILE:'):].decode('utf-8')
    file_name, file_content = file_data.split(':', 1)

    # Broadcast file to all clients except the sender
    for username, cl in active_clients.items():
        if username != sender_username:
            try:
                # Prepare file transfer data
                file_transfer_data = f'FILE:{file_name}:{file_content}'
                cl.sendall(file_transfer_data.encode('utf-8'))
            except Exception as e:
                print(f"Error sending file to {username}: {e}")


def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")
        traceback.print_exc()

def send_messages_to_all(message, sending_client):
    with lock:
        for user, cl in active_clients.items():
            if cl != sending_client:
                send_message_to_client(cl, message)

def client_handler(client):
    try:
        while True:
            username = client.recv(2048).decode('utf-8')
            if username:
                with lock:
                    active_clients[username] = client
                join_message = f"🙋: {username} joined the chat"
                log_to_file(join_message)
                send_messages_to_all(join_message, client)
                break
            else:
                print("Client username is empty")
    except Exception as e:
        print(f"Error in client_handler: {e}")
        traceback.print_exc()

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

def log_to_file(message):
    try:
        with open('chat_log.txt', 'a', encoding='utf-8') as f:  # Specify encoding
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
        traceback.print_exc()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        traceback.print_exc()

    server.listen(LISTENER_LIMIT)

    while True:
        try:
            client, address = server.accept()
            print(f"💻: Successfully connected to client {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except Exception as e:
            print(f"Error accepting client connection: {e}")
            traceback.print_exc()

if __name__ == '__main__':
    main()

import socket
import threading
import cv2
import struct

# Define server address and ports
SERVER_IP = '0.0.0.0'
VIDEO_PORT = 9999
AUDIO_PORT = 10000

# Setup video and audio sockets
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind((SERVER_IP, VIDEO_PORT))
video_socket.listen(2)

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.bind((SERVER_IP, AUDIO_PORT))
audio_socket.listen(2)

# Function to handle sending video to a client
def send_video_to_client(client_socket, cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        # Send the frame size first (4 bytes header)
        client_socket.sendall(struct.pack('!I', len(frame_data)))
        # Send the frame data
        client_socket.sendall(frame_data)

# Function to handle audio transmission between two clients
def handle_audio(client_socket, other_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            other_socket.sendall(data)
        except:
            break

# Main server function to handle clients
def main():
    print("Server is waiting for connections...")

    # Accept video connections
    video_conn1, addr1 = video_socket.accept()
    video_conn2, addr2 = video_socket.accept()
    print(f"Video connections established with {addr1} and {addr2}")

    # Accept audio connections
    audio_conn1, addr_audio1 = audio_socket.accept()
    audio_conn2, addr_audio2 = audio_socket.accept()
    print(f"Audio connections established with {addr_audio1} and {addr_audio2}")

    # Start video streaming from one client's webcam to both
    cap = cv2.VideoCapture(0)

    # Start threads to send video to both clients
    threading.Thread(target=send_video_to_client, args=(video_conn1, cap)).start()
    threading.Thread(target=send_video_to_client, args=(video_conn2, cap)).start()

    # Handle audio streaming
    threading.Thread(target=handle_audio, args=(audio_conn1, audio_conn2)).start()
    threading.Thread(target=handle_audio, args=(audio_conn2, audio_conn1)).start()

if __name__ == "__main__":
    main()

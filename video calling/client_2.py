import cv2
import socket
import threading
import numpy as np
import struct
import sounddevice as sd
import time
from tkinter import *
from PIL import Image, ImageTk

# Define server address and ports
SERVER_IP = '0.0.0.0'  # Replace with your server IP or localhost
VIDEO_PORT = 9999
AUDIO_PORT = 10000

# Create sockets for video and audio
video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.connect((SERVER_IP, VIDEO_PORT))

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.connect((SERVER_IP, AUDIO_PORT))

# Initialize video capture from webcam
cap = cv2.VideoCapture(0)

# Video receiving function and Tkinter window update
def receive_video(window, label):
    while True:
        try:
            # Receive the frame size first (4 bytes)
            packed_size = video_socket.recv(4)
            if not packed_size:
                break
            frame_size = struct.unpack('!I', packed_size)[0]

            # Now receive the frame data based on the frame size
            data = b""
            while len(data) < frame_size:
                packet = video_socket.recv(frame_size - len(data))
                if not packet:
                    break
                data += packet

            # Decode the frame
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                # Resize the frame to fit the Tkinter window (e.g., 640x480)
                frame = cv2.resize(frame, (640, 480))

                # Convert the frame to RGB and PIL format for Tkinter display
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk  # Keep a reference to avoid garbage collection
                label.configure(image=imgtk)

            window.update_idletasks()

        except Exception as e:
            print(f"Error receiving video: {e}")
            break

# Audio sending function
def send_audio():
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        audio_socket.sendall(indata)

    with sd.InputStream(samplerate=44100, channels=1, callback=audio_callback):
        while True:
            time.sleep(0.1)  # Add a small sleep to prevent flooding the audio stream

# Audio receiving function
def receive_audio():
    while True:
        data = audio_socket.recv(4096)
        if data:
            audio_data = np.frombuffer(data, dtype=np.int16)
            if len(audio_data) > 0:
                sd.play(audio_data, samplerate=44100)

# Tkinter window setup
def setup_window():
    window = Tk()
    window.title("Video Call")

    # Set up label to hold the video feed
    label = Label(window)
    label.pack()

    return window, label

# Create and start threads for video and audio
window, label = setup_window()

video_receive_thread = threading.Thread(target=receive_video, args=(window, label))
audio_send_thread = threading.Thread(target=send_audio)
audio_receive_thread = threading.Thread(target=receive_audio)

video_receive_thread.start()
audio_send_thread.start()
audio_receive_thread.start()

# Start Tkinter event loop
window.mainloop()

# Wait for threads to complete
video_receive_thread.join()
audio_send_thread.join()
audio_receive_thread.join()

# Release resources
cap.release()
cv2.destroyAllWindows()
video_socket.close()
audio_socket.close()

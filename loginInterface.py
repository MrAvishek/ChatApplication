import tkinter as tk
from tkinter import messagebox
import socket
import subprocess

class LoginInterface:
    def __init__(self, master):
        self.master = master
        master.title("Chat Room Login")
        master.geometry("400x300")

        self.create_room_button = tk.Button(master, text="Create Room", command=self.create_room, bg="blue", fg="white", font=("Helvetica", 16))
        self.create_room_button.pack(pady=20)

        self.join_room_button = tk.Button(master, text="Join Room", command=self.join_room, bg="green", fg="white", font=("Helvetica", 16))
        self.join_room_button.pack(pady=20)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application, bg="red", fg="white", font=("Helvetica", 16))
        self.exit_button.pack(pady=20)

        # Connect to the server
        self.server_host = '127.0.0.1'
        self.server_port = 1234
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((self.server_host, self.server_port))

    def create_room(self):
        # Add functionality to create a room
        messagebox.showinfo("Create Room", "Functionality to create a room will be implemented here.")

    def join_room(self):
        # Add functionality to join a room
        messagebox.showinfo("Join Room", "Functionality to join a room will be implemented here.")

    def exit_application(self):
        # Send a shutdown signal to the server
        self.server_socket.sendall(b'SHUTDOWN')
        self.server_socket.close()
        self.master.destroy()

def main():
    root = tk.Tk()
    login_interface = LoginInterface(root)
    root.mainloop()


main()

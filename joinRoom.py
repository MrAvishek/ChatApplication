import tkinter as tk
import subprocess

class LoginInterface:
    def __init__(self, master):
        self.master = master
        master.title("Create Or Join Into a room")
        master.geometry("400x400")
        master.configure(background="#EEF0E5")

        # Text entry for creating a room code
        self.create_label = tk.Label(master, text="Enter Room Code to Create Room:", font=("Arial",11))
        self.create_label.pack(pady=10)
        self.create_entry = tk.Entry(master, width=45)
        self.create_entry.pack(pady=5)
        self.create_button = tk.Button(master, text="Create Room", command=self.create_room, bg="blue",foreground="white", font=("Helvetica", 16))
        self.create_button.pack(pady=10)

        # Text entry for joining a room
        self.join_label = tk.Label(master, text="Enter Room Code to Join Room:",font=("Arial",11))
        self.join_label.pack(pady=10)
        self.join_entry = tk.Entry(master, width=45)
        self.join_entry.pack(pady=5)
        self.join_button = tk.Button(master, text="Join Room", command=self.join_room, bg="blue",foreground="white", font=("Helvetica", 16))
        self.join_button.pack(pady=10)

        # Button for closing the room
        self.back_button = tk.Button(master, text="Close", command=self.close, bg="red",foreground="white", font=("Helvetica", 16))
        self.back_button.pack(pady=10)

    def create_room(self):
        # Get the room code from the entry field and process creating the room
        room_code = self.create_entry.get()
        print("Creating room with code:", room_code)
        # Add functionality to create a room using the provided room code

    def join_room(self):
        # Get the room code from the entry field and process joining the room
        room_code = self.join_entry.get()
        print("Joining room with code:", room_code)
        # Add functionality to join a room using the provided room code

    def close(self):
        # Functionality to go back
        self.master.destroy()
        subprocess.Popen(["python", "loginInterface.py"])
        
        print("Going back")
        # Implement the desired behavior for going back

def main():
    root = tk.Tk()
    login_interface = LoginInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
import subprocess
import random
import string
databasePath=r"database\chatDatabase.txt"

class LoginInterface:
    def __init__(self, master):
        self.master = master
        master.title("Create Or Join Into a room")
        master.geometry("400x400")
        master.configure(background="#EEF0E5")

        # Text entry for creating a room code
        self.create_label = tk.Label(master, text="Generate a Room Code :", font=("Arial",11))
        self.create_label.pack(pady=10)
        self.create_entry = tk.Label(master, text="Room Code", font=("Arial",15))
        self.create_entry.pack()
        self.join_label = tk.Label(master, text="Generate Room Password:",font=("Arial",11))
        self.join_label.pack(pady=10)
        self.join_entry = tk.Entry(master, width=10)
        self.join_entry.pack(pady=5)
        self.join_button = tk.Button(master, text="Confirm Room", command=self.putting_all_together, bg="blue",foreground="white", font=("Helvetica", 16))
        self.join_button.pack(pady=10)

        # Button for closing the room
        self.back_button = tk.Button(master, text="Close", command=self.close, bg="red",foreground="white", font=("Helvetica", 16))
        self.back_button.pack(pady=10)
        
    def create_database(self,key, value):
        with open(databasePath, "a") as file:
            file.write(f"{key}: {value}\n")
            print(f"Added {key}: {value} to the database file.")
        
    def generate_random_string(self,length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def create_room_code(self):
        random_string = self.generate_random_string(6)
        print("Creating room with code:", random_string)
        # self.create_entry.config(text=f"RoomID:{random_string}",bg="#FFFFEC",fg="#483838")
        return random_string
        
    def putting_all_together(self):
        room_id = self.create_room_code()
        password = self.join_entry.get()
        if len(password)==6:
            self.create_database(room_id, password)
            print("Success")
            self.join_entry.pack_forget()
            self.create_label.pack_forget()
            self.join_label.pack_forget()
            ID_level=tk.Label(self.master,text=f"Room_ID:{room_id}", bg="#FFFFEC", fg="#483838", font=("Helvetica", 14))
            ID_level.pack(pady=5)
            password_label = tk.Label(self.master, text=f"Password: {password}", bg="#FFFFEC", fg="#483838", font=("Helvetica", 14))
            password_label.pack(pady=5)
            # self.join_entry.config(text=f"Password:{password}", state="disabled", bg="#FFFFEC",fg="#483838", font=("Helvetica", 14))
            self.join_button.config(text="Room created successfully", state="disabled", bg="#FFFFEC",fg="#483838", font=("Helvetica", 14))
        else:
            print("password is not valid")
            
        
        
    
    def close(self):
        # Functionality to close child process
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

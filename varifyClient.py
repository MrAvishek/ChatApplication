import tkinter as tk
from tkinter import messagebox
import subprocess

databasePath = r"database\chatDatabase.txt"
def join_room():
    room_code = room_code_entry.get().strip()
    room_password = room_password_entry.get().strip()
    print("Entered Room Code:", room_code)
    print("Entered Room Password:", room_password)
    varifyPerson(room_code, room_password)

# def show_custom_message(title, message):
#     custom_window = tk.Toplevel(root)
#     custom_window.title(title)
#     message_label = tk.Label(custom_window, text=message, font=("Helvetica", 12))
#     message_label.pack(padx=20, pady=10)
#     ok_button = tk.Button(custom_window, text="OK", command=custom_window.destroy)
#     ok_button.pack(pady=5)

def varifyPerson(room_code,room_password):
    with open(databasePath, "r") as file:
        for line in file:
            stored_code, stored_password = line.strip().split(":")
            stored_code=stored_code.strip()
            stored_password=stored_password.strip()
            print("Checking:", stored_code, stored_password)
            if room_code == stored_code and room_password == stored_password:
                messagebox.showinfo("Room Found", "There we found a room for you!!!")
                # print("There we found a room for you!!!")
                root.destroy()
                subprocess.Popen(["python","client.py"])

                return
        messagebox.showerror("Room Not Found", "Try Creating a New Room")

root = tk.Tk()
root.title("Join Room")

# Labels
room_code_label = tk.Label(root, text="Enter your Room code:")
room_code_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

room_password_label = tk.Label(root, text="Enter room password:")
room_password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Entry boxes
room_code_entry = tk.Entry(root)
room_code_entry.grid(row=0, column=1, padx=10, pady=5)

room_password_entry = tk.Entry(root, show="*")
room_password_entry.grid(row=1, column=1, padx=10, pady=5)

# Join button
join_button = tk.Button(root, text="Join", bg="crimson", fg="white", command=join_room)
join_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

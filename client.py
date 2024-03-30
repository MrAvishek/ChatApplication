import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, PhotoImage

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#1FA8CF'
WHITE = "white"
FONT = ("Helvetica", 16,"bold")
BUTTON_FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)
ICON_FONT = ("Helvetica",22,"bold")
FILE_FONT = ("Helvetica",22,"bold")
EXIT_FONT= ("Helvetica", 20)
Impath = r"images\background.png"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message, is_server=False, sent_by_me=False):
    message_box.config(state=tk.NORMAL)
    if is_server:
        message_box.insert(tk.END, message, 'server')
    elif sent_by_me:
        message_box.insert(tk.END, message, 'sent_by_me')
    else:
        message_box.insert(tk.END, message, 'sent_by_others')
    message_box.insert(tk.END, '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    global username
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("💻: Successfully connected to the server", is_server=True)
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
        username_textbox.pack_forget()
        username_button.pack_forget()
        message_textbox.pack(side=tk.LEFT, padx=10, pady=10)
        message_button.pack(side=tk.LEFT, padx=10, pady=10)
        username_label.config(text=f"(◕‿◕) Welcome, {username}!")
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

def send_message(event=None):
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        add_message(f"✧{username}: {message}", sent_by_me=True)
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

def send_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            client.sendall(b'FILE:')
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                client.sendall(file_data)
            client.sendall(b'ENDFILE')
            add_message(f"File '{file_path}' sent successfully.")
    except FileNotFoundError:
        messagebox.showerror("File not found", "The selected file does not exist.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while sending the file: {str(e)}")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        send_file(file_path)

def exit_application():
    try:
        client.sendall('exit'.encode('ascii'))  
        print("exit message Sent")# Send exit message to the server
    except Exception as e:
        print(f"Error sending exit message to server: {e}")
        # traceback.print_exc()
    root.destroy()  


def handle_file_data(data):
    pass
    # Extract file name and content
    # file_data = data[len(b'FILE:'):]
    # file_content = file_data.split(b':', 1)[1]  # Split by the first colon to separate file name and content
    # file_name = file_data.split(b':', 1)[0].decode('utf-8')  # Decode file name from bytes to string

    # # Save the file to the local filesystem if the received data length matches the file content length
    # if len(file_content) == len(data) - len(b'FILE:') - len(file_name) - 1:  # Subtracting lengths of prefixes and separator
    #     save_file(file_name, file_content)
    #     add_message(f"File '{file_name}' saved successfully.")
    # else:
    #     add_message("Incomplete file received. Please try again.")

def save_file(file_name, file_content):
    file_path = filedialog.asksaveasfilename()
    if file_path:
        with open(file_path, 'wb') as file:
            file.write(file_content)
        add_message(f"File '{file_name}' saved successfully.")

def listen_for_messages_from_server(client):
    while True:
        data = client.recv(4096)
        if data:
            if data.startswith(b'FILE:'):
                handle_file_data(data)
            else:
                # Handle regular messages
                message = data.decode('utf-8')
                if ":" in message:
                    username, content = message.split(":", 1)
                    if username.strip() == "[SERVER]":
                        add_message(message, is_server=True)
                    else:
                        add_message(message, sent_by_me=(username.strip() == username))
                else:
                    add_message(message)
        else:
            messagebox.showerror("Error", "Message received from server is empty")

root = tk.Tk()
root.geometry("630x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg="#B0C5A4")
top_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=10)

middle_frame = tk.Frame(root, width=600, height=400, bg="#F8FCFB")
middle_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=10, pady=10)

bottom_frame = tk.Frame(root, width=600, height=100, bg="#E1EEFF")
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW, padx=10, pady=10)

username_label = tk.Label(top_frame, text="Enter your Name", font=FONT, bg="#B0C5A4", fg="#23120B")
username_label.pack(side=tk.LEFT, padx=6, pady=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg="#FEFBF6", fg="#000000", width=23)
username_textbox.pack(side=tk.LEFT, padx=10)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg="#4F6F52", fg="#FEFBF6",height=1, command=connect)
username_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(top_frame, text="🏃", font=EXIT_FONT, bg="#FA7070", fg="#000000", command=exit_application,height=1)
exit_button.pack(side=tk.RIGHT, padx=5, pady=10)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg="#B0C5A4", fg=WHITE, width=31)
message_button = tk.Button(bottom_frame, text="⏎", font=ICON_FONT, bg=OCEAN_BLUE, fg="#1D242B", command=send_message,width=5)
file_button = tk.Button(bottom_frame, text="📁", font=FILE_FONT, bg=OCEAN_BLUE, fg="#1D242B", command=select_file,width=1,padx=20)

message_textbox.bind("<Return>", send_message)
# Pack the buttons
file_button.pack(side=tk.LEFT, padx=5, pady=10)
message_button.pack(side=tk.LEFT, padx=5, pady=10)

# Load the background image
background_image = PhotoImage(file=Impath)

# Create a Canvas widget for the background
canvas = tk.Canvas(middle_frame, width=550, height=400, bg='white')
canvas.pack(expand=True, fill='both')

# Add the background image to the Canvas
canvas.create_image(0, 0, anchor='nw', image=background_image)

# Create the scrolled text box on top of the Canvas
message_box = scrolledtext.ScrolledText(canvas, font=SMALL_FONT, bg="#222831", fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP, padx=10, pady=10)

# scrolled text box expands with the Canvas
canvas.create_window(0, 0, anchor='nw', window=message_box)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()

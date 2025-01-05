from pathlib import Path
from tkinter import Canvas,Text, Entry, Button, PhotoImage,filedialog, scrolledtext
import tkinter as tk
import socket
import rsa
import os
import secrets
import threading
from utils.file_transfer_utils import compute_hash, rsa_encrypt  # Ensure these utilities are in file_transfer_utils.py


BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame3'

DEFAULT_PORT = 12345
FILE_CHUNK_SIZE = 64 * 1024  # Chunk size for file transfer
RSA_KEY_SIZE = 2048  # RSA key size
XOR_KEY_SIZE = 16  # XOR key size for encryption
PROGRESS_LOG_INTERVAL = 1024 * 1024  # Log progress


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class SendGUI:
    def __init__(self, root, call_backmenu):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Send")
        self.root.configure(bg="#316CEC")
        self.client_socket = None
        self.selected_file = None

        self.canvas = Canvas(
            self.root,
            bg="#316CEC",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.back_to_menu = call_backmenu  # Store the callback
        self.setup_ui()

    def setup_ui(self):
        # Background image
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(400.0, 300.0, image=self.image_image_1)

        self.bg_box = PhotoImage(file=relative_to_assets("bg_box.png"))
        self.canvas.create_image(400.0, 430.0, image=self.bg_box)

        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=13, width=65, state='disabled',bg='#EBEDF0', fg='black',bd=0, highlightthickness=0)
        self.log_area.place(x=130, y=318)  # Set the desired x and y coordinates


        # Input File Entry
        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.canvas.create_image(360.0, 272.0, image=self.entry_image_3)
        self.receiver_ip_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,font=("Montserrat", 10))
        self.receiver_ip_entry.place(x=214.0, y=135.0, width=298.0, height=26.0)

        # Key Entry
        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(285.0, 204.0, image=self.entry_image_2)
        self.port_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,font=("Montserrat", 10))
        self.port_entry.insert(0, str(DEFAULT_PORT))
        self.port_entry.place(x=211.0, y=191.0, width=110.0, height=26.0)

        # Output File Entry
        self.entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(413.0, 148.0, image=self.entry_image_1)


        # Connect Button
        self.connect_button = PhotoImage(file=relative_to_assets("connect_button.png"))
        button_4 = Button(image=self.connect_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.connect, relief="flat", bg="white")
        button_4.place(x=385.0, y=189.0, width=140.0, height=40.0)

        # Disconnect Button
        self.disconnect_button = PhotoImage(file=relative_to_assets("disconnect_button.png"))
        button_2 = Button(image=self.disconnect_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.disconnect, relief="flat", bg="white")
        button_2.place(x=526.0, y=189.0, width=140.0, height=40.0)

        # select Button
        self.select_button = PhotoImage(file=relative_to_assets("select_button.png"))
        button_3 = Button(image=self.select_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.select_file, relief="flat", bg="white")
        button_3.place(x=534.0, y=249.0, width=142.0, height=50.0)

        # Send Button ```python
        self.send_button = PhotoImage(file=relative_to_assets("send_button.png"))
        button_send = Button(image=self.send_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.send, relief="flat", bg="white")
        button_send.place(x=697.0, y=246.0, width=61.0, height=61.0)

        # Labels
        self.canvas.create_text(530, 139.0, anchor="nw", text="Receiver Ip", fill="#808080", font=("Montserrat Medium", 15 * -1))
        self.canvas.create_text(320, 195.0, anchor="nw", text="Port", fill="#808080", font=("Montserrat Medium", 15 * -1))
        self.canvas.create_text(500, 192.0, anchor="nw", text="Input File", fill="#808080", font=("Montserrat Medium", 15 * -1))

        self.file_label = tk.Label(self.root, text="No file selected.", bg="#FFFFFF", fg="black")
        self.file_label.place(x=214, y=260, width=250.0, height=22.0)  # Adjust the position as needed

        # Back Button to go back to gui_menu
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_back = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.back_to_Menu, relief="flat", bg="white")
        button_back.place(x=698.0, y=502.0, width=50.0, height=50.0)

        # Icons
        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(180.0, 145.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(180.0, 205.0, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(180.0, 271.0, image=self.image_image_5)

        self.canvas.create_text(300.0, 35.0, anchor="nw", text="Send a file", fill="#000000", font=("Montserrat Medium", 40 * -1))



    def connect(self):
        """Connects to the receiver."""
        def connect_to_receiver():
            receiver_ip = self.receiver_ip_entry.get()
            port = int(self.port_entry.get())
            try:
                self.client_socket = socket.socket()
                self.client_socket.connect((receiver_ip, port))
                self.log_message("Connected to receiver. Waiting for approval...")

                self.client_socket.send(b"Connection Request")
                approval = self.client_socket.recv(1024)
                if approval == b"Approved":
                    self.log_message("Connection approved by receiver.")
                else:
                    self.log_message("Connection denied by receiver.")
                    self.client_socket.close()
                    self.client_socket = None
            except Exception as e:
                self.log_message(f"Error connecting to receiver: {str(e)}")

        # Create and start a new thread for the connection process
        connection_thread = threading.Thread(target=connect_to_receiver)
        connection_thread.start()

    def disconnect(self):
        """Disconnects from the receiver."""
        if self.client_socket:
            try:
                self.client_socket.send(b"DISCONNECT")
                self.client_socket.close()
                self.client_socket = None
                self.log_message("Disconnected from the receiver.")
            except Exception as e:
                self.log_message(f"Error during disconnect: {str(e)}")


    def log_message(self, message):
        """Logs messages to the GUI."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)

    def select_file(self):
        """Handles file selection."""
        filename = filedialog.askopenfilename(title="Select a file to send")
        self.file_label.config(text=f"File Selected: {filename}" if filename else "No file selected.")


    def send(self):
        """Sends the selected file."""
        if not self.client_socket:
            self.log_message("You must connect to the receiver first.")
            return

        def send_file_thread(sock):
            file_path = self.file_label.cget("text").replace("File Selected: ", "")
            if not file_path or file_path == "No file selected.":
                self.log_message("No file selected.")
                return

            try:
                self.log_message("Sending file...")

                # Step 1: Receive Public Key from Receiver
                receiver_public_key = rsa.PublicKey.load_pkcs1(sock.recv(RSA_KEY_SIZE))

                # Step 2: Generate and Send XOR Key (Encrypted)
                xor_key = secrets.token_bytes(XOR_KEY_SIZE)  # Use XOR_KEY_SIZE constant
                sock.send(rsa_encrypt(xor_key, receiver_public_key))

                # Step 3: Encrypt and Send Metadata
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                file_hash = compute_hash(file_path)

                self.send_all(sock, rsa_encrypt(file_name.encode(), receiver_public_key))  # File name
                self.send_all(sock, rsa_encrypt(file_size.to_bytes(16, 'big'), receiver_public_key))  # File size
                self.send_all(sock, rsa_encrypt(file_hash.encode(), receiver_public_key))  # File hash

                # Step 4: Encrypt and Send File Data
                sent_bytes = 0
                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(FILE_CHUNK_SIZE)  # Use FILE_CHUNK_SIZE constant
                        if not data:
                            break
                        encrypted_data = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(data)])
                        self.send_all(sock, len(encrypted_data).to_bytes(4, 'big'))  # Send chunk length
                        self.send_all(sock, encrypted_data)  # Send encrypted chunk
                        sent_bytes += len(data)

                        # Log progress in the log area
                        if sent_bytes % PROGRESS_LOG_INTERVAL == 0:  # Every PROGRESS_LOG_INTERVAL bytes
                            progress_percentage = (sent_bytes / file_size) * 100
                            self.log_message(f"Progress: {progress_percentage:.2f}% ({sent_bytes}/{file_size} bytes)")

                self.log_message("File sent successfully.")
            except socket.timeout:
                self.log_message("Connection timed out. Check the receiver IP and try again.")
            except ConnectionRefusedError:
                self.log_message("Connection refused. Ensure the receiver is listening.")
            except Exception as e:
                self.log_message(f"Unexpected Error: {str(e)}")

        # Start the thread to send the file
        threading.Thread(target=send_file_thread, args=(self.client_socket,), daemon=True).start()

    def send_all(self, sock, data):
        """Ensures all data is sent over the socket."""
        total_sent = 0
        while total_sent < len(data):
            sent = sock.send(data[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent


    def back_to_Menu(self):
        # Call the callback function to go back to the menu
        self.back_to_menu()  # Ensure this calls the function

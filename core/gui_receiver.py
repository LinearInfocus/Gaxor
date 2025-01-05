from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, ttk, filedialog, scrolledtext, messagebox, Entry
import socket
import tkinter as tk
import rsa
import os
import threading
from utils.file_transfer_utils import compute_hash, rsa_decrypt  # Ensure these utilities are in file_transfer_utils.py

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame4'
DEFAULT_PORT = 12345
RSA_KEY_SIZE = 2048
CHUNK_SIZE = 64 * 1024

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ReceiverGUI:
    def __init__(self, root, call_backmenu):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Receiver")
        self.root.configure(bg="#316CEC")
        self.server_socket = None
        self.conn = None
        self.addr = None
        self.listening = True  # FLAG

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

        # LOGGING BOX
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=13, width=65, state='disabled',bg='#EBEDF0', fg='black',bd=0, highlightthickness=0)
        self.log_area.place(x=130, y=318)  # Set the desired x and y coordinates

        # Port Entry
        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(375.0, 148.0, image=self.entry_image_2)
        self.port_entry = Entry(
            self.root,
            width=15,
            bg="#FFFFFF",  # Menggunakan bg untuk tk.Entry
            fg="#000716",bd=0, highlightthickness=0,font=("Montserrat", 10)   # Menggunakan fg untuk tk.Entry
        )

        # Mengisi entry dengan nilai default
        self.port_entry.insert(0, str(DEFAULT_PORT))

        # Menempatkan entry di posisi yang diinginkan
        self.port_entry.place(x=298, y=137,width=110.0, height=20.0)

        # Connect Button
        self.start_button = PhotoImage(file=relative_to_assets("start_button.png"))
        button_4 = Button(image=self.start_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.start_receiver, relief="flat", bg="white")
        button_4.place(x=470.0, y=128.0, width=140.0, height=40.0)

        # Disconnect Button
        self.stop_button = PhotoImage(file=relative_to_assets("stop_button.png"))
        button_2 = Button(image=self.stop_button, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.stop, relief="flat", bg="white")
        button_2.place(x=470.0, y=189.0, width=140.0, height=40.0)

        # Labels
        self.canvas.create_text(415, 139.0, anchor="nw", text="Port", fill="#808080", font=("Montserrat Medium", 15 * -1))

        # Back Button to go back to gui_menu
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_back = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.back_to_menu, relief="flat", bg="white")
        button_back.place(x=698.0, y=502.0, width=50.0, height=50.0)

        # Icons
        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(270.0, 148.0, image=self.image_image_4)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(370.0, 245.0, image=self.image_image_3)

        self.canvas.create_text(285.0, 35.0, anchor="nw", text="Receive a file", fill="#000000", font=("Montserrat Medium", 40 * -1))

    def log_message(self, message):
        """Logs messages to the GUI."""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.config(state='disabled')
        self.log_area.see(tk.END)

    def start_receiver(self):
        """Starts the receiver in a separate thread."""
        self.listening = True  # Reset the listening flag

        def receiver_thread():
            while self.listening:  # Keep the server running until manually stopped
                try:
                    self.log_message("Server starting...")
                    self.log_message("Generating RSA keys...")
                    public_key, private_key = rsa.newkeys(RSA_KEY_SIZE)  # Using constant RSA_KEY_SIZE
                    self.log_message("RSA keys generated.")

                    # Set up server
                    host = "192.168.192.228"
                    port = int(self.port_entry.get() or DEFAULT_PORT)  # Using constant DEFAULT_PORT
                    self.server_socket = socket.socket()
                    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.server_socket.bind(("", port))
                    self.server_socket.listen(1)
                    self.log_message(f"Listening on {host} {port}...")

                    self.conn, self.addr = self.server_socket.accept()
                    self.log_message(f"Connection established with {self.addr}")

                    if not self.handle_connection_request():
                        continue  # Skip this connection and continue listening

                    # Send public key
                    self.conn.send(public_key.save_pkcs1())

                    # Receive XOR key and metadata
                    xor_key = rsa_decrypt(self.receive_exactly(256), private_key)
                    file_name = rsa_decrypt(self.receive_exactly(256), private_key).decode()
                    file_size = int.from_bytes(rsa_decrypt(self.receive_exactly(256), private_key), "big")
                    expected_file_hash = rsa_decrypt(self.receive_exactly(256), private_key).decode()

                    self.log_message(f"Receiving file: {file_name} ({file_size} bytes)")

                    save_path = self.ask_save_directory(file_name)
                    if not save_path:
                        continue  # If no directory selected, skip and continue listening

                    self.receive_file(save_path, xor_key, file_size, expected_file_hash)

                except Exception as e:
                    self.log_message(f"Error: {str(e)}")
                finally:
                    if self.conn:
                        self.conn.close()
                    if self.server_socket:
                        self.server_socket.close()
                    self.log_message("Server stopped.")

        threading.Thread(target=receiver_thread, daemon=True).start()

    def stop(self):
        """Stops the server and disconnects."""
        self.listening = False  # Stop the listening loop
        if self.conn:
            try:
                self.conn.send(b"STOP")  # Notify sender to stop
                self.conn.close()  # Close the client connection
                self.conn = None  # Reset to None for reuse
                self.log_message("Connection with client closed.")
            except Exception as e:
                self.log_message(f"Error sending STOP signal or closing connection: {str(e)}")
        if self.server_socket:
            try:
                self.server_socket.close()  # Close the server socket
                self.server_socket = None  # Reset to None for reuse
                self.log_message("Server stopped.")
            except Exception as e:
                self.log_message(f"Error stopping server: {str(e)}")

    def handle_connection_request(self):
        """Handles the connection request from the sender."""
        connection_request = self.conn.recv(1024)
        if connection_request == b"Connection Request":
            if messagebox.askyesno("Connection Request", f"Accept connection from {self.addr}?"):
                self.conn.send(b"Approved")
                self.log_message("Connection approved by user.")
                return True
            else:
                self.conn.send(b"Denied")
                self.log_message("Connection denied by user.")
        return False

    def receive_exactly(self, size):
        """Receives an exact number of bytes from the connection."""
        data = b""
        while len(data) < size:
            packet = self.conn.recv(size - len(data))
            if not packet:
                raise ConnectionError("Connection lost during data reception.")
            data += packet
        return data

    def ask_save_directory(self, file_name):
        """Asks the user to select a save directory."""
        save_directory = filedialog.askdirectory(title="Select Save Directory")
        if not save_directory:
            self.log_message("No directory selected. Exiting.")
            return None
        return os.path.join(save_directory, file_name)

    def receive_file(self, save_path, xor_key, file_size, expected_file_hash):
        """Receives the file data and decrypts it."""
        received_bytes = 0
        with open(save_path, "wb") as f:
            while received_bytes < file_size:
                # Receive chunk size
                chunk_size = int.from_bytes(self.receive_exactly(4), "big")
                # Receive encrypted chunk
                encrypted_data = self.receive_exactly(chunk_size)
                # Decrypt the chunk using the XOR key
                decrypted_data = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(encrypted_data)])
                # Write decrypted data to file
                f.write(decrypted_data)
                received_bytes += len(decrypted_data)

                if received_bytes % (1024 * 1024) == 0:
                    progress_percentage = (received_bytes / file_size) * 100
                    self.log_message(f"Progress: {progress_percentage:.2f}% ({received_bytes}/{file_size} bytes)")

        self.verify_file_integrity(save_path, expected_file_hash)
        # Log the message after the file has been saved
        self.log_message(f"File received and saved successfully at: {save_path}")

    def verify_file_integrity(self, file_path, expected_hash):
        """Verifies the file integrity using the hash."""
        received_file_hash = compute_hash(file_path)
        if received_file_hash == expected_hash:
            self.log_message("File integrity verified successfully.")
        else:
            self.log_message("File integrity check failed!")

    def back_to_menu(self):
        """Calls the callback function to go back to the menu."""
        self.back_to_menu()  # Ensure this calls the function

import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import re
import hashlib  # Untuk hashing password

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame1'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def create_database():
    conn = sqlite3.connect(BASE_DIR / "users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username VARCHAR(30) UNIQUE, "
        "password VARCHAR(250)"
        ")"
    )
    conn.commit()
    conn.close()

class RegisterGUI:
    def __init__(self, root, go_back_callback):
        self.window = root
        self.go_back_callback = go_back_callback
        self.window.geometry("800x600")
        self.window.title("Sign Up")
        self.window.configure(bg="#316CEC")

        create_database()  # Initialize the database

        self.canvas = Canvas(
            self.window,
            bg="#316CEC",
            height=600,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # UI elements remain unchanged
        self.setup_decorations()
        self.setup_entries()
        self.setup_buttons()

        # password decor
        self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(265.0, 290.0, image=self.image_5)
        # user decor
        self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(265.0, 234.0, image=self.image_3)

        self.window.resizable(False, False)

    def setup_decorations(self):
        # Add decorative images to canvas

        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(148.0, 230.0, image=self.image_2)

        self.image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
        self.canvas.create_image(400.0, 300.0, image=self.image_7)
        # decor
        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(700.0, 150.0, image=self.image_1)
        # kaka headset
        self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(270.0, 430.0, image=self.image_4)

    def setup_entries(self):
        # Setup username and password entry fields
        self.entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
        self.canvas.create_image(403.0, 230.0, image=self.entry_image_3)
        self.entry_3 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_3.place(x=280.0, y=218.2, width=260.0, height=25.2)

        self.entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(385.0, 290.0, image=self.entry_image_2)
        self.entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.entry_2.place(x=280.0, y=278.2, width=230.0, height=25.2)

        # Show/Hide password functionality
        self.setup_show_password()

    def setup_show_password(self):
        show_password_button_image = PhotoImage(file=relative_to_assets("show_password_button.png"))
        hide_password_button_image = PhotoImage(file=relative_to_assets("hide_password_button.png"))
        self.password_button = Button(
            image=show_password_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.toggle_password(show_password_button_image, hide_password_button_image),
            relief="flat",
            bg="white"
        )
        self.password_button.image = show_password_button_image
        self.password_button.place(x=525.0, y=280.0, width=24.0, height=24.0)

    def setup_buttons(self):
        # Sign Up Button
        self.canvas.create_text(348.0, 125.0, anchor="nw", text="Sign Up", fill="#000000", font=("Montserrat Medium", 24 * -1))
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            activebackground = "white",
            command=self.register_user,
            relief="flat",
            bg="white"
        )
        self.button_1.place(x=328.0, y=355.0, width=142.75, height=32.76)

        # Back Button to gui_login.py
        self.back_image = PhotoImage(file=relative_to_assets("button_2.png"))  # Load back button image
        self.back_button = Button(image=self.back_image, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.go_back_callback, relief="flat", bg="white")
        self.back_button.place(x=540.0, y=435.0, width=50.0, height=50.0)

    def toggle_password(self, show_image, hide_image):
        if self.entry_2['show'] == '*':
            self.entry_2['show'] = ''
            self.password_button.config(image=hide_image)
        else:
            self.entry_2['show'] = '*'
            self.password_button.config(image=show_image)

    def register_user(self):
        username = self.entry_3.get()
        password = self.entry_2.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

        if len(password) < 8:
            messagebox.showwarning("Input Error", "Password must be at least 8 characters long.")
            return

        # Check if password contains a special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showwarning("Input Error", "Password must contain at least one special character.")
            return

        # Check if password contains at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            messagebox.showwarning("Input Error", "Password must contain at least one uppercase letter.")
            return

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = sqlite3.connect(BASE_DIR / "users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.go_back_callback()  # Go back to login screen
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists. Please choose a different one.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

#END

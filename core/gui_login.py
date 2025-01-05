import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
import hashlib  # Untuk hashing password

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame0'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LoginGUI:
    def __init__(self, window, show_register_callback, show_menu_callback):
        self.window = window
        self.show_register_callback = show_register_callback
        self.show_menu_callback = show_menu_callback  # Store the callback

        self.initialize_database()
        self.setup_ui()

    def initialize_database(self):
        try:
            conn = sqlite3.connect(BASE_DIR / "users.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(30) PRIMARY KEY,
                    password VARCHAR(250) NOT NULL
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

            
    def validate_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Both fields are required.")
            return

        # Hash the entered password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(BASE_DIR / "users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.show_menu_callback()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def go_register(self):
        """Switch to the registration screen."""
        self.show_register_callback()

    def setup_ui(self):
        """Setup UI components like Canvas, buttons, and entry fields."""

        self.canvas = Canvas(self.window, bg="#316CEC", height=600, width=800, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Add the UI elements
        self.setup_decorations()
        self.setup_inputs_and_buttons()

        # Set window properties
        self.window.resizable(False, False)

    def setup_decorations(self):
        """Store the images as attributes to prevent garbage collection."""
        self.image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(490.0, 79.0, image=self.image_1)


        self.image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(213.0, 310.0, image=self.image_4)

        # Floating plane for entry, sign in button
        self.image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(600.0, 310.0, image=self.image_5)

        # User image for username decor
        self.image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(493.0, 258.0, image=self.image_2)

        # Key Image for Password
        self.image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(493.0, 303.0, image=self.image_3)

        self.canvas.create_text(558.0, 191.0, anchor="nw", text="Sign In", fill="#000000", font=("Montserrat Medium", 24 * -1))

    def setup_inputs_and_buttons(self):
        """Setup the input fields and buttons for login."""
        # Username Entry
        self.entry_bg_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(610.0, 260.0, image=self.entry_bg_1)
        self.entry_username = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_username.place(x=520.0, y=250.0, width=184.0, height=20.0)

        # Password Entry
        self.entry_bg_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(602.0, 304.0, image=self.entry_bg_2)
        self.entry_password = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, show="*")
        self.entry_password.place(x=520.0, y=294.0, width=165.0, height=20.0)

        # LOGIN button - placed after the rounded image (image_5)
        button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_image_1 = button_image_1
        self.sign_in_button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            activebackground = "white",
            command=self.validate_login,  # Call the SQLite validation function
            relief="flat"
        )
        self.sign_in_button_1.place(x=555.0, y=342.0, width=96.0, height=24.0)

        # Show password functionality
        show_password_button_image = PhotoImage(file=relative_to_assets("show_password_button.png"))
        hide_password_button_image = PhotoImage(file=relative_to_assets("hide_password_button.png"))
        self.password_button = Button(
            image=show_password_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.toggle_password(show_password_button_image, hide_password_button_image),
            relief="flat",
            bg='white'
        )
        self.password_button.image = show_password_button_image
        self.password_button.place(x=700.0, y=297.0, width=15.0, height=15.0)

        # Sign Up Label
        self.canvas.create_text(515.0, 378.0, anchor="nw", text="Don’t have an account? ", fill="#000000", font=("Montserrat Medium", 10 * -1))
        self.sign_up_label = Label(self.window, text="Sign Up", fg="#2196F3", cursor="hand2", bg="#FFFFFF", font=("Montserrat", 10 * -1, "underline"))
        self.sign_up_label.place(x=640.0, y=374.5)
        self.sign_up_label.bind("<Button-1>", lambda e: self.go_register())

    def toggle_password(self, show_image, hide_image):
        """Toggle the visibility of the password."""
        if self.entry_password['show'] == '*':
            self.entry_password['show'] = ''
            self.password_button.config(image=hide_image)
        else:
            self.entry_password['show'] = '*'
            self.password_button.config(image=show_image)

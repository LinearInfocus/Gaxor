from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,messagebox

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame5'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class AboutGui:
    def __init__(self, root, next_to_menu):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Menu")
        self.root.configure(bg="#316CEC")

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

        
        self.next_to_menu = next_to_menu
        self.setup_ui()

    def setup_ui(self):
        # Load and display images
        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(400.0, 300.0, image=self.image_image_3)

        # Button to "receiver" Window
        self.button_image_2_normal = PhotoImage(file=relative_to_assets("button_2_normal.png"))  # 70% opacity image
        self.button_image_2_hover = PhotoImage(file=relative_to_assets("button_2_hover.png"))    # 100% opacity image
        self.button_2 = Button(image=self.button_image_2_normal, borderwidth=0, highlightthickness=0, command=self.virrel, relief="flat")
        self.button_2.place(x=145.0, y=125.0, width=150, height=300)
        self.button_2.bind("<Enter>", lambda e: self.button_2.config(image=self.button_image_2_hover))
        self.button_2.bind("<Leave>", lambda e: self.button_2.config(image=self.button_image_2_normal))

        # Button to "sender" Window
        self.button_image_4_normal = PhotoImage(file=relative_to_assets("button_4_normal.png"))  # 70% opacity image
        self.button_image_4_hover = PhotoImage(file=relative_to_assets("button_4_hover.png"))    # 100% opacity image
        self.button_4 = Button(image=self.button_image_4_normal, borderwidth=0, highlightthickness=0, command=self.helen, relief="flat")
        self.button_4.place(x=510.0, y=125.0, width=150, height=300)
        self.button_4.bind("<Enter>", lambda e: self.button_4.config(image=self.button_image_4_hover))
        self.button_4.bind("<Leave>", lambda e: self.button_4.config(image=self.button_image_4_normal))

        # Button to "sender" Window (duplicate, consider removing)
        self.button_image_3_normal = PhotoImage(file=relative_to_assets("button_3_normal.png"))  # 70% opacity image
        self.button_image_3_hover = PhotoImage(file=relative_to_assets("button_3_hover.png"))    # 100% opacity image
        self.button_3 = Button(image=self.button_image_3_normal, borderwidth=0, highlightthickness=0, command=self.Bintang, relief="flat")
        self.button_3.place(x=325.0, y=115.0, width=160.0, height=310)
        self.button_3.bind("<Enter>", lambda e: self.button_3.config(image=self.button_image_3_hover))
        self.button_3.bind("<Leave>", lambda e: self.button_3.config(image=self.button_image_3_normal))

        # Decoration images
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(400.0, 60.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(400.0, 480.0, image=self.image_image_2)

        # Back button
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.next_to, relief="flat", bg="white")
        button_1.place(x=620.0, y=500.0, width=150.0, height=50.0)

    def Bintang(self):
        """Navigate to the send window."""
        messagebox.showinfo("Infokan", "Ketua Awak Nih")

    def helen(self):
        messagebox.showinfo("Info", "Kang Program")

    def virrel(self):
        """Navigate to the receiver window."""
        messagebox.showinfo("Info", "Kang Designer")

    def next_to(self):
        """Go back to the login screen."""
        self.next_to_menu()


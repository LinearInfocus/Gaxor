from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

BASE_DIR = Path(__file__).resolve().parent
ASSETS_PATH = BASE_DIR / 'assets' / 'frame2'

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MenuGui:
    def __init__(self, root, sign_out_callback, send_callback, receiver_callback, go_to_about):
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

        self.go_to_about = go_to_about
        self.receiver_callback = receiver_callback  # Corrected variable name
        self.send_callback = send_callback
        self.sign_out_callback = sign_out_callback
        self.setup_ui()

    def setup_ui(self):
        # Load and display images
        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.canvas.create_image(400.0, 300.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.canvas.create_image(230.0, 290.0, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.canvas.create_image(570.0, 290.0, image=self.image_image_5)

        # Button to "receiver" Window
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.receive, relief="flat")
        button_2.place(x=510.0, y=370.0, width=130.0, height=48.51)

        # Button to "sender" Window
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.send, relief="flat")
        button_1.place(x=167.0, y=370.0, width=130.0, height=48.51)

        # Menu Title/Header
        self.canvas.create_text(330.0, 60.0, anchor="nw", text="Choose ", fill="#000000", font=("Montserrat Medium", 38 * -1))

        # Decoration images
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.canvas.create_image(400.0, 540.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.canvas.create_image(230.0, 250.0, image=self.image_image_2)

        self.image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
        self.canvas.create_image(570.0, 250.0, image=self.image_image_6)

        # Back button
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.sign_out, relief="flat", bg="white")
        button_3.place(x=600, y=502.0, width=150.0, height=50.0)

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, activebackground = "white", command=self.about, relief="flat", bg="white")
        button_4.place(x=50.0, y=502.0, width=150.0, height=50.0)



    def about(self):
        
        self.go_to_about()

    def send(self):
        """Navigate to the send window."""
        self.send_callback()  # Call the send callback

    def receive(self):
        """Navigate to the receiver window."""
        self.receiver_callback()  # Corrected method name

    def sign_out(self):
        """Go back to the login screen."""
        self.sign_out_callback()


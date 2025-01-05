# main.py
import tkinter as tk
from core.gui_login import LoginGUI
from core.gui_register import RegisterGUI
from core.gui_menu import MenuGui
from core.gui_sender import SendGUI  # Import MenuGUI for navigation
from core.gui_receiver import ReceiverGUI
from core.gui_About_Us import AboutGui

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Navigation")
        self.root.geometry("800x600")
        self.root.configure(bg="#316CEC")
        self.show_login()

    def show_login(self):
        """Display the login window."""
        self.clear_window()
        LoginGUI(self.root, self.show_register, self.show_menu)  # Pass show_menu1 as the callback

    def show_register(self):
        """Display the register window."""
        self.clear_window()
        RegisterGUI(self.root, self.show_login)

    def show_about(self):
        """Display the register window."""
        self.clear_window()
        AboutGui(self.root, self.show_menu)

    def show_menu(self):
        """Display the main menu after a successful login."""
        self.clear_window()
        MenuGui(self.root, self.show_login, self.show_send, self.show_reciever,self.show_about)

    def show_send(self):
        """Display the register window."""
        self.clear_window()
        SendGUI(self.root, self.show_menu)

    def show_reciever(self):
        self.clear_window
        ReceiverGUI(self.root, self.show_menu)



    def clear_window(self):
        """Clear the current content of the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()

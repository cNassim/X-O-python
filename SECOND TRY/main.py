import tkinter as tk
import customtkinter as ctk
from ui_pages import TicTacToePages

if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToePages(root)
    root.mainloop()
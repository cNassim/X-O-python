import customtkinter as ctk
from tkinter import messagebox
import random
from game_logic import TicTacToeLogic
from utils import Utils

class TicTacToePages(TicTacToeLogic, Utils):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x400")
        self.root.wm_attributes("-fullscreen", True)

        self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme)

        self.welcome_page()

    def welcome_page(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", anchor="center")

        # UI Elements
        welcome_label = ctk.CTkLabel(
            frame, 
            text="Welcome to Tic Tac Toe!", 
            font=("Arial", 36, "bold"), 
            text_color="white",
            fg_color="Gray",
            corner_radius=5
        )
        welcome_label.pack(pady=(175, 10))

        mode_label = ctk.CTkLabel(frame, text="Select Game Mode:")
        mode_label.pack(pady=(10, 5))

        self.mode_var = ctk.StringVar(value="Classique")
        mode_menu = ctk.CTkOptionMenu(frame, variable=self.mode_var, values=["Classique", "Case grise","Non aligné"])
        mode_menu.pack(pady=(5, 10))

        play_button = ctk.CTkButton(frame, text="Play", command=self.settings_page)
        play_button.pack(pady=(10, 5))

        options_button = ctk.CTkButton(frame, text="Options", command=self.options_page)
        options_button.pack(pady=(5, 5))

        quit_button = ctk.CTkButton(frame, text="Quit", command=self.confirm_exit)
        quit_button.pack(pady=(5, 20))

        footer_label = ctk.CTkLabel(
            self.root,
            text="Made with heart ❤ by Nassim",
            font=("Arial", 10, "italic"),
            text_color="gray",
            fg_color="transparent"
        )
        footer_label.pack(side="bottom", pady=10)

    def settings_page(self):
        self.clear_frame()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both")

        title_label = ctk.CTkLabel(frame, text="Game Settings", font=("Arial", 20))
        title_label.pack(pady=(40, 10))

        grid_label = ctk.CTkLabel(frame, text="Grid Size (NxM):")
        grid_label.pack()

        self.rows_var = ctk.IntVar(value=3)
        self.cols_var = ctk.IntVar(value=3)

        grid_frame = ctk.CTkFrame(frame)
        grid_frame.pack()
    
        rows_entry = ctk.CTkEntry(grid_frame, textvariable=self.rows_var, width=50)
        rows_entry.pack(side="left", padx=5)
        cols_entry = ctk.CTkEntry(grid_frame, textvariable=self.cols_var, width=50)
        cols_entry.pack(side="left", padx=5)


        Win_label = ctk.CTkLabel(frame, text="To win you need to align :")
        Win_label.pack(pady=5)

        self.Win_var = ctk.StringVar(value="Par defaut")
        self.Win_menu= ctk.CTkOptionMenu(frame, variable=self.Win_var, values=[""])
        self.Win_menu.pack()
        self.Win_var.trace("w", self.update_Win_options)
        self.update_Win_options()

        self.rows_var.trace("w", self.update_Win_options)
        self.cols_var.trace("w", self.update_Win_options)
        self.update_Win_options()

        difficulty_label = ctk.CTkLabel(frame, text="Difficulty:")
        difficulty_label.pack(pady=5)

        self.difficulty_var = ctk.StringVar(value="Easy")
        difficulty_menu = ctk.CTkOptionMenu(frame, variable=self.difficulty_var, values=["Easy", "Hard"])
        difficulty_menu.pack()

        color_label = ctk.CTkLabel(frame, text="Player Color:")
        color_label.pack(pady=5)

        self.color_var = ctk.StringVar(value="Red")
        self.color_menu = ctk.CTkOptionMenu(frame, variable=self.color_var, values=["Red", "Blue", "Green", "Yellow"])
        self.color_menu.pack()

        ai_color_label = ctk.CTkLabel(frame, text="AI Color:")
        ai_color_label.pack(pady=5)

        self.ai_color_var = ctk.StringVar(value="Green")
        self.ai_color_menu = ctk.CTkOptionMenu(frame, variable=self.ai_color_var, values=["Red", "Blue", "Green", "Yellow"])
        self.ai_color_menu.pack()

        self.color_var.trace("w", self.update_color_options)
        self.ai_color_var.trace("w", self.update_color_options)
        self.update_color_options()

        first_player_label = ctk.CTkLabel(frame, text="Who Starts:")
        first_player_label.pack(pady=5)

        self.first_player_var = ctk.StringVar(value="Player")
        self.first_player_menu = ctk.CTkOptionMenu(frame, variable=self.first_player_var, values=["Player", "AI"])

        if self.mode_var.get() == "Case grise" or self.mode_var.get() == "Non aligné":
            self.first_player_menu.pack()
            gray_mode_label = ctk.CTkLabel(frame, text="Gray Mode Configuration:")
            gray_mode_label.pack(pady=(0, 10))

            self.gray_mode_var = ctk.StringVar(value="Randomisé")
            gray_mode_menu = ctk.CTkOptionMenu(frame, variable=self.gray_mode_var, values=["Randomisé", "Pyramide"])
            gray_mode_menu.pack(pady=10)

            self.pyramid_position_var = ctk.StringVar(value="En haut")
            pyramid_position_menu = ctk.CTkOptionMenu(
                frame, variable=self.pyramid_position_var,
                values=["En haut", "En bas", "À gauche", "À droite"]
            )
            pyramid_position_menu.pack(pady=10)

            gray_count_label = ctk.CTkLabel(frame, text="Number of Gray Cells:")
            gray_count_label.pack(pady=5)

            self.gray_count_var = ctk.IntVar(value=0)
            gray_count_entry = ctk.CTkEntry(frame, textvariable=self.gray_count_var, width=100)
            gray_count_entry.pack(pady=5)

            def update_gray_options(*args):
                if self.gray_mode_var.get() == "Pyramide":
                    pyramid_position_menu.configure(state="normal")
                    gray_count_entry.configure(state="disabled")
                elif self.gray_mode_var.get() == "Randomisé":
                    pyramid_position_menu.configure(state="disabled")
                    gray_count_entry.configure(state="normal")

            self.gray_mode_var.trace("w", update_gray_options)
            update_gray_options()
        else:
            self.first_player_menu.pack(pady=(0, 170))

        start_button = ctk.CTkButton(frame, text="Start Game", command=self.start_game)
        start_button.pack(pady=3)

        back_button = ctk.CTkButton(frame, text="Back", command=self.welcome_page)
        back_button.pack(pady=3)

        quit_button = ctk.CTkButton(frame, text="Quit", command=self.confirm_exit)
        quit_button.pack(pady=3)

    def options_page(self):
        self.clear_frame()

        # Create a frame for the settings page
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", anchor="center")

        # Settings title
        settings_label = ctk.CTkLabel(
            frame,
            text="Settings",
            font=("Arial", 36, "bold"),
            text_color="white",
            fg_color="Gray",
            corner_radius=5
        )
        settings_label.pack(pady=(50, 20))

        # Theme toggle button
        theme_button = ctk.CTkButton(
            frame,
            text="Dark Mode: OFF" if ctk.get_appearance_mode() == "Light" else "Dark Mode: ON",
            command=lambda: self.update_theme_button(theme_button)
        )
        theme_button.pack(pady=(20, 10))

        # Fullscreen toggle button
        fullscreen_button = ctk.CTkButton(
            frame,
            text="Fullscreen: OFF" if not self.root.attributes('-fullscreen') else "Fullscreen: ON",
            command=lambda: self.toggle_fullscreen(fullscreen_button)
        )
        fullscreen_button.pack(pady=(10, 20))

        # Back button to return to the welcome page
        back_button = ctk.CTkButton(
            frame,
            text="Back",
            command=self.welcome_page
        )
        back_button.pack(pady=(20, 10))


    def game_page(self, rows, cols):
        self.clear_frame()

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both")

        title_label = ctk.CTkLabel(frame, text=f"Tic Tac Toe {rows}x{cols} - {self.game_mode}", font=("Arial", 20))
        title_label.pack(pady=10)

        grid_frame = ctk.CTkFrame(frame, fg_color="white")
        grid_frame.pack(expand=True)

        self.grid = []
        total_cells = rows * cols

        gray_cells = []  # Liste des cases grises à désactiver

        if self.game_mode == "Case grise" or self.game_mode == "Non aligné":
            if self.gray_mode_var.get() == "Randomisé":
                gray_cells = random.sample(range(total_cells), self.gray_count_var.get())
            elif self.gray_mode_var.get() == "Pyramide":
                pyramid_position = self.pyramid_position_var.get()
                gray_cells = self.generate_pyramid_cells(rows, cols, pyramid_position)

        # Création de la grille avec cases grises ou normales
        for r in range(rows):
            row = []
            for c in range(cols):
                index = r * cols + c
                if index in gray_cells:
                    # Case grise
                    cell = ctk.CTkButton(
                        grid_frame, text="", width=40, height=40, fg_color="white",
                        corner_radius=0, state="disabled"
                    )
                else:
                    # Case normale
                    cell = ctk.CTkButton(
                        grid_frame, text="", width=40, height=40, fg_color="gray",
                        corner_radius=0, command=lambda x=r, y=c: self.make_move(x, y)
                    )
                cell.grid(row=r, column=c, padx=2, pady=2)
                row.append(cell)
            self.grid.append(row)

        undo_button = ctk.CTkButton(frame, text="Undo Move", command=self.undo_move)
        undo_button.pack(pady=0)

        redo_button = ctk.CTkButton(frame, text="Redo Move", command=self.redo_move)
        redo_button.pack(pady=10)

        back_button = ctk.CTkButton(frame, text="Back to Settings", command=self.settings_page)
        back_button.pack()
        self.current_player = self.player_color if self.first_player_var.get() == "Player" else self.ai_color
        
        quit_button = ctk.CTkButton(frame, text="Quit", command=self.confirm_exit)
        quit_button.pack(pady=10)
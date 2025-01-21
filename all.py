import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random

class Utils:
    def toggle_theme(self):
        # Basculer entre les thèmes
        if self.current_theme == "dark":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme)

    def toggle_fullscreen(self, button):
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        button.configure(text="Fullscreen: ON" if not is_fullscreen else "Fullscreen: OFF")

    def update_theme_button(self, button):
        from customtkinter import get_appearance_mode, set_appearance_mode
        if get_appearance_mode() == "Dark":
            set_appearance_mode("Light")
            button.configure(text="Dark Mode: OFF")
        else:
            set_appearance_mode("Dark")
            button.configure(text="Dark Mode: ON")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to quit the game?"):
            self.root.destroy()

    def update_color_options(self, *args):
        # Obtenir les couleurs sélectionnées
        selected_player_color = self.color_var.get()
        selected_ai_color = self.ai_color_var.get()

        # Liste des couleurs possibles
        all_colors = ["Red", "Blue", "Green", "Yellow"]

        # Options disponibles pour le joueur et l'IA
        player_options = [color for color in all_colors if color != selected_ai_color]
        ai_options = [color for color in all_colors if color != selected_player_color]

        # Mettre à jour les menus déroulants
        self.color_menu.configure(values=player_options)
        self.ai_color_menu.configure(values=ai_options)

        # Assurer que les couleurs sélectionnées sont valides
        if selected_player_color not in player_options:
            self.color_var.set(player_options[0])
        if selected_ai_color not in ai_options:
            self.ai_color_var.set(ai_options[0])

    def get_empty_cells(self):
        empty_cells = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell.cget("fg_color") == "gray":  # Case non jouée
                    empty_cells.append((r, c))
        return empty_cells

    def generate_pyramid_cells(self, rows, cols, position):
        pyramid_cells = []
        if position == "En haut":
            for i in range(rows):
                for j in range(i, cols - i):
                    pyramid_cells.append(i * cols + j)
        elif position == "En bas":
            for i in range(rows):
                for j in range(i, cols - i):
                    pyramid_cells.append((rows - 1 - i) * cols + j)
        elif position == "À gauche":
            for j in range(cols):
                for i in range(j, rows - j):
                    pyramid_cells.append(i * cols + j)
        elif position == "À droite":
            for j in range(cols):
                for i in range(j, rows - j):
                    pyramid_cells.append(i * cols + (cols - 1 - j))
        return pyramid_cells

class TicTacToeLogic:
    def __init__(self, root):
        self.root = root
        self.grid = []
        self.current_player = "Red"
        self.player_color = "Red"
        self.ai_color = "Green"
        self.move_stack = []
        self.redo_stack = []

    def start_game(self):
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        if rows < 3 or cols < 3 or rows > 7 or cols > 7:
            messagebox.showerror("Invalid Grid Size", "Grid size must be between 3x3 and 7x7.")
            return

        self.difficulty = self.difficulty_var.get()
        self.player_color = self.color_var.get()
        self.ai_color = self.ai_color_var.get()
        self.current_player = self.player_color if self.first_player_var.get() == "Player" else self.ai_color
        self.game_mode = self.mode_var.get()

        if self.difficulty == "Hard":
            if rows * cols <= 9:  # Grille 3x3
                self.ai_depth = 5
            else:  # Grille > 3x3
                self.ai_depth = 1
        else:  # Difficulté "Easy"
            if rows * cols <= 9:  # Grille 3x3
                self.ai_depth = 4
            else:  # Grille > 3x3
                self.ai_depth = 0

        if self.game_mode == "Case grise" and self.gray_mode_var.get() == "Randomisé":
            total_cells = rows * cols
            if self.gray_count_var.get() > total_cells:
                messagebox.showerror("Invalid Gray Cell Count", "The number of gray cells exceeds the total cells available.")
                return

        self.move_stack = []  # Réinitialiser l'historique des coups
        self.redo_stack = []  # Réinitialiser l'historique des coups annulés
        self.game_page(rows, cols)
        if self.first_player_var.get() == "AI":
            ai_move = self.find_best_move()
            if ai_move:
                self.make_move(*ai_move)

    def make_move(self, row, col):
        cell = self.grid[row][col]
        if cell.cget("text") == "":
            cell.configure(fg_color=self.current_player, state="disabled")
            self.move_stack.append((row, col, self.current_player))
            self.redo_stack.clear()

            # Check for game outcomes
            if self.game_mode == "Non aligné":
                if self.check_winner_by_color(self.ai_color):
                    messagebox.showinfo("Game Over", "You win in Non-aligned mode!")
                    self.settings_page()
                    return
                elif self.check_winner_by_color(self.player_color):
                    messagebox.showinfo("Game Over", "AI wins in Non-aligned mode!")
                    self.settings_page()
                    return
                elif self.check_draw():
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.settings_page()
                    return
            else:
                if self.check_winner_by_color(self.ai_color):
                    messagebox.showinfo("Game Over", "AI wins!")
                    self.settings_page()
                    return
                elif self.check_winner_by_color(self.player_color):
                    messagebox.showinfo("Good game", "You win!")
                    self.settings_page()
                    return
                elif self.check_draw():
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.settings_page()
                    return

            self.current_player = self.ai_color if self.current_player == self.player_color else self.player_color
            if self.current_player == self.ai_color:
                ai_move = self.find_best_move()
                if ai_move:
                    self.make_move(*ai_move)

    def minimax(self, is_ai_turn, depth):
        if self.game_mode == "Non aligné":
            if self.check_winner_by_color(self.ai_color):
                return -10  # L'IA perd si elle aligne trois cases
            elif self.check_winner_by_color(self.player_color):
                return 10  # Le joueur perd s'il aligne trois cases
        else:
            if self.check_winner_by_color(self.ai_color):
                return 10  # L'IA gagne en mode normal
            elif self.check_winner_by_color(self.player_color):
                return -10  # Le joueur gagne en mode normal
        
        if self.check_draw() or depth == 0:
            return self.evaluate_board()  # Égalité ou profondeur atteinte

        empty_cells = self.get_empty_cells()

        if is_ai_turn:
            best_score = float("-inf")
            for (r, c) in empty_cells:
                self.grid[r][c].configure(fg_color=self.ai_color)
                score = self.minimax(False, depth - 1)
                self.grid[r][c].configure(fg_color="gray")
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for (r, c) in empty_cells:
                self.grid[r][c].configure(fg_color=self.player_color)
                score = self.minimax(True, depth - 1)
                self.grid[r][c].configure(fg_color="gray")
                best_score = min(best_score, score)
            return best_score

    def evaluate_board(self):
        rows, cols = len(self.grid), len(self.grid[0])

        def check_line(line):
            if self.game_mode == "Non aligné":
                if all(cell.cget("fg_color") == self.ai_color for cell in line):
                    return -10  # L'IA perd si elle aligne trois cases
                elif all(cell.cget("fg_color") == self.player_color for cell in line):
                    return 10  # Le joueur perd s'il aligne trois cases
            else:
                if all(cell.cget("fg_color") == self.ai_color for cell in line):
                    return 10  # L'IA gagne en mode normal
                elif all(cell.cget("fg_color") == self.player_color for cell in line):
                    return -10  # Le joueur gagne en mode normal
            return 0

        score = 0

        # Vérifier les lignes
        for row in self.grid:
            score += check_line(row)

        # Vérifier les colonnes
        for col in range(cols):
            score += check_line([self.grid[row][col] for row in range(rows)])

        # Vérifier les diagonales
        score += check_line([self.grid[i][i] for i in range(min(rows, cols))])
        score += check_line([self.grid[i][cols - 1 - i] for i in range(min(rows, cols))])

        return score
    
    def find_best_move(self):
        best_score = float("-inf")
        best_move = None
        empty_cells = self.get_empty_cells()
        for (r, c) in empty_cells:
            self.grid[r][c].configure(fg_color=self.ai_color)
            score = self.minimax(False, depth=self.ai_depth)
            self.grid[r][c].configure(fg_color="gray")
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    def check_winner_by_color(self, color):
        rows, cols = len(self.grid), len(self.grid[0])
        for r in range(rows):
            if all(self.grid[r][c].cget("fg_color") == color for c in range(cols)):
                return True
        for c in range(cols):
            if all(self.grid[r][c].cget("fg_color") == color for r in range(rows)):
                return True
        if all(self.grid[i][i].cget("fg_color") == color for i in range(rows)):
            return True
        if all(self.grid[i][cols - 1 - i].cget("fg_color") == color for i in range(rows)):
            return True
        return False

    def check_draw(self):
        for row in self.grid:
            for cell in row:
                if cell.cget("fg_color") == "gray":  # Une case grise indique qu'elle n'a pas été jouée
                    return False
        return True

    def undo_move(self):
        if len(self.move_stack) < 2:
            messagebox.showinfo("Undo", "Not enough moves to undo!")
            return

        for _ in range(2):  # Supprimer deux derniers coups
            row, col, color = self.move_stack.pop()
            self.redo_stack.append((row, col, color))  # Ajouter à redo_stack
            cell = self.grid[row][col]
            cell.configure(fg_color="gray", state="normal")

        self.current_player = self.player_color

    def redo_move(self):
        if len(self.redo_stack) < 2:
            messagebox.showinfo("Redo", "Not enough moves to redo!")
            return

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
        title_label.pack(pady=(100, 10))

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

        if self.mode_var.get() == "Case grise":
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

        if self.game_mode == "Case grise":
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

if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToePages(root)
    root.mainloop()
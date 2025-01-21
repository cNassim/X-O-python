import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x400")
        self.root.wm_attributes("-fullscreen", True)

        # Initialiser le thème
        self.current_theme = "dark"  # Mode sombre par défaut
        ctk.set_appearance_mode(self.current_theme)


        self.grid = []
        self.current_player = "Red"
        self.player_color = "Red"
        self.ai_color = "Green"
        self.move_stack = []  # Historique des coups (joueur + IA)
        self.redo_stack = []  # Historique des coups annulés

        self.welcome_page()

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
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            button.configure(text="Dark Mode: OFF")
        else:
            ctk.set_appearance_mode("Dark")
            button.configure(text="Dark Mode: ON")

    def welcome_page(self):
        self.clear_frame()

        # Créer un frame pour la page de bienvenue
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", anchor="center")

        # Label de bienvenue avec décoration
        welcome_label = ctk.CTkLabel(
            frame, 
            text="Welcome to Tic Tac Toe!", 
            font=("Arial", 36, "bold"), 
            text_color="white",
            fg_color="Gray",
            corner_radius=5
        )
        welcome_label.pack(pady=(175, 10))

        # Label de sélection du mode
        mode_label = ctk.CTkLabel(frame, text="Select Game Mode:")
        mode_label.pack(pady=(10, 5))  # Espacement en haut et en bas

        # Menu déroulant pour le mode de jeu
        self.mode_var = ctk.StringVar(value="Classique")
        mode_menu = ctk.CTkOptionMenu(frame, variable=self.mode_var, values=["Classique", "Case grise"])
        mode_menu.pack(pady=(5, 10))  # Espacement en haut et en bas

        # Bouton Play
        play_button = ctk.CTkButton(frame, text="Play", command=self.settings_page)
        play_button.pack(pady=(10, 5))  # Espacement en haut et en bas

            # Options button (to navigate to settings)
        options_button = ctk.CTkButton(
            frame,
            text="Options",
            command=self.options_page
        )
        options_button.pack(pady=(5, 5))

        # Bouton Quit
        quit_button = ctk.CTkButton(frame, text="Quit", command=self.confirm_exit)
        quit_button.pack(pady=(5, 20))  # Espacement en haut et en bas

        # Texte en bas stylisé
        footer_label = ctk.CTkLabel(
            self.root,
            text="Made with heart ❤ by Nassim",
            font=("Arial", 10, "italic"),
            text_color="gray",
            fg_color="transparent"
        )
        footer_label.pack(side="bottom", pady=10)

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
        else :
            self.first_player_menu.pack(pady=(0, 170))
        start_button = ctk.CTkButton(frame, text="Start Game", command=self.start_game)
        start_button.pack(pady=3)

        back_button = ctk.CTkButton(frame, text="Back", command=self.welcome_page)
        back_button.pack(pady=3)

        quit_button = ctk.CTkButton(frame, text="Quit", command=self.confirm_exit)
        quit_button.pack(pady=3)

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
                self.ai_depth = 6
            else:  # Grille > 3x3
                self.ai_depth = 2
        else:  # Difficulté "Easy"
            if rows * cols <= 9:  # Grille 3x3
                self.ai_depth = 4
            else:  # Grille > 3x3
                self.ai_depth = 1


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

    def make_move(self, row, col):
        cell = self.grid[row][col]
        if cell.cget("text") == "":
            cell.configure(fg_color=self.current_player, state="disabled")
            self.move_stack.append((row, col, self.current_player))  # Ajouter coup à la pile
            self.redo_stack.clear()  # Effacer redo_stack après un nouveau coup

            if self.check_winner(row, col):
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.settings_page()
                return
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.settings_page()
                return

            # Changement de joueur
            self.current_player = self.ai_color if self.current_player == self.player_color else self.player_color

            # IA joue
            if self.current_player == self.ai_color:
                ai_move = self.find_best_move()
                if ai_move:
                    self.make_move(*ai_move)
    def get_empty_cells(self):
        empty_cells = []
        for r, row in enumerate(self.grid):
            for c, cell in enumerate(row):
                if cell.cget("fg_color") == "gray":  # Case non jouée
                    empty_cells.append((r, c))
        return empty_cells

    def minimax(self, is_ai_turn, depth):
        empty_cells = self.get_empty_cells()
        if depth == 0:
            return 0  # Arrêt conditionnel basé sur la profondeur

        # Vérifier si l'IA ou le joueur a gagné après le dernier coup
        winner = None
        for (r, c) in empty_cells:
            if self.check_winner(r, c):  # Vérifier si ce coup conduit à une victoire
                winner = self.current_player
                break

        if winner == self.ai_color:
            return 1  # Victoire pour l'IA
        elif winner == self.player_color:
            return -1  # Victoire pour le joueur
        elif self.check_draw():  # Vérifier si c'est une égalité
            return 0
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

    def find_best_move(self):
        best_score = float("-inf")
        best_move = None
        empty_cells = self.get_empty_cells()

        for (r, c) in empty_cells:
            self.grid[r][c].configure(fg_color=self.ai_color)
            score = self.minimax(False, depth=self.ai_depth)
            self.grid[r][c].configure(fg_color="gray")  # Annuler le coup
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move
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

        for _ in range(2):  # Restaurer deux derniers coups
            row, col, color = self.redo_stack.pop()
            self.move_stack.append((row, col, color))  # Replacer dans move_stack
            cell = self.grid[row][col]
            cell.configure(fg_color=color, state="disabled")

        self.current_player = self.player_color

    def check_draw(self):
        for row in self.grid:
            for cell in row:
                if cell.cget("fg_color") == "gray":  # Une case grise indique qu'elle n'a pas été jouée
                    return False
        return True

    def check_winner(self, row, col):
        rows, cols = len(self.grid), len(self.grid[0])

        for r in range(rows):
            if all(self.grid[r][c].cget("fg_color") == self.current_player for c in range(cols)):
                return True
        
        for c in range(cols):
            if all(self.grid[r][c].cget("fg_color") == self.current_player for r in range(rows)):
                return True

        if all(self.grid[i][i].cget("fg_color") == self.current_player for i in range(rows)):
            return True
        
        if all(self.grid[i][rows - 1 - i].cget("fg_color") == self.current_player for i in range(rows)):
            return True

        return False


    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to quit the game?"):
            self.root.destroy()


    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToeApp(root)
    root.mainloop()


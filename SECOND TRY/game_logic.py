from tkinter import messagebox

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
        self.win_cond = self.Win_var.get()

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
        # Determine the number of rows and columns based on win condition
        if self.win_cond == "Par defaut":
            rows, cols = len(self.grid), len(self.grid[0])
        else:
            win_size = int(self.win_cond)
            rows, cols = len(self.grid), len(self.grid[0])

        # Check for horizontal win
        for r in range(rows):
            for c in range(cols - win_size + 1):
                if all(self.grid[r][c + i].cget("fg_color") == color for i in range(win_size)):
                    return True

        # Check for vertical win
        for c in range(cols):
            for r in range(rows - win_size + 1):
                if all(self.grid[r + i][c].cget("fg_color") == color for i in range(win_size)):
                    return True

        # Check for diagonal win (top-left to bottom-right)
        for r in range(rows - win_size + 1):
            for c in range(cols - win_size + 1):
                if all(self.grid[r + i][c + i].cget("fg_color") == color for i in range(win_size)):
                    return True

        # Check for diagonal win (top-right to bottom-left)
        for r in range(rows - win_size + 1):
            for c in range(win_size - 1, cols):
                if all(self.grid[r + i][c - i].cget("fg_color") == color for i in range(win_size)):
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
        for _ in range(2):  # Restaurer deux derniers coups
            row, col, color = self.redo_stack.pop()
            self.move_stack.append((row, col, color))  # Replacer dans move_stack
            cell = self.grid[row][col]
            cell.configure(fg_color=color, state="disabled")

        self.current_player = self.player_color
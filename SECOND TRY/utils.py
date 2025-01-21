from tkinter import messagebox
import customtkinter as ctk
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

    def update_theme_button(self,button):
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

    def update_Win_options(self,*args):
        rows_selected = self.rows_var.get()
        cols_selected = self.cols_var.get()

        nbr1 = min(rows_selected, cols_selected)
        options = ["Par defaut"]

        while nbr1 >= 3:
            options.append(str(nbr1))
            nbr1 -= 1

        current_selection = self.Win_var.get()
        if current_selection in options:
            options.remove(current_selection)

        self.Win_menu.configure(values=options)


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

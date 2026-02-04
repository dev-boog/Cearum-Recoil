import customtkinter as ctk

from menu.custom_widgets.widgets import Widgets
from tkinter import filedialog

class SettingsMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  
        
        self.configure(fg_color="transparent")
        
        self.game_scaler, _ = Widgets.render_combobox(self, "Game Scalar", ["Manual", "CS2"], "Manual")


        ctk.CTkLabel(self, text="Game Sensitivity", text_color="#FFFFFF").pack(padx=3, pady=(5,0), anchor="w")
        self.cs2_user_sens = ctk.CTkTextbox(self, height=20, border_width=1, border_color="#404040", fg_color="#1A1A1A", text_color="#FFFFFF")
        self.cs2_user_sens.pack(padx=3, pady=(0,3), fill="x")
        
    def get_cs2_sensitivity(self):
        try:
            value = self.cs2_user_sens.get("1.0", "end").strip()
            sens = float(value)
            return sens if sens > 0 else 1.0
        except ValueError:
            return 1.0
        
    def get_game_scalar(self):
        return str(self.game_scaler.get())

        
    
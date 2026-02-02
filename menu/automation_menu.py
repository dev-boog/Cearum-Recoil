import customtkinter as ctk
from tkinter import filedialog

class AutomationMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x")
        ctk.CTkLabel(info_frame, text="Format: X, Y, MS_DELAY, EVENT", font=ctk.CTkFont(size=12)).pack(padx=5, pady=1, side="left")
        ctk.CTkLabel(info_frame, text="Events: RCLICK, LCLICK", font=ctk.CTkFont(size=12)).pack(padx=5, pady=1, side="right")
        self.mouse_movements_inpt = ctk.CTkTextbox(self, width=150, height=250, font=("Consolas", 14), border_width=1, border_color="gray")
        self.mouse_movements_inpt.pack(padx=5, pady=5, fill="x")
        self.mouse_movements_inpt.bind("<<Modified>>", self.on_modified)
        
    
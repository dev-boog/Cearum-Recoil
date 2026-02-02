import customtkinter as ctk
import webbrowser
from tkinter import filedialog

class SettingsMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)  
        
        self.configure(fg_color="transparent")

        ctk.CTkButton(self, text="Join Discord", command=self.join_discord).pack(padx=3, pady=3, fill="x")
        
    def join_discord(self):
        webbrowser.open("https://discord.gg/llamarecoil")
        
    
import customtkinter as ctk

from.automation_menu import AutomationMenu
from .recoil_menu import RecoilMenu 
from .settings_menu import SettingsMenu

from customtkinter import CTkImage
from PIL import Image
from tkinter import PhotoImage

import os
import sys

class MenuApp(ctk.CTk): 
    def __init__(self):
        self.is_running = True
        
        super().__init__()
        self.geometry("400x820")
        ctk.set_default_color_theme("dark-blue")
        ctk.set_widget_scaling(0.8)
        
        if getattr(sys, 'frozen', False):
            BASE_DIR = sys._MEIPASS  
            EXE_DIR = os.path.dirname(sys.executable) 
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            EXE_DIR = BASE_DIR

        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
        
        self.title("")
        self.resizable(False, False)

        self.configure(fg_color="#151515")  
        
        logo = Image.open(logo_path)
        logo = logo.resize((120, 120))
        logo_image = CTkImage(light_image=logo, dark_image=logo, size=(120, 120))
        ctk.CTkLabel(self, image=logo_image, text="").pack(pady=(7,0))
       

        self.tabs = ctk.CTkTabview(self, width=280, height=340, border_width=1, fg_color="#232323", border_color="#404040")
        self.tabs.pack(padx=10, pady=(0,10), fill="both", expand=True)
        self.mouse_tab = self.tabs.add("Recoil")
        self.settings_tab = self.tabs.add("Settings")

        self.recoil_menu = RecoilMenu(self.mouse_tab)
        self.recoil_menu.pack(padx=5, pady=5, fill="both", expand=True)

        self.settings_menu = SettingsMenu(self.settings_tab)
        self.settings_menu.pack(padx=5, pady=5, fill="both", expand=True)
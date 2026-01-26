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

        self.geometry("400x825")
        self.resizable(False, False)

        ctk.set_default_color_theme("blue")
        ctk.set_widget_scaling(1.0)

        self.configure(fg_color="#151515")

        # -------- PATH HANDLING --------
        if getattr(sys, "frozen", False):
            EXE_DIR = os.path.dirname(sys.executable)
        else:
            EXE_DIR = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(EXE_DIR, "assets", "logo.png")

        # -------- LOGO (KEEP REFERENCE) --------
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((120, 120))

        self.logo_image = CTkImage(
            light_image=logo,
            dark_image=logo,
            size=(120, 120)
        )

        ctk.CTkLabel(self, image=self.logo_image, text="").pack(pady=(7, 0))

        # -------- TABS --------
        self.tabs = ctk.CTkTabview(
            self,
            width=280,
            height=340,
            border_width=1,
            fg_color="#232323",
            border_color="#404040"
        )
        self.tabs.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        self.mouse_tab = self.tabs.add("Recoil")
        self.settings_tab = self.tabs.add("Settings")

        # -------- MENUS --------
        self.recoil_menu = RecoilMenu(self.mouse_tab)
        self.recoil_menu.pack(padx=5, pady=5, fill="both", expand=True)

        self.settings_menu = SettingsMenu(self.settings_tab)
        self.settings_menu.pack(padx=5, pady=5, fill="both", expand=True)
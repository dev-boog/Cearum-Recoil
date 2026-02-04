from menu.menu import MenuApp  
from menu.recoil_menu import RecoilMenu
from mouse.makcu import makcu_controller
from features.recoil.recoil import recoil

import tkinter as tk
from tkinter import messagebox

import time
import threading
import os

def show_message(title: str, message: str):
    root = tk.Tk()
    root.withdraw()  
    root.attributes('-topmost', True)
    messagebox.showinfo(title, message)

def main():
    app = MenuApp()
    
    if makcu_controller.connect() is None:
        show_message("Cearum", "Their was an error connecting to your Makcu. Please make sure its connected and try again.")
        time.sleep(3)
        return
    
    show_message("Cearum", "Makcu has been found.")
    makcu_controller.StartButtonListener() 

    recoil_thread = threading.Thread(target=recoil.run_recoil, args=(app.recoil_menu, app.settings_menu), daemon=True)
    recoil_thread.start()

    def on_closing():
        time.sleep(0.1)
        app.destroy()        
        os._exit(0)         

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()

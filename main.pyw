from menu.menu import MenuApp  
from mouse.makcu import makcu_controller
from features.recoil.recoil import recoil

import tkinter as tk
from tkinter import messagebox

import time
import threading

def show_message(title: str, message: str):
    root = tk.Tk()
    root.withdraw()  
    root.attributes('-topmost', True)
    messagebox.showinfo(title, message)
    
def cycle_script_listener(app):
    last_cycle_state = False
    while True:
        try:
            if not makcu_controller.is_connected():
                time.sleep(0.5)  # Longer sleep when disconnected
                continue
                
            recoil_menu = app.recoil_menu
            cycle_key = recoil_menu.cycle_keybind.get()
            if cycle_key != "NONE":
                pressed = makcu_controller.get_button_state(cycle_key)
                if pressed and not last_cycle_state:
                    recoil_menu.cycle_script() 
                last_cycle_state = pressed
            time.sleep(0.1)  # Increased from 0.05 to reduce CPU usage
        except Exception as e:
            print(f"Cycle listener error: {e}")
            time.sleep(0.5)

def main():
    app = MenuApp()
    
    if makcu_controller.connect() is None:
        show_message("Cearum", "Their was an error connecting to your Makcu. Please make sure its connected and try again.")
        time.sleep(3)
        return
    
    show_message("Cearum", "Makcu has been found.")
    makcu_controller.StartButtonListener() 

    recoil_thread = threading.Thread(target=recoil.run_recoil, args=(app.recoil_menu,), daemon=True)
    recoil_thread.start()
    
    cycle_thread = threading.Thread(target=cycle_script_listener, args=(app,), daemon=True)
    cycle_thread.start()

    def on_closing():
        time.sleep(0.1)
        app.destroy()        
        import os
        os._exit(0)         

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()

from menu.menu import MenuApp
from mouse.makcu import makcu_controller
from features.recoil.recoil import recoil

import tkinter as tk
from tkinter import messagebox
import threading
import time

def main():
    # -------- CREATE CTK ROOT --------
    app = MenuApp()

    def show_message(title: str, message: str):
        app.after(
            0,
            lambda: messagebox.showinfo(title, message, parent=app)
        )

    # -------- MAKCU CONNECT --------
    if makcu_controller.connect() is None:
        show_message(
            "Cearum",
            "There was an error connecting to your Makcu.\n"
            "Make sure it is connected and try again."
        )
        return

    show_message("Cearum", "Makcu has been found.")
    makcu_controller.StartButtonListener()

    # -------- RECOIL THREAD (UNCHANGED) --------
    recoil_thread = threading.Thread(
        target=recoil.run_recoil,
        args=(app.recoil_menu,),
        daemon=True
    )
    recoil_thread.start()

    # -------- GUI-SAFE CYCLE POLLING --------
    app._last_cycle_state = False

    def cycle_script_poll():
        if not app.is_running:
            return

        recoil_menu = app.recoil_menu
        cycle_key = recoil_menu.cycle_keybind.get()

        if cycle_key != "NONE":
            pressed = makcu_controller.get_button_state(cycle_key)

            if pressed and not app._last_cycle_state:
                recoil_menu.cycle_script()

            app._last_cycle_state = pressed

        app.after(50, cycle_script_poll)

    app.after(50, cycle_script_poll)

    # -------- CLEAN SHUTDOWN --------
    def on_closing():
        app.is_running = False
        makcu_controller.disconnect()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
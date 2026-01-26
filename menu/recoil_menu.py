import customtkinter as ctk
import os
from tkinter import filedialog

from menu.custom_widgets.widgets import Widgets
from mouse.makcu import makcu_controller


class RecoilMenu(ctk.CTkFrame):
    SCRIPTS_DIR = "./saved_scripts"
    LOADED_SCRIPT_NAME = "NONE"

    def __init__(self, parent):
        super().__init__(parent)

        self.vectors = []
        self.configure(fg_color="transparent")

        self.enable_checkbox, _ = Widgets.render_checkbox(self, "Enable", False)
        self.toggle_keybind, _ = Widgets.render_combobox(self, "Toggle Keybind", ["M4", "M5", "MMB", "NONE"], "NONE")
        self.enable_require_right_chk, _ = Widgets.render_checkbox(self, "Require Aim", False)
        self.loop_recoil_chk, _ = Widgets.render_checkbox(self, "Loop Recoil", False)

        self.scalar_slider, self.scalar_value_label = Widgets.render_slider(self, "Recoil Scalar", 1.0, 0.0, 3.0, self.update_scalar_label)
        self.control_x_slider, self.control_x_value_label = Widgets.render_slider(self, "X Control", 1.0, 0.0, 1.0, self.update_x_control_label)
        self.control_y_slider, self.control_y_value_label = Widgets.render_slider(self, "Y Control", 1.0, 0.0, 1.0, self.update_y_control_label)

        self.vector_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.vector_frame.pack(fill="x")

        self.mouse_movements_inpt = ctk.CTkTextbox(self.vector_frame, height=300, width=120, font=("Consolas", 12), border_width=1, border_color="#404040", fg_color="#1A1A1A", text_color="#575757")
        self.mouse_movements_inpt.pack(side="left", pady=(0, 5))
        self.mouse_movements_inpt.bind("<<Modified>>", self.on_modified)

        self.script_list_frame = ctk.CTkFrame(self.vector_frame, width=235, height=300, fg_color="#1A1A1A", border_color="#404040", border_width=1)
        self.script_list_frame.pack(side="right", pady=(0, 5))
        self.script_list_frame.pack_propagate(False)

        self.scrollable_container = ctk.CTkScrollableFrame(self.script_list_frame, fg_color="#1A1A1A", border_color="#404040", border_width=1)
        self.scrollable_container.pack(fill="both", expand=True)

        self.refresh_script_list()

        name_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", border_color="#404040", border_width=1)
        name_frame.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(name_frame, text="Loaded Script", text_color="#FFFFFF").pack(side="left", padx=10)
        self.script_name_label = ctk.CTkLabel(name_frame, text="No Script Loaded", text_color="#6B6B6B")
        self.script_name_label.pack(side="right", padx=10, pady=2)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x")

        self.cycle_keybind, _ = Widgets.render_combobox(btn_frame, "Cycle Keybind", ["M4", "M5", "MMB", "NONE"], "NONE")
        
        ctk.CTkButton(btn_frame, text="Save Vector", command=self.save_vector, text_color="#FFFFFF").pack(side="left", padx=5, pady=5)
        ctk.CTkButton(btn_frame, text="Change Directory", command=self.change_directory, text_color="#FFFFFF").pack(side="right", padx=5, pady=5)
        
    def refresh_script_list(self):
        os.makedirs(self.SCRIPTS_DIR, exist_ok=True)

        for w in self.scrollable_container.winfo_children():
            w.destroy()

        scripts = sorted(f[:-4] for f in os.listdir(self.SCRIPTS_DIR) if f.endswith(".txt"))

        if not scripts:
            ctk.CTkLabel(self.scrollable_container, text="No scripts saved", text_color="#555555").pack(pady=20)
            return

        for script in scripts:
            if script == self.LOADED_SCRIPT_NAME:
                frame_color = "#1F4D2B"  # green for loaded script
                border_color = "#3C9D5D"
                text=""
            else:
                frame_color = "#2E2E2E"
                border_color = "#404040"
                text="Load"
                
            frame = ctk.CTkFrame(self.scrollable_container, fg_color=frame_color, border_color=border_color, border_width=1)
            frame.pack(fill="x", padx=5, pady=(5, 0))

            ctk.CTkLabel(frame, text=script).pack(side="left", padx=5)
            ctk.CTkButton(frame, text="X", width=5, fg_color="transparent", text_color="#FF5555", hover=False, command=lambda s=script: self.delete_vector_from_name(s)).pack(side="right", padx=(0, 5), pady=1)
            ctk.CTkButton(frame, text=text, width=40, fg_color="transparent", text_color="#575757", hover=False, command=lambda s=script: self.load_vector_from_name(s)).pack(side="right", padx=(5,0), pady=1)
    
    def cycle_script(self):
        scripts = sorted(f[:-4] for f in os.listdir(self.SCRIPTS_DIR) if f.endswith(".txt"))
        if not scripts:
            return

        if self.LOADED_SCRIPT_NAME in scripts:
            current_index = scripts.index(self.LOADED_SCRIPT_NAME)
            next_index = (current_index + 1) % len(scripts)
        else:
            next_index = 0

        self.load_vector_from_name(scripts[next_index])
    
    def change_directory(self):
        path = filedialog.askdirectory(initialdir=self.SCRIPTS_DIR)
        if path:
            self.SCRIPTS_DIR = path
            self.refresh_script_list()
    
    def save_vector(self):
        path = filedialog.asksaveasfilename(initialdir=self.SCRIPTS_DIR, defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        with open(path, "w") as f:
            f.write(self.mouse_movements_inpt.get("0.0", "end-1c"))
        self.script_name_label.configure(text=os.path.basename(path)[:-4])
        self.refresh_script_list()

    def load_vector_from_name(self, name):
        path = os.path.join(self.SCRIPTS_DIR, f"{name}.txt")
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            self.mouse_movements_inpt.delete("0.0", "end")
            self.mouse_movements_inpt.insert("0.0", f.read())
        self.script_name_label.configure(text=name)
        self.LOADED_SCRIPT_NAME = os.path.basename(path)[:-4]
        self.refresh_script_list()

    def delete_vector_from_name(self, name):
        path = os.path.join(self.SCRIPTS_DIR, f"{name}.txt")
        if os.path.exists(path):
            os.remove(path)
        self.refresh_script_list()

    def load_vector(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        with open(path, "r") as f:
            self.mouse_movements_inpt.delete("0.0", "end")
            self.mouse_movements_inpt.insert("0.0", f.read())
        self.script_name_label.configure(text=os.path.basename(path)[:-4])
        self.LOADED_SCRIPT_NAME = os.path.basename(path)[:-4]
        self.refresh_script_list()

    def on_modified(self, _=None):
        self.mouse_movements_inpt.edit_modified(False)
        self.vectors = self.get_mouse_vectors()

    def update_x_control_label(self, v):
        self.control_x_value_label.configure(text=f"{float(v):.2f}")

    def update_y_control_label(self, v):
        self.control_y_value_label.configure(text=f"{float(v):.2f}")

    def update_scalar_label(self, v):
        self.scalar_value_label.configure(text=f"{float(v):.2f}")
        makcu_controller.set_recoil_scaler(float(v))

    def get_mouse_vectors(self):
        vectors = []
        for line in self.mouse_movements_inpt.get("0.0", "end-1c").splitlines():
            try:
                x, y, d = map(str.strip, line.split(","))
                vectors.append((float(x), float(y), float(d) / 1000))
            except:
                pass
        return vectors

    def get_is_enabled(self):
        return self.enable_checkbox.get()

    def get_is_recoil_looped(self):
        return self.loop_recoil_chk.get()

    def get_toggle_keybind(self):
        return self.toggle_keybind.get()
    def get_x_control(self):
        return self.control_x_slider.get()
    def get_y_control(self):
        return self.control_y_slider.get()

    def requires_right_button(self):
        return self.enable_require_right_chk.get()

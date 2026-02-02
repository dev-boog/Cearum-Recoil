import customtkinter as ctk
import tkinter as tk

class Widgets:
    @staticmethod
    def render_slider(parent, text, default_value=0.0, from_=0.0, to=1.0, command=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x")

        slider = ctk.CTkSlider(frame, from_=from_, to=to, orientation="horizontal", command=command)
        slider.set(default_value)
        slider.pack(padx=0, fill="x", side="left")

        ctk.CTkLabel(frame, text=text, text_color="#FFFFFF").pack(padx=3, side="right")

        value_label = ctk.CTkLabel(frame, text=str(default_value), font=ctk.CTkFont(weight="bold"), text_color="#FFFFFF")
        value_label.pack(padx=3, side="right")

        return slider, value_label

    @staticmethod
    def render_checkbox(parent, text, default_value=False, command=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x")

        var = tk.BooleanVar(value=default_value)
        checkbox = ctk.CTkCheckBox(frame, text="", variable=var, border_width=1, border_color="#404040", command=command)
        checkbox.var = var  # attach var to checkbox so you can access it later
        checkbox.pack(padx=0, pady=5, side="left")

        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=12), text_color="#FFFFFF")
        label.pack(padx=3, pady=3, side="right")

        return checkbox, label
    
    @staticmethod
    def render_combobox(parent, text, values, default_value=None, command=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x")

        combobox = ctk.CTkComboBox(frame, values=values, border_width=1, border_color="#404040", button_color="#1A1A1A", fg_color="#1A1A1A", text_color="#535353", command=command)
        if default_value is not None:
            combobox.set(default_value)
        combobox.pack(padx=0, pady=3, fill="x", side="left")

        label = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=12), text_color="#FFFFFF")
        label.pack(padx=3, pady=3, side="right")

        return combobox, label

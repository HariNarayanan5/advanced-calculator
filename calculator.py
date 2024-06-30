import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import math
import matplotlib.pyplot as plt
import numpy as np
import speech_recognition as sr
from mpl_toolkits.mplot3d import Axes3D

class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Calculator")
        self.geometry("800x1000")
        self.resizable(True, True)
        self.configure(bg="#202020")

        self.current_input = ""
        self.memory = ""
        self.history = []
        self.theme = "dark"

        self.create_widgets()
        self.create_styles()

    def create_widgets(self):
        self.display_frame = tk.Frame(self, height=2, bg="#202020")
        self.display_frame.pack(fill="both", padx=10, pady=10)

        self.history_display = tk.Label(self.display_frame, text="", anchor="e", font=("Arial", 12), bg="#000000", fg="#FFFFFF")
        self.history_display.pack(expand=True, fill="both")

        self.result_display = tk.Label(self.display_frame, text="", anchor="e", font=("Arial", 24), bg="#000000", fg="#FFFFFF")
        self.result_display.pack(expand=True, fill="both")

        self.button_frame = tk.Frame(self, bg="#202020")
        self.button_frame.pack(expand=True, fill="both")

        self.create_buttons()

        self.voice_button = tk.Button(self, text="Voice Input", command=self.voice_input, bg="#333333", fg="#FFFFFF")
        self.voice_button.pack(side="left", padx=10, pady=10)

        self.plot_button = tk.Button(self, text="Plot Graph", command=self.plot_graph, bg="#333333", fg="#FFFFFF")
        self.plot_button.pack(side="right", padx=10, pady=10)

        self.theme_button = tk.Button(self, text="Toggle Theme", command=self.toggle_theme, bg="#333333", fg="#FFFFFF")
        self.theme_button.pack(side="top", padx=10, pady=10)

    def create_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 18), borderwidth=0, relief="flat", background="#333333", foreground="#FFFFFF")
        style.map("TButton", background=[("active", "#666666")])
        style.configure("Display.TFrame", background="#000000")

    def create_buttons(self):
        button_texts = [
            ['C', 'CE', 'M+', 'M-', 'MR', 'MC'],
            ['7', '8', '9', '/', 'sinh', 'cosh'],
            ['4', '5', '6', '*', 'tanh', 'log'],
            ['1', '2', '3', '-', 'ln', '^'],
            ['0', '.', '=', '+', '(', ')']
        ]

        button_colors = {
            "C": "#ff6666", "CE": "#ff6666", "M+": "#66ccff", "M-": "#66ccff", 
            "MR": "#66ccff", "MC": "#66ccff", "=": "#66ff66"
        }

        for row in button_texts:
            button_row = tk.Frame(self.button_frame, bg="#202020")
            button_row.pack(expand=True, fill="both")
            for btn_text in row:
                btn_color = button_colors.get(btn_text, "#333333")
                button = tk.Button(button_row, text=btn_text, font=("Arial", 18), bg=btn_color, fg="#FFFFFF", command=lambda x=btn_text: self.on_button_click(x))
                button.pack(side="left", expand=True, fill="both")
                self.animate_button(button, btn_color)

    def animate_button(self, button, color):
        def on_enter(e):
            button.configure(bg="#888888")
        def on_leave(e):
            button.configure(bg=color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def on_button_click(self, char):
        if char == "=":
            self.calculate()
        elif char in ["C", "CE"]:
            self.clear_display(char)
        elif char in ["M+", "M-", "MR", "MC"]:
            self.memory_operations(char)
        else:
            self.current_input += str(char)
            self.update_display()

    def calculate(self):
        try:
            result = eval(self.current_input)
            self.history.append(self.current_input + "=" + str(result))
            self.current_input = str(result)
            self.update_display()
            self.update_history_display()
        except Exception as e:
            self.result_display.config(text="Error")

    def clear_display(self, clear_type):
        if clear_type == "C":
            self.current_input = ""
        elif clear_type == "CE":
            self.current_input = self.current_input[:-1]
        self.update_display()

    def memory_operations(self, operation):
        if operation == "M+":
            self.memory = self.current_input
        elif operation == "M-":
            self.memory = ""
        elif operation == "MR":
            self.current_input += self.memory
            self.update_display()
        elif operation == "MC":
            self.memory = ""

    def update_display(self):
        self.result_display.config(text=self.current_input)

    def update_history_display(self):
        self.history_display.config(text="\n".join(self.history[-5:]))

    def plot_graph(self):
        equation = self.current_input
        x = np.linspace(-10, 10, 400)
        y = eval(equation)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label=equation)
        plt.title("Graph Plot")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.show()

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                self.current_input = command
                self.update_display()
            except sr.UnknownValueError:
                messagebox.showerror("Voice Input Error", "Could not understand the audio.")
            except sr.RequestError:
                messagebox.showerror("Voice Input Error", "Could not request results; check your network connection.")

    def toggle_theme(self):
        if self.theme == "dark":
            self.configure(bg="#FFFFFF")
            self.display_frame.configure(bg="#FFFFFF")
            self.history_display.configure(bg="#FFFFFF", fg="#000000")
            self.result_display.configure(bg="#FFFFFF", fg="#000000")
            self.button_frame.configure(bg="#FFFFFF")
            self.theme = "light"
        else:
            self.configure(bg="#202020")
            self.display_frame.configure(bg="#202020")
            self.history_display.configure(bg="#000000", fg="#FFFFFF")
            self.result_display.configure(bg="#000000", fg="#FFFFFF")
            self.button_frame.configure(bg="#202020")
            self.theme = "dark"

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = AdvancedCalculator()
    app.run()

import tkinter as tk
from tkinter import ttk
import time

class WelcomeScreen:
    
    def __init__(self, root, main_app_callback):
        self.root = root
        self.main_app_callback = main_app_callback
        self.root.title("Hospital Management System")
        self.root.geometry("600x400")
        self.root.config(bg="#f4f4f9")
        
        # Center the window
        window_width = 600
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Welcome content
        self.logo_label = tk.Label(
            self.root,
            text="🏥",
            font=("Helvetica", 72),
            bg="#f4f4f9",
            fg="#4CAF50"
        )
        self.logo_label.pack(pady=50)
        
        self.welcome_label = tk.Label(
            self.root,
            text="Welcome to Hospital Management System",
            font=("Helvetica", 18),
            bg="#f4f4f9",
            fg="#333333"
        )
        self.welcome_label.pack()
        
        self.loading_label = tk.Label(
            self.root,
            text="Loading...",
            font=("Helvetica", 12),
            bg="#f4f4f9",
            fg="#666666"
        )
        self.loading_label.pack(pady=20)
        
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack()
        
        # Simulate loading
        self.load_progress()
        
    def load_progress(self):
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.03)
        self.root.destroy()
        self.main_app_callback()
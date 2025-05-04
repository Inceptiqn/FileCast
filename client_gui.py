import tkinter as tk
from tkinter import ttk
from Client import FileClient
import threading
import os

class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FileCast Client")
        self.window.geometry("400x500")
        
        self.client = FileClient(port=65432)  # Match server port
        self.setup_gui()

    def setup_gui(self):
        # Connection controls
        conn_frame = ttk.Frame(self.window, padding="5")
        conn_frame.pack(fill='x', padx=5, pady=5)
        
        self.connect_button = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.pack(side='left', padx=5)
        
        # Status display
        self.status_var = tk.StringVar(value="Not connected")
        status_label = ttk.Label(self.window, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # File list
        files_frame = ttk.LabelFrame(self.window, text="Received Files", padding="5")
        files_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.file_list = tk.Listbox(files_frame)
        self.file_list.pack(fill='both', expand=True)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            self.window, 
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(fill='x', padx=5, pady=5)

    def toggle_connection(self):
        if self.connect_button['text'] == "Connect":
            self.connect_button['text'] = "Disconnect"
            self.status_var.set("Connecting...")
            # Start connection in separate thread
            threading.Thread(target=self.connect).start()
        else:
            self.client.running = False
            self.connect_button['text'] = "Connect"
            self.status_var.set("Disconnected")

    def connect(self):
        try:
            self.client.connect()
            self.status_var.set("Connected")
        except Exception as e:
            self.status_var.set(f"Connection failed: {e}")
            self.connect_button['text'] = "Connect"

    def update_progress(self, received, total):
        progress = (received / total) * 100
        self.progress_var.set(progress)
        self.window.update_idletasks()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ClientGUI()
    gui.run()
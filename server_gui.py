import tkinter as tk
from tkinter import ttk, filedialog
from Server import FileServer

class ServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FileCast Server")
        self.window.geometry("400x500")
        
        self.server = FileServer(port=65432)  # Using a less common port
        self.server.set_callbacks(
            client_callback=self.update_client_list,
            status_callback=self.update_status
        )
        self.setup_gui()

    def setup_gui(self):
        # Server controls
        control_frame = ttk.Frame(self.window, padding="5")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Server", command=self.toggle_server)
        self.start_button.pack(side='left', padx=5)
        
        self.file_button = ttk.Button(control_frame, text="Select File", command=self.select_file)
        self.file_button.pack(side='left', padx=5)
        self.file_button['state'] = 'disabled'
        
        # Status display
        self.status_var = tk.StringVar(value="Server not running")
        status_label = ttk.Label(self.window, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Client list
        client_frame = ttk.LabelFrame(self.window, text="Connected Clients", padding="5")
        client_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.client_list = tk.Listbox(client_frame)
        self.client_list.pack(fill='both', expand=True)

    def toggle_server(self):
        if self.start_button['text'] == "Start Server":
            if self.server.start():
                self.start_button['text'] = "Stop Server"
                self.file_button['state'] = 'normal'
                self.update_status("Server running")
        else:
            self.server.stop()
            self.start_button['text'] = "Start Server"
            self.file_button['state'] = 'disabled'
            self.update_status("Server stopped")
            self.client_list.delete(0, tk.END)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.server.set_file(file_path)
            self.update_status(f"Selected file: {file_path}")

    def update_status(self, status):
        self.status_var.set(status)
        self.window.update_idletasks()

    def update_client_list(self, client_info, remove=False):
        if remove:
            # Find and remove client from list
            items = self.client_list.get(0, tk.END)
            for idx, item in enumerate(items):
                if client_info in item:
                    self.client_list.delete(idx)
                    break
        else:
            self.client_list.insert(tk.END, f"Client: {client_info}")
        self.window.update_idletasks()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ServerGUI()
    gui.run()
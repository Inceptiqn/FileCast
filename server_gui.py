import tkinter as tk
from tkinter import ttk, filedialog
from Server import FileServer
import threading

class ServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FileCast Server")
        self.window.geometry("400x500")
        
        self.server = FileServer(port=65432)  # Using a less common port
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
                self.status_var.set("Server running")
                # Start accept thread
                self.accept_thread = threading.Thread(target=self.accept_clients)
                self.accept_thread.daemon = True
                self.accept_thread.start()
        else:
            self.server.stop()
            self.start_button['text'] = "Start Server"
            self.file_button['state'] = 'disabled'
            self.status_var.set("Server stopped")
            self.client_list.delete(0, tk.END)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.server.file_path = file_path
            self.status_var.set(f"Selected file: {file_path}")
            self.server.ready_to_send.set()

    def accept_clients(self):
        while self.server.running:
            try:
                client_socket, address = self.server.server_socket.accept()
                self.server.clients.append(client_socket)
                self.client_list.insert(tk.END, f"Client: {address[0]}:{address[1]}")
                client_thread = threading.Thread(
                    target=self.server.handle_client,
                    args=(client_socket,)
                )
                client_thread.daemon = True
                client_thread.start()
            except:
                if self.server.running:  # Only show error if we're still supposed to be running
                    self.status_var.set("Error accepting client")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = ServerGUI()
    gui.run()
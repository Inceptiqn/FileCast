import tkinter as tk
from tkinter import ttk, filedialog
from Server import FileServer

class ServerGUI:
    def __init__(self):
        # Inizializzazione della finestra principale
        self.window = tk.Tk()
        self.window.title("FileCast Server")
        self.window.geometry("400x500")
        
        # Creazione del server e configurazione callback
        self.server = FileServer(port=65432)
        self.server.set_callbacks(
            client_callback=self.update_client_list,
            status_callback=self.update_status
        )
        self.setup_gui()

    def setup_gui(self):
        # Controlli del server
        control_frame = ttk.Frame(self.window, padding="5")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Server", command=self.toggle_server)
        self.start_button.pack(side='left', padx=5)
        
        self.file_button = ttk.Button(control_frame, text="Select File", command=self.select_file)
        self.file_button.pack(side='left', padx=5)
        self.file_button['state'] = 'disabled'
        
        # Display stato server
        self.status_var = tk.StringVar(value="Server not running")
        status_label = ttk.Label(self.window, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Lista client connessi
        client_frame = ttk.LabelFrame(self.window, text="Connected Clients", padding="5")
        client_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.client_list = tk.Listbox(client_frame)
        self.client_list.pack(fill='both', expand=True)

    def toggle_server(self):
        # Gestisce avvio/arresto del server
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
        # Seleziona il file da inviare
        file_path = filedialog.askopenfilename()
        if file_path:
            self.server.set_file(file_path)
            self.update_status(f"Selected file: {file_path}")

    def update_status(self, status):
        # Aggiorna lo stato visualizzato
        self.status_var.set(status)
        self.window.update_idletasks()

    def update_client_list(self, client_info, remove=False):
        # Aggiorna la lista dei client connessi
        if remove:
            items = self.client_list.get(0, tk.END)
            for idx, item in enumerate(items):
                if client_info in item:
                    self.client_list.delete(idx)
                    break
        else:
            self.client_list.insert(tk.END, f"Client: {client_info}")
        self.window.update_idletasks()

    def run(self):
        # Avvia l'interfaccia
        self.window.mainloop()

if __name__ == "__main__":
    gui = ServerGUI()
    gui.run()
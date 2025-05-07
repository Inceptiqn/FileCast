import tkinter as tk
from tkinter import ttk, filedialog
import os
from Client import FileClient

class ClientGUI:
    def __init__(self):
        # Inizializzazione della finestra principale
        self.window = tk.Tk()
        self.window.title("FileCast Client")
        self.window.geometry("400x500")
        
        # Creazione del client e configurazione callback
        self.client = FileClient(port=65432)
        self.client.set_callbacks(
            status_callback=self.update_status,
            progress_callback=self.update_progress,
            file_callback=self.update_file_list
        )
        self.setup_gui()

    def setup_gui(self):
        # Controlli di connessione
        conn_frame = ttk.Frame(self.window, padding="5")
        conn_frame.pack(fill='x', padx=5, pady=5)
        
        self.connect_button = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.pack(side='left', padx=5)
        
        # Display stato connessione
        self.status_var = tk.StringVar(value="Not connected")
        status_label = ttk.Label(self.window, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Percorso di salvataggio
        save_frame = ttk.Frame(self.window, padding="5")
        save_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(save_frame, text="Save Location:").pack(side='left', padx=5)
        self.save_location = ttk.Label(save_frame, text=self.client.download_dir)
        self.save_location.pack(side='left', padx=5)
        
        browse_button = ttk.Button(save_frame, text="Browse", command=self.choose_save_location)
        browse_button.pack(side='right', padx=5)
        
        # Lista file ricevuti
        files_frame = ttk.LabelFrame(self.window, text="Received Files", padding="5")
        files_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.file_list = ttk.Treeview(files_frame, columns=("path",), show="tree headings")
        self.file_list.heading("path", text="File Path")
        self.file_list.pack(fill='both', expand=True)
        
        # Barra di progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            self.window, 
            variable=self.progress_var,
            maximum=100
        )
        self.progress.pack(fill='x', padx=5, pady=5)

    def toggle_connection(self):
        # Gestisce connessione/disconnessione
        if self.connect_button['text'] == "Connect":
            self.connect_button['text'] = "Disconnect"
            self.update_status("Connecting...")
            self.client.start_connection()
        else:
            self.client.disconnect()
            self.connect_button['text'] = "Connect"
            self.update_status("Disconnected")

    def update_status(self, status):
        # Aggiorna lo stato visualizzato
        self.status_var.set(status)
        self.window.update_idletasks()

    def update_progress(self, received, total):
        # Aggiorna la barra di progresso
        progress = (received / total) * 100
        self.progress_var.set(progress)
        self.window.update_idletasks()

    def choose_save_location(self):
        # Permette di scegliere dove salvare i file
        directory = filedialog.askdirectory(initialdir=self.client.download_dir)
        if directory:
            self.client.set_download_directory(directory)
            self.save_location.config(text=directory)

    def update_file_list(self, filepath):
        # Aggiorna la lista dei file ricevuti
        filename = os.path.basename(filepath)
        self.file_list.insert("", "end", text=filename, values=(filepath,))
        self.window.update_idletasks()

    def run(self):
        # Avvia l'interfaccia
        self.window.mainloop()

if __name__ == "__main__":
    gui = ClientGUI()
    gui.run()
# FileCast

FileCast è un'applicazione per il trasferimento di file tramite rete locale, sviluppata in Python utilizzando Tkinter per l'interfaccia grafica.

## Caratteristiche

- **Server GUI**: Interfaccia grafica per il controllo del server
- **Client GUI**: Interfaccia grafica per il client con barra di progresso
- **Trasferimento File**: Supporto per l'invio di file di qualsiasi dimensione
- **Connessioni Multiple**: Gestione di più client contemporaneamente
- **Directory Personalizzabile**: Possibilità di scegliere la cartella di download

## Requisiti

- Python 3.6 o superiore

## Installazione

1. Clona il repository:
```bash
git clone https://github.com/tuousername/FileCast.git
cd FileCast
```

## Utilizzo

### Avvio Server

```bash
python server_gui.py
```

1. Clicca "Start Server" per avviare il server
2. Usa "Select File" per scegliere il file da inviare
3. Monitora i client connessi nella lista

### Avvio Client

```bash
python client_gui.py
```

1. Clicca "Connect" per connettersi al server
2. Usa "Browse" per scegliere la cartella di download
3. Monitora il progresso dei download nella barra di avanzamento

## Struttura del Progetto

```
FileCast/
│
├── server_gui.py    # Interfaccia grafica del server
├── client_gui.py    # Interfaccia grafica del client
├── Server.py        # Logica del server
├── Client.py        # Logica del client
└── README.md        # Questo file
```

## Come Funziona

1. Il server viene avviato e rimane in ascolto
2. I client possono connettersi al server usando l'indirizzo IP locale
3. Quando il server seleziona un file, viene inviato a tutti i client connessi
4. I client salvano i file ricevuti nella directory specificata

## TODO

### Bugfix
- [ ] Sistemare la gestione della chiusura/riapertura dei socket
- [ ] Gestire errori di connessione rifiutata
- [ ] Migliorare la pulizia delle risorse alla chiusura

### Miglioramenti Base
- [ ] Aggiungere notifica di trasferimento completato

### UI
- [ ] Migliorare i messaggi di stato
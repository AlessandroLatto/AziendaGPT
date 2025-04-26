import customtkinter as ctk
from tkinter import scrolledtext
from moduli.backend import set_api_key, set_system_message, get_chatgpt_answer
from tkinter import filedialog
import json

# imposta modalità scura e tema verde per l'interfaccia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def send_message():
    # funzione per inviare un messaggio 
    user_message = user_input.get().strip()
    if not user_message:
        return

    # mostra il messaggio dell'utente nell'area della chat
    chat_area.insert("end", f"You: {user_message}\n", "human_message")
    user_input.delete(0, "end")

    # chiama il backend per ottenere la risposta e la mostra
    try:
        answer = get_chatgpt_answer(user_message)
        chat_area.insert("end", f"AziendaGPT: {answer}\n", "ai_message")
    except Exception as e:
        chat_area.insert("end", f"[Error: {e}]\n", "error")

    # configura i colori per i messaggi
    chat_area.tag_config("ai_message", foreground="lightblue")
    chat_area.tag_config("human_message", foreground="lightgreen")
    chat_area.tag_config("error", foreground="red")

    # scorre automaticamente in basso
    chat_area.see("end")

def settingswindow():
    # finestra per le impostazioni
    settings_window = ctk.CTkToplevel(app)
    settings_window.title("Settings")
    settings_window.geometry("500x700")

    def save_settings():
        # salva la chiave api e il messaggio di sistema
        set_api_key(api_key_entry.get().strip())
        set_system_message(system_message_entry.get("1.0", "end-1c").strip()) # ("1.0", "end-1c") vuol dire tutto il testo. Preso dalla documentazione di customtkinter
        settings_window.destroy()
        chat_area.insert("end", "[impostazioni aggiornate]\n", "info")
        chat_area.tag_config("info", foreground="white")

    def load_defaults():
        # carica valori predefiniti per chiave api e messaggio di sistema
        default_api_key = "DEFAULTS"
        default_system_message = "Tu sei AziendaGPT, un'intelligenza artificiale esperta in gestione aziendale, marketing, strategia d'impresa, finanza e risorse umane. Il tuo obiettivo è aiutare imprenditori, manager e team aziendali a prendere decisioni strategiche, migliorare l'efficienza operativa e aumentare la competitività sul mercato. Offri risposte pratiche, analisi dei dati, consigli personalizzati e soluzioni innovative per ogni tipo di impresa, dalla startup alla multinazionale. Rispondi sempre in modo chiaro, professionale e orientato ai risultati, adattando il linguaggio al livello dell’utente."
        
        api_key_entry.delete(0, "end")
        api_key_entry.insert(0, default_api_key)
        
        system_message_entry.delete("1.0", "end")
        system_message_entry.insert("1.0", default_system_message)
        
        chat_area.insert("end", "[Impostate le opzioni predefinite]\n", "info")
 
    def export_chat_history_to_json():
        # esporta la cronologia della chat in un file json (txt funzione dedicata)
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        chat_history = chat_area.get("1.0", "end-1c").strip().split("\n")
        try:
            with open(file_path, "w") as file:
                json.dump({"chat_history": chat_history}, file, indent=4)
            chat_area.insert("end", "[Cronologia chat esportata]\n", "info")
        except Exception as e:
            chat_area.insert("end", f"[Errore nell'esportazione: {e}]\n", "error")


    def export_chat_history_to_txt():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not file_path:
            return
        try:
            content = chat_area.get("1.0", "end-1c")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            chat_area.insert("end", "[Cronologia chat esportata in .txt]\n", "info")
        except Exception as e:
            chat_area.insert("end", f"[Errore nell'esportazione: {e}]\n", "error")

    def riassunto():
        # genera un riassunto della conversazione
        chat_history = chat_area.get("1.0", "end-1c").strip().split("\n")
        riassunto = get_chatgpt_answer("Riassumi la seguente conversazione in un paragrafo che la descrive:\n" + "\n".join(chat_history))
        chat_area.insert("end", f"[Riassunto: {riassunto}]\n", "info")
        settings_window.destroy()
    
    # interfaccia per inserire chiave api e messaggio di sistema
    ctk.CTkLabel(settings_window, text="OpenAI API Key:").pack(pady=10)
    api_key_entry = ctk.CTkEntry(settings_window,
                                width=250,
                                placeholder_text="Enter your API key")
    api_key_entry.pack(pady=5)

    ctk.CTkLabel(settings_window, text="System Message:").pack(pady=10)
    system_message_entry = ctk.CTkTextbox(settings_window,
                                         width=250,
                                         height=100)
    system_message_entry.pack(pady=5)

    def load_system_message_from_file():
        # carica un messaggio di sistema da un file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                system_message_entry.delete("1.0", "end")
                system_message_entry.insert("1.0", file.read())
            chat_area.insert("end", "[Messaggio di sistema caricato dal file]\n", "info")
        except Exception as e:
            chat_area.insert("end", f"[Errore nel caricamento del file: {e}]\n", "error")

    # pulsanti per salvare, caricare predefiniti, esportare e riassumere
    load_file_button = ctk.CTkButton(settings_window,
                                     text="Carica file...",
                                     command=load_system_message_from_file)
    load_file_button.pack(pady=5)

    save_button = ctk.CTkButton(settings_window,
                                text="Save",
                                command=save_settings)
    save_button.pack(pady=10)

    load_defaults_button = ctk.CTkButton(settings_window, 
                                        text="Carica predefiniti",
                                        command=load_defaults)
    load_defaults_button.pack(pady=10)


    export_button = ctk.CTkButton(settings_window,
                                  text="Esporta cronologia in TXT",
                                  command=export_chat_history_to_txt)
    export_button.pack(pady=10)

    export_json_button = ctk.CTkButton(settings_window,
                                       text="Esporta cronologia in JSON",
                                       command=export_chat_history_to_json)
    export_json_button.pack(pady=10)

    riassunto_chat = ctk.CTkButton(settings_window,
                                   text="Riassunto chat",
                                   command=riassunto)
    riassunto_chat.pack(pady=10)

# finestra principale dell'applicazione
app = ctk.CTk()
app.geometry("400x800")
app.title("AziendaGPT")
# etichetta per mostrare il costo stimato della chat
cost_label = ctk.CTkLabel(app, text="Costo stimato: $0.00")
cost_label.pack(pady=5)

def update_cost_estimate():
    # calcola il costo stimato basato sul numero di token
    chat_history = chat_area.get("1.0", "end-1c").strip()
    token_count = len(chat_history.split())  # stima approssimativa dei token
    cost_per_token = 0.002 / 1000  # costo per token per 3.5-turbo
    estimated_cost = token_count * cost_per_token
    cost_label.configure(text=f"Costo stimato: ${estimated_cost}")
    print(estimated_cost)
    
# area della chat con scorrimento
chat_area = scrolledtext.ScrolledText(app,
                                      wrap="word",
                                      font=("Aptos", 12))
chat_area.bind("<Key>", lambda e: "break")  # disabilita la scrittura manuale nell'area della chat

chat_area.pack(padx=10, pady=10, fill="both", expand=True)

# campo di input per i messaggi dell'utente
user_input = ctk.CTkEntry(app,
                         width=300,
                         placeholder_text="Digita il tuo messaggio...")
user_input.pack(padx=10, pady=5)

# pulsanti per inviare messaggi e aprire le impostazioni
send_button = ctk.CTkButton(app, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

settings_button = ctk.CTkButton(app,
                                text="Settings",
                                command=settingswindow)
settings_button.pack(padx=10, pady=5)

clear_button = ctk.CTkButton(app,
                             text="Pulisci chat",
                             command=lambda: chat_area.delete("1.0", "end"))
clear_button.pack(padx=10, pady=5)

cost_upd = ctk.CTkButton(app,
                             text="Aggiorna costo",
                             command=update_cost_estimate)
cost_upd.pack(padx=10, pady=5)



# avvia l'applicazione
app.mainloop()

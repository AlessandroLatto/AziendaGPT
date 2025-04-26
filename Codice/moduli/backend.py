# moduli/backend.py
from openai import OpenAI

api_key = ""
system_message = ""
chat_history = []
client = None # Necessario per evitare l'errore "Client non definito" se non si imposta una API

def get_default_api_key():
    # Legge la chiave API predefinita da un file di testo
    with open("default_api.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

def set_api_key(new_api_key):
    # Imposta una nuova chiave API o utilizza quella predefinita
    global api_key, client
    if new_api_key.lower() == "defaults":
        api_key = get_default_api_key()
    else:
        api_key = new_api_key
    client = OpenAI(api_key=api_key)  # Inizializza il client OpenAI con la chiave API

def set_system_message(new_system_message):
    # Imposta il messaggio di sistema (o lo resetta se è "steam")
    global system_message
    system_message = new_system_message

def get_chatgpt_answer(message):
    # Invia un messaggio a ChatGPT e restituisce la risposta
    global chat_history, client
    if client is None:
        raise ValueError("API mancante")  # Errore se il client non è stato configurato
    openai_client = client  # Usa il client OpenAI già configurato
    chat_history.append({"role": "user", "content": message})  # Aggiunge il messaggio dell'utente alla cronologia
    messages = [{"role": "system", "content": system_message}] + chat_history  # Combina il messaggio di sistema con la cronologia

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specifica il modello da utilizzare
        messages=messages
    )
    answer = response.choices[0].message.content  # Estrae la risposta dal modello
    chat_history.append({"role": "assistant", "content": answer})  # Aggiunge la risposta alla cronologia
    return answer

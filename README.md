# AziendaGPT – Assistente Virtuale per il Business

**AziendaGPT** è un'applicazione desktop che simula un assistente virtuale intelligente, pensato per supportare aziende di ogni tipo. Sfrutta le API di OpenAI per offrire risposte professionali e personalizzate su temi come strategia d'impresa, marketing, finanza e risorse umane.

L'obiettivo dell'applicazione è fornire uno strumento pratico per manager, imprenditori e team aziendali, facilitando decisioni strategiche e migliorando l'efficienza operativa.

---

## Funzionalità Principali

- **Chat AI in tempo reale**: dialoga con un assistente virtuale esperto in contesti aziendali.
- **Personalizzazione del contesto**: carica un messaggio di sistema per adattare l’AI al tuo settore (es. turismo, sanità, tecnologia).
- **Esportazione conversazioni**: salva la cronologia in formato `.txt` o `.json` per archiviazione o analisi successive.
- **Riassunto automatico**: genera un paragrafo riassuntivo della conversazione, utile per report o follow-up.
- **Stima dei costi**: calcola il costo approssimativo della sessione in base ai token utilizzati dal modello.
- **Interfaccia intuitiva**: design moderno in modalità scura, facile da usare anche per chi non ha competenze tecniche.

---

## Struttura dell'Applicazione

- **Interfaccia Grafica**:
  - Campo input per scrivere messaggi.
  - Area chat con visualizzazione dinamica dei messaggi.
  - Pulsanti per invio, impostazioni, pulizia chat, aggiornamento costo.
- **Finestra Impostazioni**:
  - Inserimento chiave API.
  - Caricamento di un contesto aziendale personalizzato.
  - Funzioni di esportazione chat.
  - Riassunto automatico della conversazione.

---

## Tecnologie Utilizzate

- **customtkinter**: per una GUI moderna e personalizzabile.
- **OpenAI API**: per l’intelligenza artificiale conversazionale.
- **tkinter.scrolledtext**: per la gestione della chat con scorrimento.
- **json**: per la gestione e salvataggio dei dati.


"""
Programma monitor.py per il monitoraggio della cartella C:\\Work\\marconilab.

Il programma registra l'avvio in un file di log e controlla
le modifiche che avvengono nella cartella indicata.
Ogni modifica viene stampata a video e salvata nel file di log.
"""

__author__ = "Carloumbero Olivieri e Simone Volpe"
__version__ = "Rev. 1.3 del 2026-05-26"

from pathlib import Path  # Importa Path, utile per gestire percorsi di file e cartelle in modo semplice
import time  # Importa time, usata per ottenere data e ora da inserire nei log
from watchfiles import watch  # Importa watch, funzione che controlla le modifiche in una cartella

def scrivi_log(messaggio, percorso_log):  # funzione scrivi_log 
    """
    Scrive un messaggio nel file di log.
    Ogni riga del log contiene:
    - data e ora dell'evento;
    - descrizione dell'evento.
    """

    # Crea una stringa con data e ora attuali nel formato anno-mese-giorno ore:minuti:secondi
    orario = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepara la riga da scrivere nel log, inserendo orario e messaggio
    riga = f"[{orario}] {messaggio}\n"

    # Apre il file di log in modalità append, cioè aggiungendo il testo in fondo al file
    with open(percorso_log, mode="a", encoding="utf-8") as f_log:
        f_log.write(riga)  # Scrive la riga nel file di log

    print(riga, end="")  # Stampa la stessa riga anche a video

def monitora_cartella(cartella_da_osservare, percorso_log): # funzione monitora_cartella
    """
    Monitora una cartella e registra nel file di log gli eventi rilevati.
    Gli eventi potranno in futuro essere usati anche per avviare
    operazioni di backup.
    """
    
    # Mostra a video quale cartella viene monitorata
    print(f"Monitoraggio avviato su: {cartella_da_osservare}")

    # watch resta in ascolto e restituisce le modifiche rilevate nella cartella
    for modifiche in watch(cartella_da_osservare):
        
        
        # Ogni modifica contiene il tipo di evento e il percorso del file coinvolto
        for tipo_evento, percorso_file in modifiche:
            # Prepara il messaggio descrittivo dell'evento rilevato
            messaggio = f"- Evento: {tipo_evento.name} | File: {percorso_file}"

            # chiama la funzione scrivi_log per scrivere il messaggio nel file di log 
            scrivi_log(messaggio, percorso_log)
            
def main(): # funzione main
    """
    Stabilisce i percorsi principali, registra l'avvio del programma
    e avvia il monitoraggio della cartella scelta.
    """

    # Percorso della cartella da controllare
    cartella_da_osservare = Path(r"C:\Work\marconilab")
    
    # Percorso relativo del file di log, costruito partendo dalla posizione di questo file Python
    cartella_corrente = Path(__file__).parent  # Cartella in cui si trova monitor.py
    cartella_progetto = cartella_corrente.parent  # Cartella principale del progetto
    file_log = cartella_progetto / "log" / "monitor.log"  # Percorso completo del file di log

    # Registra nel log l'avvio del programma
    scrivi_log("Programma avviato", file_log)

    print(f"--- monitor.py attivo su {cartella_da_osservare} ---") # messaggio da stampare a video
    print("Premi Ctrl + C per fermarlo se sei in console.") # messaggio da stampare a video

    # Avvia il monitoraggio della cartella
    monitora_cartella(cartella_da_osservare, file_log)

if __name__ == "__main__":
    main()  #chiama la funzione main 
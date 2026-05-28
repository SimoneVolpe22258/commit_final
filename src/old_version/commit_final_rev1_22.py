"""
Programma per il monitoraggio della cartella C:\Work\marconilab.

Il programma registra l'avvio in un file di log e controlla
le modifiche che avvengono nella cartella indicata.
Ogni modifica viene stampata a video (per ora) e inserita nel
File di log.
"""

__author__= "Carloumbero Olivieri e Simone Volpe"
__version__ ="Rev. 1.2 del 2026-05-21"

import os
import time
from watchfiles import watch

def scrivi_log(messaggio, percorso_log):
    """
    Scrive un messaggio nel file di log.

    Ogni riga del log contiene:
    - data e ora dell'evento;
    - descrizione dell'evento.
    """

    orario = time.strftime("%Y-%m-%d %H:%M:%S")
    riga = f"[{orario}] {messaggio}\n"

    with open(percorso_log, mode="a", encoding="utf-8") as f_log:
        f_log.write(riga)

    print(riga, end="")

def monitora_cartella(cartella_da_osservare, percorso_log):
    """
    Gli eventi rilevati vengono inviati al file di log
    e successivamente potranno essere usati per il backup.
    """
    
    print(f"Monitoraggio avviato su: {cartella_da_osservare}")

    for modifiche in watch(cartella_da_osservare):
        scrivi_log("Modifica rilevata:", percorso_log)
        
        for tipo_evento, percorso_file in modifiche:
            messaggio = f"- Evento: {tipo_evento.name} | File: {percorso_file}"
            scrivi_log(messaggio, percorso_log)
            
def main():
    """
    Funzione principale del programma.

    Stabilisce i percorsi principali, registra l'avvio del programma
    e avvia il controllo della cartella del cliente.
    """

    cartella_da_osservare = r"C:\Work\marconilab"
    file_log = r"..\log\monitor.log"

    scrivi_log("Programma avviato", file_log)

    print(f"--- commit_final attivo su {cartella_da_osservare} ---")
    print("Premi Ctrl + C per fermarlo se sei in console.")

    monitora_cartella(cartella_da_osservare, file_log)

if __name__ == "__main__":
    main()
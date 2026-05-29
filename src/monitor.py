"""
Programma monitor.py per il monitoraggio della cartella C:\\Work\\marconilab.

Il programma registra l'avvio in un file di log e controlla
le modifiche che avvengono nella cartella indicata.
Ogni modifica viene stampata a video (per ora) e inserita nel
File di log.
"""

__author__= "Carloumberto Olivieri e Simone Volpe"
__version__ ="Rev. 2.0 del 2026-05-28"

from pathlib import Path
import time
from watchfiles import watch

def percorsi_conf():
    """ Funzione per recuperare percorsi dei file esteni da "conf.con"
    restituisco i tre valori corrispondenti ai percorsi.
    """
    path_cartella_da_osservare = 0
    path_cartella_backup = 0
        
    with open("conf.conf", "r") as p:
        for riga in p:
            riga = riga.strip()
            chiave, valore = riga.split("=")
            valore = valore.strip('"')
            if chiave == "path_cartella_da_osservare":
                path_cartella_da_osservare = valore
                
            elif chiave == "path_cartella_backup":
                path_cartella_backup = valore
                                  
        return path_cartella_da_osservare, path_cartella_backup
    
    
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
        # scrivi_log("Modifica rilevata:", percorso_log) Riga che crea confusione nel log
        
        for tipo_evento, percorso_file in modifiche:
            messaggio = f"- Evento: {tipo_evento.name} | File: {percorso_file}"
            scrivi_log(messaggio, percorso_log)


def backup():
    """
    Funzione che si occupa del backup in luogo di modifica file.
    """
    # return


def main():
    """
    Stabilisce i percorsi principali, registra l'avvio del programma
    e avvia il controllo della cartella del cliente.
    """
    path_cartella_da_osservare, path_cartella_backup = percorsi_conf()
    cartella_da_osservare = Path(path_cartella_da_osservare)
    cartella_backup= Path(path_cartella_backup)
    
    cartella_corrente = Path(__file__).parent
    cartella_progetto = cartella_corrente.parent 
    file_log = cartella_progetto / "log" / "monitor.log"
    # path_backup = "\\w11STAT-18-216\work2\backup"
    scrivi_log("Programma avviato", file_log)

    print(f"--- monitor.py attivo su {cartella_da_osservare} ---")
    print("Premi Ctrl + C per fermarlo se sei in console.")

    monitora_cartella(cartella_da_osservare, file_log)

if __name__ == "__main__":
    main()

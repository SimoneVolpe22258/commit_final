"""
Programma monitor.py per il monitoraggio della cartella C:\\Work\\marconilab.

Il programma registra l'avvio in un file di log e controlla
le modifiche che avvengono nella cartella indicata.
Ogni modifica viene stampata a video e inserita nel
File di log. successivamente il nuovo file viene copiato in cartella
"""

__author__= "Carloumberto Olivieri e Simone Volpe"
__version__ ="Rev. 3.2 del 2026-05-29"

from pathlib import Path
import time
from watchfiles import watch
import shutil


def percorsi_conf(percorso_conf):
    """ Funzione per recuperare percorsi dei file esteni da "conf.con"
    restituisco i tre valori corrispondenti ai percorsi.
    """
    sottocartelle = []
    
    path_cartella_da_osservare = 0
    path_cartella_backup = 0
        
    with open(percorso_conf, "r") as p:
        for riga in p:
            riga = riga.strip() # Toglie spazi bianchi a inizio e fine riga
            
            # --- LO SCUDO DI SICUREZZA ---
            # 1. Se la riga è vuota, salta.
            # 2. Se la riga inizia con #, è un commento, quindi salta.
            # 3. Per sicurezza, se manca il simbolo '=', non possiamo fare lo split, quindi salta.
            if not riga or riga.startswith("#") or "=" not in riga:
                continue                 
            
            chiave, valore = riga.split("=")
            valore = valore.strip('"')
            
            
            if chiave == "path_cartella_da_osservare":
                path_cartella_da_osservare = valore
                
            elif chiave == "path_cartella_backup":
                path_cartella_backup = valore
                
            elif chiave == "sottocartelle_da_monitorare":
                sottocartelle = valore.split(",")
            
                                  
    return path_cartella_da_osservare, path_cartella_backup, sottocartelle
    
    
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


def monitora_cartella(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle):
    """
    Monitora la cartella e aggiorna costantemente la cartella di backup.
    """

    print(f"Monitoraggio avviato su: {cartella_da_osservare}")

    for modifiche in watch(cartella_da_osservare):
        for tipo_evento, percorso_file in modifiche:
            percorso_file = Path(percorso_file)
            # Controllo di sicurezza: il file fa parte delle cartelle configurate?
            consentito = False
            for cartella in sottocartelle:
                if cartella in percorso_file.parts:
                    consentito = True
                    break
            
            if not consentito:
                continue # Ignora il file se non è in una cartella monitorata

            messaggio = f"- Evento: {tipo_evento.name} | File: {percorso_file}"
            scrivi_log(messaggio, percorso_log)

            backup(percorso_file, cartella_da_osservare, cartella_backup, percorso_log)
            

def backup(sorgente, cartella_da_osservare, cartella_backup, percorso_log):
    """
    Copia il file modificato nella cartella di backup,
    mantenendo la stessa struttura della cartella monitorata.
    """

    sorgente = Path(sorgente)

    if not sorgente.is_file():
        return

    try:
        percorso_relativo = sorgente.relative_to(cartella_da_osservare)
        destinazione = cartella_backup / percorso_relativo

        destinazione.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(sorgente, destinazione)

        scrivi_log(f"Backup aggiornato: {destinazione}", percorso_log)
        
    except Exception as e:
        scrivi_log(f"Errore durante il backup di {sorgente}: {e}", percorso_log)
        
def main():
    """
    Stabilisce i percorsi principali, registra l'avvio del programma
    e avvia il controllo della cartella del cliente.
    """
    cartella_corrente = Path(__file__).parent
    cartella_progetto = cartella_corrente.parent
    
    conf_conf = cartella_progetto / "src" / "conf.conf"
    
    path_cartella_da_osservare, path_cartella_backup, lista_sottocartelle = percorsi_conf(conf_conf)

    cartella_da_osservare = Path(path_cartella_da_osservare)
    cartella_backup = Path(path_cartella_backup)
        
    file_log = cartella_progetto / "log" / "monitor.log"
    
    
    file_log.parent.mkdir(parents=True, exist_ok=True)

    scrivi_log("Programma avviato", file_log)

    print(f"--- monitor.py attivo su {cartella_da_osservare} ---")
    print("Premi Ctrl + C per fermarlo se sei in console.")

    monitora_cartella(cartella_da_osservare, cartella_backup, file_log, lista_sottocartelle)

if __name__ == "__main__":
    main()

"""
Programma monitor.py per il monitoraggio della cartella C:\\Work\\marconilab.

Il log contiene solo informazioni di esecuzione del programma.
Gli eventi sui file vengono salvati nel file CSV configurato in conf.conf.
"""

__author__ = "Carloumberto Olivieri e Simone Volpe"
__version__ = "Rev. 4.0 del 2026-06-04"

from pathlib import Path
import time
from watchfiles import watch
import shutil


def percorsi_conf(percorso_conf):
    """
    Legge il file conf.conf e recupera i percorsi usati dal programma.
    Le righe vuote e i commenti vengono ignorati.
    """
    cartella_da_osservare = ""
    cartella_backup = ""
    sottocartelle = []
    file_csv = ""

    with open(percorso_conf, "r", encoding="utf-8") as file:
        for riga in file:
            riga = riga.strip()

            if riga == "" or riga.startswith("#") or "=" not in riga:
                continue

            chiave, valore = riga.split("=", 1)
            chiave = chiave.strip()
            valore = valore.strip().strip('"')

            if chiave == "path_cartella_da_osservare":
                cartella_da_osservare = valore
            elif chiave == "path_cartella_backup":
                cartella_backup = valore
            elif chiave == "sottocartelle_da_monitorare":
                sottocartelle = valore.split(",")
            elif chiave == "path_file_csv":
                file_csv = valore

    return cartella_da_osservare, cartella_backup, sottocartelle, file_csv


def scrivi_log(messaggio, percorso_log):
    """
    Scrive nel log solo informazioni di esecuzione.
    """
    orario = time.strftime("%Y-%m-%d %H:%M:%S")
    riga = f"[{orario}] {messaggio}\n"

    with open(percorso_log, "a", encoding="utf-8") as file:
        file.write(riga)

    print(riga, end="")


def scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, backup):
    """
    Scrive nel CSV i dati dei file monitorati.
    Non usa la libreria csv.
    """
    percorso_file = Path(percorso_file)
    orario = time.strftime("%Y-%m-%d %H:%M:%S")

    file_da_scrivere = percorso_file.relative_to(cartella_da_osservare)

    if percorso_file.is_file():
        dimensione = percorso_file.stat().st_size
        ultima_modifica = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(percorso_file.stat().st_mtime))
    else:
        dimensione = "N/D"
        ultima_modifica = "N/D"

    intestazione = "data_ora;evento;file;dimensione;ultima_modifica;backup\n"
    riga = f"{orario};{evento};{file_da_scrivere};{dimensione};{ultima_modifica};{backup}\n"

    if not percorso_csv.exists():
        with open(percorso_csv, "w", encoding="utf-8") as file:
            file.write(intestazione)

    with open(percorso_csv, "a", encoding="utf-8") as file:
        file.write(riga)


def backup(percorso_file, cartella_da_osservare, cartella_backup, percorso_log):
    """
    Copia il file nella cartella di backup mantenendo la struttura originale.
    Restituisce OK oppure ERRORE.
    """
    try:
        percorso_relativo = percorso_file.relative_to(cartella_da_osservare)
        destinazione = cartella_backup / percorso_relativo

        destinazione.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(percorso_file, destinazione)
        scrivi_log(f"Backup aggiornato: {destinazione}", percorso_log)

        return "OK"

    except Exception as errore:
        scrivi_log(f"Errore durante il backup di {percorso_file}: {errore}", percorso_log)
        return "ERRORE"


def file_in_cartelle_monitorate(percorso_file, sottocartelle):
    """
    Controlla se il file si trova in una delle sottocartelle indicate in conf.conf.
    """
    for cartella in sottocartelle:
        cartella = cartella.strip()

        if cartella in percorso_file.parts:
            return True

    return False


def traduci_evento(evento_watch):
    """
    Converte i nomi degli eventi della libreria watchfiles in italiano.
    """
    if evento_watch == "added":
        return "creazione"
    elif evento_watch == "modified":
        return "modifica"
    elif evento_watch == "deleted":
        return "eliminazione"
    else:
        return evento_watch


def monitora_cartella(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv):
    """
    Controlla la cartella monitorata.
    Gli eventi sui file vengono scritti nel CSV.
    """
    print(f"Monitoraggio avviato su: {cartella_da_osservare}")

    for modifiche in watch(cartella_da_osservare):
        for tipo_evento, percorso_file in modifiche:
            percorso_file = Path(percorso_file)
            evento = traduci_evento(tipo_evento.name)

            if not file_in_cartelle_monitorate(percorso_file, sottocartelle):
                continue

            if evento == "eliminazione":
                scrivi_log("Eliminato file nella cartella monitorata", percorso_log)
                scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, "NON CANCELLATO")
                continue

            if not percorso_file.is_file():
                continue

            risultato_backup = backup(percorso_file, cartella_da_osservare, cartella_backup, percorso_log)
            scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, risultato_backup)


def main():
    """
    Prepara i percorsi, avvia il log e poi il monitoraggio.
    """
    cartella_corrente = Path(__file__).parent
    cartella_progetto = cartella_corrente.parent

    percorso_conf = cartella_progetto / "src" / "conf.conf"
    percorso_log = cartella_progetto / "log" / "monitor.log"

    path_osservare, path_backup, sottocartelle, path_csv = percorsi_conf(percorso_conf)

    cartella_da_osservare = Path(path_osservare)
    cartella_backup = Path(path_backup)
    percorso_csv = Path(path_csv)

    if not percorso_csv.is_absolute():
        percorso_csv = cartella_corrente / percorso_csv

    percorso_log.parent.mkdir(parents=True, exist_ok=True)
    percorso_csv.parent.mkdir(parents=True, exist_ok=True)

    scrivi_log("Programma avviato", percorso_log)

    print(f"--- monitor.py attivo su {cartella_da_osservare} ---")
    print("Premi Ctrl + C per fermarlo se sei in console.")

    try:
        monitora_cartella(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv)
    except KeyboardInterrupt:
        scrivi_log("Programma terminato dall'utente", percorso_log)
        print("\nMonitoraggio interrotto.")


if __name__ == "__main__":
    main()
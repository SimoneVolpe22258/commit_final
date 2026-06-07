"""
Programma monitor.py per il monitoraggio della cartella C:\\Work\\marconilab.

Il log contiene informazioni di esecuzione del programma.
Gli eventi sui file vengono salvati nel file CSV configurato in conf.conf.
"""

__author__ = "Carloumberto Olivieri e Simone Volpe"
__version__ = "Rev. 5.1 del 2026-06-06"

from pathlib import Path
import csv
import shutil
import time
from watchfiles import watch


INTESTAZIONE_CSV = [
    "data_ora",
    "evento",
    "file",
    "percorso_completo",
    "dimensione",
    "ultima_modifica",
    "backup",
]


def timestamp():
    """
    Restituisce data e ora nel formato usato da log e CSV.
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")


def percorsi_conf(percorso_conf):
    """
    Legge il file conf.conf e recupera i percorsi usati dal programma.
    Le righe vuote e i commenti vengono ignorati.
    """
    if not percorso_conf.exists():
        raise FileNotFoundError(f"File di configurazione non trovato: {percorso_conf}")

    configurazione = {}

    with open(percorso_conf, "r", encoding="utf-8") as file:
        for numero_riga, riga in enumerate(file, start=1):
            riga = riga.strip()

            if riga == "" or riga.startswith("#"):
                continue

            if "=" not in riga:
                raise ValueError(f"Riga {numero_riga} non valida nel file conf.conf: {riga}")

            chiave, valore = riga.split("=", 1)
            configurazione[chiave.strip()] = valore.strip().strip('"')

    chiavi_obbligatorie = [
        "path_cartella_da_osservare",
        "path_cartella_backup",
        "sottocartelle_da_monitorare",
        "path_file_csv",
    ]

    for chiave in chiavi_obbligatorie:
        if chiave not in configurazione or configurazione[chiave].strip() == "":
            raise ValueError(f"Valore mancante nel file conf.conf: {chiave}")

    sottocartelle = [
        cartella.strip()
        for cartella in configurazione["sottocartelle_da_monitorare"].split(",")
        if cartella.strip() != ""
    ]

    if not sottocartelle:
        raise ValueError("Nessuna sottocartella da monitorare indicata nel file conf.conf")

    return (
        configurazione["path_cartella_da_osservare"],
        configurazione["path_cartella_backup"],
        sottocartelle,
        configurazione["path_file_csv"],
    )


def scrivi_log(messaggio, percorso_log, livello="INFO"):
    """
    Scrive nel log informazioni di esecuzione con livello e messaggio dettagliato.
    """
    riga = f"[{timestamp()}] [{livello}] {messaggio}\n"

    percorso_log.parent.mkdir(parents=True, exist_ok=True)

    with open(percorso_log, "a", encoding="utf-8") as file:
        file.write(riga)

    print(riga, end="")


def percorso_relativo_sicuro(percorso_file, cartella_da_osservare):
    """
    Restituisce il percorso relativo se possibile, altrimenti il nome del file.
    Evita errori bloccanti in caso di percorsi anomali.
    """
    try:
        return percorso_file.relative_to(cartella_da_osservare)
    except ValueError:
        return percorso_file.name


def scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, risultato_backup):
    """
    Scrive nel CSV i dati dei file monitorati usando la libreria csv.
    """
    percorso_file = Path(percorso_file)
    file_da_scrivere = percorso_relativo_sicuro(percorso_file, cartella_da_osservare)

    if percorso_file.is_file():
        stat_file = percorso_file.stat()
        dimensione = stat_file.st_size
        ultima_modifica = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_file.st_mtime))
    else:
        dimensione = "N/D"
        ultima_modifica = "N/D"

    percorso_csv.parent.mkdir(parents=True, exist_ok=True)
    file_esiste = percorso_csv.exists()

    with open(percorso_csv, "a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")

        if not file_esiste:
            writer.writerow(INTESTAZIONE_CSV)

        writer.writerow([
            timestamp(),
            evento,
            str(file_da_scrivere),
            str(percorso_file),
            dimensione,
            ultima_modifica,
            risultato_backup,
        ])


def esegui_backup(percorso_file, cartella_da_osservare, cartella_backup, percorso_log):
    """
    Copia il file nella cartella di backup mantenendo la struttura originale.
    Restituisce OK oppure ERRORE.
    """
    try:
        percorso_relativo = percorso_file.relative_to(cartella_da_osservare)
        destinazione = cartella_backup / percorso_relativo

        destinazione.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(percorso_file, destinazione)
        scrivi_log(f"Backup aggiornato | origine={percorso_file} | destinazione={destinazione}", percorso_log)

        return "OK"

    except Exception as errore:
        scrivi_log(f"Backup fallito | file={percorso_file} | errore={errore}", percorso_log, "ERRORE")
        return "ERRORE"


def file_in_cartelle_monitorate(percorso_file, cartella_da_osservare, sottocartelle):
    """
    Controlla se il file si trova dentro una delle sottocartelle indicate in conf.conf.
    Se nel conf.conf è indicato *, monitora tutte le sottocartelle.
    """
    try:
        percorso_relativo = percorso_file.relative_to(cartella_da_osservare)
    except ValueError:
        return False

    if not percorso_relativo.parts:
        return False

    if "*" in sottocartelle:
        return True

    return percorso_relativo.parts[0] in sottocartelle


def valida_percorsi(cartella_da_osservare, cartella_backup, percorso_csv, percorso_log):
    """
    Verifica che i percorsi principali siano utilizzabili prima di avviare il monitoraggio.
    """
    if not cartella_da_osservare.exists():
        raise FileNotFoundError(f"Cartella da osservare inesistente: {cartella_da_osservare}")

    if not cartella_da_osservare.is_dir():
        raise NotADirectoryError(f"Il percorso da osservare non è una cartella: {cartella_da_osservare}")

    cartella_backup.mkdir(parents=True, exist_ok=True)
    percorso_csv.parent.mkdir(parents=True, exist_ok=True)
    percorso_log.parent.mkdir(parents=True, exist_ok=True)


def controlla_backup_iniziale(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv):
    """
    All'avvio confronta i file della cartella osservata con quelli nella cartella di backup.
    Scrive nel log e nel CSV i file mancanti nel backup o meno recenti.

    Il controllo NON copia i file: serve solo per fare una verifica dettagliata
    prima di avviare il monitoraggio in tempo reale.
    """
    scrivi_log("Controllo iniziale backup avviato", percorso_log)

    totale_file_controllati = 0
    totale_mancanti = 0
    totale_meno_recenti = 0
    totale_errori = 0

    inizio = time.time()

    for percorso_file in cartella_da_osservare.rglob("*"):
        try:
            if not percorso_file.is_file():
                continue

            if not file_in_cartelle_monitorate(percorso_file, cartella_da_osservare, sottocartelle):
                continue

            totale_file_controllati += 1

            percorso_relativo = percorso_file.relative_to(cartella_da_osservare)
            file_backup = cartella_backup / percorso_relativo

            if not file_backup.exists():
                totale_mancanti += 1
                messaggio = f"Backup mancante | origine={percorso_file} | atteso={file_backup}"
                scrivi_log(messaggio, percorso_log, "AVVISO")
                scrivi_csv(
                    percorso_csv,
                    "controllo_iniziale",
                    percorso_file,
                    cartella_da_osservare,
                    "MANCANTE IN BACKUP",
                )
                continue

            if not file_backup.is_file():
                totale_errori += 1
                messaggio = f"Backup non valido: il percorso esiste ma non è un file | backup={file_backup}"
                scrivi_log(messaggio, percorso_log, "ERRORE")
                scrivi_csv(
                    percorso_csv,
                    "controllo_iniziale",
                    percorso_file,
                    cartella_da_osservare,
                    "ERRORE - BACKUP NON E' UN FILE",
                )
                continue

            stat_origine = percorso_file.stat()
            stat_backup = file_backup.stat()

            # Tolleranza di 1 secondo per evitare falsi positivi dovuti al filesystem.
            backup_piu_vecchio = stat_backup.st_mtime < (stat_origine.st_mtime - 1)
            dimensione_diversa = stat_backup.st_size != stat_origine.st_size

            if backup_piu_vecchio or dimensione_diversa:
                totale_meno_recenti += 1
                ultima_origine = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_origine.st_mtime))
                ultima_backup = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat_backup.st_mtime))
                messaggio = (
                    "Backup non aggiornato | "
                    f"origine={percorso_file} | backup={file_backup} | "
                    f"modifica_origine={ultima_origine} | modifica_backup={ultima_backup} | "
                    f"dimensione_origine={stat_origine.st_size} | dimensione_backup={stat_backup.st_size}"
                )
                scrivi_log(messaggio, percorso_log, "AVVISO")
                scrivi_csv(
                    percorso_csv,
                    "controllo_iniziale",
                    percorso_file,
                    cartella_da_osservare,
                    "BACKUP NON AGGIORNATO",
                )

        except Exception as errore:
            totale_errori += 1
            scrivi_log(
                f"Errore durante controllo iniziale backup | file={percorso_file} | errore={errore}",
                percorso_log,
                "ERRORE",
            )

    durata = round(time.time() - inizio, 2)
    scrivi_log(
        "Controllo iniziale backup completato | "
        f"file_controllati={totale_file_controllati} | "
        f"mancanti={totale_mancanti} | "
        f"non_aggiornati={totale_meno_recenti} | "
        f"errori={totale_errori} | "
        f"durata_secondi={durata}",
        percorso_log,
    )


def monitora_cartella(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv):
    """
    Controlla la cartella monitorata.
    Gli eventi sui file vengono scritti nel CSV.
    """
    scrivi_log(f"Monitoraggio avviato | cartella={cartella_da_osservare}", percorso_log)
    scrivi_log(f"Sottocartelle monitorate | {', '.join(sottocartelle)}", percorso_log)

    for modifiche in watch(cartella_da_osservare):
        for tipo_evento, percorso_file in modifiche:
            percorso_file = Path(percorso_file)
            evento = tipo_evento.name

            if not file_in_cartelle_monitorate(percorso_file, cartella_da_osservare, sottocartelle):
                continue

            try:
                if evento == "deleted":
                    scrivi_log(f"File eliminato | file={percorso_file}", percorso_log, "AVVISO")
                    scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, "NON ESEGUITO - FILE ELIMINATO")
                    continue

                if not percorso_file.is_file():
                    scrivi_log(f"Evento ignorato: non è un file | evento={evento} | percorso={percorso_file}", percorso_log)
                    continue

                scrivi_log(f"Evento rilevato | evento={evento} | file={percorso_file}", percorso_log)
                risultato_backup = esegui_backup(percorso_file, cartella_da_osservare, cartella_backup, percorso_log)
                scrivi_csv(percorso_csv, evento, percorso_file, cartella_da_osservare, risultato_backup)

            except Exception as errore:
                scrivi_log(f"Errore nella gestione evento | evento={evento} | file={percorso_file} | errore={errore}", percorso_log, "ERRORE")


def main():
    """
    Prepara i percorsi, avvia il log e poi il monitoraggio.
    """
    cartella_corrente = Path(__file__).parent
    cartella_progetto = cartella_corrente.parent

    percorso_conf = cartella_progetto / "src" / "conf.conf"
    percorso_log = cartella_progetto / "log" / "monitor.log"

    try:
        path_osservare, path_backup, sottocartelle, path_csv = percorsi_conf(percorso_conf)

        cartella_da_osservare = Path(path_osservare)
        cartella_backup = Path(path_backup)
        percorso_csv = Path(path_csv)

        if not percorso_csv.is_absolute():
            percorso_csv = cartella_corrente / percorso_csv

        valida_percorsi(cartella_da_osservare, cartella_backup, percorso_csv, percorso_log)

        scrivi_log("Programma avviato", percorso_log)
        scrivi_log(f"CSV eventi | percorso={percorso_csv}", percorso_log)
        scrivi_log(f"Cartella backup | percorso={cartella_backup}", percorso_log)

        controlla_backup_iniziale(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv)

        print(f"--- monitor.py attivo su {cartella_da_osservare} ---")
        print("Premi Ctrl + C per fermarlo se sei in console.")

        monitora_cartella(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv)

    except KeyboardInterrupt:
        scrivi_log("Programma terminato dall'utente", percorso_log)
        print("\nMonitoraggio interrotto.")
    except Exception as errore:
        try:
            scrivi_log(f"Programma terminato per errore | errore={errore}", percorso_log, "ERRORE")
        except Exception:
            print(f"Errore: {errore}")


if __name__ == "__main__":
    main()

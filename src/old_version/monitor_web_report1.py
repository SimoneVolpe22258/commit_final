"""
Programma monitor.py per il monitoraggio della cartella C:\Work\marconilab.

Il log contiene informazioni di esecuzione del programma.
Gli eventi sui file vengono salvati nel file CSV configurato in conf.conf.

Versione con:
- controllo iniziale del backup;
- pagina web locale http://127.0.0.1:5000 per visualizzare file mancanti/non aggiornati;
- copia manuale nel backup dei file selezionati dalla pagina web.
"""

__author__ = "Carloumberto Olivieri e Simone Volpe"
__version__ = "Rev. 4.3 del 2026-06-06"

from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import csv
import html
import shutil
import threading
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

PORTA_SERVER_WEB = 5000
HOST_SERVER_WEB = "127.0.0.1"


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



def formatta_data_modifica(timestamp_file):
    """
    Converte un timestamp del filesystem in testo leggibile.
    """
    if timestamp_file is None:
        return "N/D"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_file))


def trova_file_non_coerenti(cartella_da_osservare, cartella_backup, sottocartelle):
    """
    Restituisce una lista di file mancanti nel backup o con backup non aggiornato.
    Non copia nulla: serve per il report web e per il controllo iniziale.
    """
    risultati = []

    for percorso_file in cartella_da_osservare.rglob("*"):
        try:
            if not percorso_file.is_file():
                continue

            if not file_in_cartelle_monitorate(percorso_file, cartella_da_osservare, sottocartelle):
                continue

            percorso_relativo = percorso_file.relative_to(cartella_da_osservare)
            file_backup = cartella_backup / percorso_relativo
            stat_origine = percorso_file.stat()

            record = {
                "id": str(percorso_relativo).replace("\\", "/"),
                "file": str(percorso_relativo),
                "origine": percorso_file,
                "backup": file_backup,
                "dimensione_origine": stat_origine.st_size,
                "dimensione_backup": "N/D",
                "modifica_origine": formatta_data_modifica(stat_origine.st_mtime),
                "modifica_backup": "N/D",
                "stato": "",
            }

            if not file_backup.exists():
                record["stato"] = "MANCANTE IN BACKUP"
                risultati.append(record)
                continue

            if not file_backup.is_file():
                record["stato"] = "ERRORE - BACKUP NON E' UN FILE"
                risultati.append(record)
                continue

            stat_backup = file_backup.stat()
            record["dimensione_backup"] = stat_backup.st_size
            record["modifica_backup"] = formatta_data_modifica(stat_backup.st_mtime)

            # Tolleranza di 1 secondo per evitare falsi positivi dovuti al filesystem.
            backup_piu_vecchio = stat_backup.st_mtime < (stat_origine.st_mtime - 1)
            dimensione_diversa = stat_backup.st_size != stat_origine.st_size

            if backup_piu_vecchio or dimensione_diversa:
                record["stato"] = "BACKUP NON AGGIORNATO"
                risultati.append(record)

        except Exception as errore:
            risultati.append({
                "id": str(percorso_file),
                "file": str(percorso_file),
                "origine": percorso_file,
                "backup": "N/D",
                "dimensione_origine": "N/D",
                "dimensione_backup": "N/D",
                "modifica_origine": "N/D",
                "modifica_backup": "N/D",
                "stato": f"ERRORE CONTROLLO: {errore}",
            })

    risultati.sort(key=lambda elemento: (elemento["stato"], elemento["file"].lower()))
    return risultati


def controlla_backup_iniziale(cartella_da_osservare, cartella_backup, percorso_log, sottocartelle, percorso_csv):
    """
    All'avvio confronta i file della cartella osservata con quelli nella cartella di backup.
    Scrive nel log e nel CSV i file mancanti nel backup o meno recenti.
    """
    scrivi_log("Controllo iniziale backup avviato", percorso_log)
    inizio = time.time()

    risultati = trova_file_non_coerenti(cartella_da_osservare, cartella_backup, sottocartelle)

    totale_mancanti = 0
    totale_meno_recenti = 0
    totale_errori = 0

    for record in risultati:
        stato = record["stato"]
        if stato == "MANCANTE IN BACKUP":
            totale_mancanti += 1
            scrivi_log(f"Backup mancante | origine={record['origine']} | atteso={record['backup']}", percorso_log, "AVVISO")
        elif stato == "BACKUP NON AGGIORNATO":
            totale_meno_recenti += 1
            scrivi_log(
                "Backup non aggiornato | "
                f"origine={record['origine']} | backup={record['backup']} | "
                f"modifica_origine={record['modifica_origine']} | modifica_backup={record['modifica_backup']} | "
                f"dimensione_origine={record['dimensione_origine']} | dimensione_backup={record['dimensione_backup']}",
                percorso_log,
                "AVVISO",
            )
        else:
            totale_errori += 1
            scrivi_log(f"Problema controllo backup | file={record['file']} | stato={stato}", percorso_log, "ERRORE")

        scrivi_csv(percorso_csv, "controllo_iniziale", record["origine"], cartella_da_osservare, stato)

    durata = round(time.time() - inizio, 2)
    scrivi_log(
        "Controllo iniziale backup completato | "
        f"mancanti={totale_mancanti} | "
        f"non_aggiornati={totale_meno_recenti} | "
        f"errori={totale_errori} | "
        f"durata_secondi={durata}",
        percorso_log,
    )


def copia_file_selezionati(id_file_selezionati, cartella_da_osservare, cartella_backup, sottocartelle, percorso_log, percorso_csv):
    """
    Copia nel backup i file selezionati dalla pagina web.
    Per sicurezza copia solo file realmente dentro la cartella monitorata e nelle sottocartelle abilitate.
    """
    risultati = []

    for id_file in id_file_selezionati:
        try:
            id_file = id_file.replace("/", "\\") if "\\" in str(cartella_da_osservare) else id_file
            percorso_origine = (cartella_da_osservare / id_file).resolve()
            cartella_base = cartella_da_osservare.resolve()

            try:
                percorso_origine.relative_to(cartella_base)
            except ValueError:
                risultati.append((id_file, "ERRORE - file fuori dalla cartella monitorata"))
                continue

            if not percorso_origine.is_file():
                risultati.append((id_file, "ERRORE - file origine non trovato"))
                continue

            if not file_in_cartelle_monitorate(percorso_origine, cartella_da_osservare, sottocartelle):
                risultati.append((id_file, "ERRORE - file fuori dalle sottocartelle monitorate"))
                continue

            risultato_backup = esegui_backup(percorso_origine, cartella_da_osservare, cartella_backup, percorso_log)
            scrivi_csv(percorso_csv, "copia_da_pagina_web", percorso_origine, cartella_da_osservare, risultato_backup)
            risultati.append((id_file, risultato_backup))

        except Exception as errore:
            scrivi_log(f"Errore copia da pagina web | file={id_file} | errore={errore}", percorso_log, "ERRORE")
            risultati.append((id_file, f"ERRORE - {errore}"))

    return risultati


def genera_html_report(cartella_da_osservare, cartella_backup, sottocartelle, messaggio=""):
    """
    Genera la pagina HTML del report. Il controllo viene rifatto ogni volta che la pagina viene aperta.
    """
    risultati = trova_file_non_coerenti(cartella_da_osservare, cartella_backup, sottocartelle)
    righe = []

    for record in risultati:
        id_html = html.escape(record["id"], quote=True)
        stato = html.escape(record["stato"])
        file = html.escape(record["file"])
        origine = html.escape(str(record["origine"]))
        backup = html.escape(str(record["backup"]))
        modifica_origine = html.escape(str(record["modifica_origine"]))
        modifica_backup = html.escape(str(record["modifica_backup"]))
        dimensione_origine = html.escape(str(record["dimensione_origine"]))
        dimensione_backup = html.escape(str(record["dimensione_backup"]))

        righe.append(f"""
            <tr>
                <td><input type="checkbox" name="file" value="{id_html}"></td>
                <td><strong>{stato}</strong></td>
                <td>{file}</td>
                <td>{modifica_origine}</td>
                <td>{modifica_backup}</td>
                <td>{dimensione_origine}</td>
                <td>{dimensione_backup}</td>
                <td class="percorso">{origine}</td>
                <td class="percorso">{backup}</td>
            </tr>
        """)

    if not righe:
        corpo_tabella = """
            <tr><td colspan="9" class="ok">Nessuna anomalia trovata: backup coerente.</td></tr>
        """
    else:
        corpo_tabella = "\n".join(righe)

    messaggio_html = ""
    if messaggio:
        messaggio_html = f"<div class='messaggio'>{html.escape(messaggio)}</div>"

    return f"""<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Report coerenza backup</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; background: #f5f5f5; color: #222; }}
        h1 {{ margin-bottom: 4px; }}
        .box {{ background: white; padding: 18px; border-radius: 10px; box-shadow: 0 1px 5px #ccc; }}
        .info {{ color: #555; margin-bottom: 16px; }}
        .messaggio {{ background: #e8f4ff; border: 1px solid #8cc8ff; padding: 10px; margin: 12px 0; border-radius: 6px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th, td {{ border-bottom: 1px solid #ddd; padding: 8px; vertical-align: top; }}
        th {{ background: #eee; text-align: left; position: sticky; top: 0; }}
        .percorso {{ font-size: 12px; color: #555; word-break: break-all; }}
        .ok {{ text-align: center; padding: 20px; color: #197a28; font-weight: bold; }}
        button {{ padding: 10px 14px; margin: 10px 8px 10px 0; cursor: pointer; border-radius: 6px; border: 1px solid #777; }}
        .primario {{ background: #1f6feb; color: white; border-color: #1f6feb; }}
        .azioni {{ margin: 12px 0; }}
    </style>
    <script>
        function selezionaTutti(valore) {{
            document.querySelectorAll('input[name="file"]').forEach(c => c.checked = valore);
        }}
    </script>
</head>
<body>
    <div class="box">
        <h1>Report coerenza backup</h1>
        <div class="info">
            Generato: {html.escape(timestamp())}<br>
            Cartella monitorata: {html.escape(str(cartella_da_osservare))}<br>
            Cartella backup: {html.escape(str(cartella_backup))}<br>
            File non coerenti trovati: <strong>{len(risultati)}</strong>
        </div>
        {messaggio_html}
        <form method="post" action="/copia">
            <div class="azioni">
                <button type="button" onclick="selezionaTutti(true)">Seleziona tutti</button>
                <button type="button" onclick="selezionaTutti(false)">Deseleziona tutti</button>
                <button class="primario" type="submit">Copia selezionati nel backup</button>
                <button type="button" onclick="location.reload()">Aggiorna report</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>Stato</th>
                        <th>File</th>
                        <th>Modifica origine</th>
                        <th>Modifica backup</th>
                        <th>Dim. origine</th>
                        <th>Dim. backup</th>
                        <th>Origine</th>
                        <th>Backup</th>
                    </tr>
                </thead>
                <tbody>
                    {corpo_tabella}
                </tbody>
            </table>
        </form>
    </div>
</body>
</html>"""


def crea_handler_server(cartella_da_osservare, cartella_backup, sottocartelle, percorso_log, percorso_csv):
    """
    Crea l'handler HTTP con accesso ai percorsi del programma.
    """
    class BackupReportHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # Evita il log HTTP standard in console; usiamo il log del programma.
            return

        def invia_html(self, contenuto, codice=200):
            dati = contenuto.encode("utf-8")

            try:
                self.send_response(codice)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(dati)))
                self.end_headers()
                self.wfile.write(dati)
            except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                # Il browser può chiudere la connessione prima di ricevere tutta la pagina
                # per ricarica, anteprima, antivirus o favicon. Non è un errore grave.
                return

        def do_GET(self):
            if self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return

            if self.path not in ("/", "/index.html"):
                try:
                    self.send_error(404, "Pagina non trovata")
                except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, OSError):
                    return
                return

            contenuto = genera_html_report(cartella_da_osservare, cartella_backup, sottocartelle)
            self.invia_html(contenuto)

        def do_POST(self):
            if self.path != "/copia":
                self.send_error(404, "Pagina non trovata")
                return

            lunghezza = int(self.headers.get("Content-Length", "0"))
            corpo = self.rfile.read(lunghezza).decode("utf-8")
            dati = parse_qs(corpo)
            selezionati = dati.get("file", [])

            if not selezionati:
                messaggio = "Nessun file selezionato."
            else:
                risultati_copia = copia_file_selezionati(
                    selezionati,
                    cartella_da_osservare,
                    cartella_backup,
                    sottocartelle,
                    percorso_log,
                    percorso_csv,
                )
                ok = sum(1 for _, risultato in risultati_copia if risultato == "OK")
                errori = len(risultati_copia) - ok
                messaggio = f"Copia completata: OK={ok}, errori={errori}. Il report è stato aggiornato."

            contenuto = genera_html_report(cartella_da_osservare, cartella_backup, sottocartelle, messaggio)
            self.invia_html(contenuto)

    return BackupReportHandler


def avvia_server_web(cartella_da_osservare, cartella_backup, sottocartelle, percorso_log, percorso_csv):
    """
    Avvia il server web locale in un thread separato.
    """
    handler = crea_handler_server(cartella_da_osservare, cartella_backup, sottocartelle, percorso_log, percorso_csv)
    server = ThreadingHTTPServer((HOST_SERVER_WEB, PORTA_SERVER_WEB), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    scrivi_log(f"Pagina report backup attiva | url=http://{HOST_SERVER_WEB}:{PORTA_SERVER_WEB}", percorso_log)
    return server


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
    Prepara i percorsi, avvia il log, avvia la pagina web locale e poi il monitoraggio.
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
        avvia_server_web(cartella_da_osservare, cartella_backup, sottocartelle, percorso_log, percorso_csv)

        print(f"--- monitor.py attivo su {cartella_da_osservare} ---")
        print(f"Apri il report backup: http://{HOST_SERVER_WEB}:{PORTA_SERVER_WEB}")
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

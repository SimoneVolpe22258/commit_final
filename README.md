# Sistema di Backup e Monitoraggio

## Descrizione del progetto

Sistema sviluppato per monitorare cartelle aziendali, registrare gli eventi sui file e mantenere un backup aggiornato della documentazione.

La versione attuale integra:

- monitoraggio in tempo reale tramite watchfiles;
- backup automatico dei file modificati;
- controllo iniziale della coerenza del backup;
- report CSV degli eventi;
- pagina web locale per la verifica delle anomalie;
- copia manuale dei file dal report web;
- logo configurabile tramite file di configurazione;
- sistema di cache per migliorare le prestazioni della pagina web.

## Componenti del sistema

- monitor.py
- conf.conf
- monitor.log
- file.csv
- report web locale
- sistema di backup automatico
- controllo di coerenza del backup
- cache del report HTML
- logo personalizzabile

## Struttura del progetto

commit_final/
├── data/
├── log/
├── src/
│   ├── monitor.py
│   ├── conf.conf
│   └── logo.png
├── CHANGELOG.txt
└── README.md

## Configurazione

Esempio:

path_cartella_da_osservare="C:\Tecnico"
path_cartella_backup="D:\BackupAutomatico\Tecnico"
sottocartelle_da_monitorare="*"
path_file_csv="../data/file.csv"
path_logo_web="logo.png"

### path_logo_web

Permette di specificare il logo visualizzato nella pagina web.

Se il percorso è relativo, il file viene cercato nella cartella src.

## Controllo iniziale del backup

All'avvio il programma:

1. esegue la scansione della cartella monitorata;
2. verifica la presenza dei file nel backup;
3. individua backup mancanti;
4. individua backup non aggiornati;
5. registra le anomalie;
6. popola la cache utilizzata dal report web.

## Report Web

URL:

http://127.0.0.1:5000

Funzionalità:

- visualizzazione file mancanti;
- visualizzazione backup non aggiornati;
- selezione multipla dei file;
- copia manuale nel backup;
- aggiornamento pagina immediato;
- ricalcolo manuale del report;
- visualizzazione logo aziendale;
- visualizzazione versione software;
- utilizzo cache per migliorare le prestazioni.

## Backup automatico

I file creati o modificati vengono copiati automaticamente nella cartella di backup mantenendo la struttura originale delle directory.

In caso di eliminazione del file originale, la copia presente nel backup NON viene eliminata per consentire la storicizzazione.

## Librerie utilizzate

- watchfiles
- pathlib
- shutil
- threading
- http.server
- csv
- html
- mimetypes

## Stato attuale

Versione software: 7.0
Ultimo aggiornamento: 07/06/2026

Funzionalità operative:

- monitoraggio file;
- backup automatico;
- report CSV;
- controllo iniziale backup;
- report web locale;
- cache del report;
- logo configurabile;
- storicizzazione dei file eliminati.

# Sistema di Backup e Monitoraggio

## Descrizione del progetto

Questo progetto è stato sviluppato per il corso di Informatica della classe 3SI serale.

L'obiettivo è realizzare un sistema in grado di monitorare alcune cartelle aziendali, registrare le modifiche effettuate sui file e creare copie di backup automatiche.

Il progetto prende come riferimento uno scenario aziendale nel quale è necessario proteggere documenti importanti e mantenere traccia delle operazioni svolte.

---

## Componenti del sistema

Il sistema è composto da:

- programma Python per il monitoraggio dei file;
- file di configurazione `conf.conf` per la gestione dei percorsi;
- file di log per la registrazione degli eventi;
- sistema di backup automatico dei file modificati;
- filtro sulle sottocartelle da monitorare;
- report CSV con informazioni sui file monitorati, ancora da implementare;
- macchina virtuale utilizzata come server di backup, ancora da implementare.

---

## Struttura del progetto

```text
commit_final/
│
├── data/
├── documentazione/
├── log/
│   └── monitor.log
├── src/
│   ├── monitor.py
│   └── conf.conf
├── CHANGELOG.txt
└── README.md
```

---

## Cartelle monitorate

Il programma controlla la cartella principale indicata nel file `conf.conf`.

Percorso previsto:

```text
C:\Work\marconilab
```

Le sottocartelle da monitorare vengono lette dal parametro:

```text
sottocartelle_da_monitorare
```

Le cartelle principali previste sono:

- clienti
- preventivi
- amministrazione

Il programma ignora gli eventi che avvengono fuori dalle sottocartelle configurate.

---

## File di configurazione

Il file `conf.conf` contiene i percorsi utilizzati dal programma.

Esempio di configurazione:

```text
path_cartella_da_osservare="C:\Work\marconilab"
path_cartella_backup="C:\Work\backup_marconilab"
sottocartelle_da_monitorare=clienti,preventivi,amministrazione
```

Il programma legge il file di configurazione all'avvio e recupera:

- percorso della cartella da osservare;
- percorso della cartella di backup;
- elenco delle sottocartelle da monitorare.

Le righe vuote, le righe commentate con `#` e le righe senza `=` vengono ignorate.

---

## Funzionamento

Il programma esegue le seguenti operazioni:

1. Legge i percorsi dal file `conf.conf`.
2. Crea la cartella `log`, se non esiste.
3. Registra l'avvio del programma nel file `monitor.log`.
4. Avvia il monitoraggio della cartella configurata.
5. Rileva gli eventi sui file:
   - creazione;
   - modifica;
   - eliminazione.
6. Controlla che il file appartenga a una delle sottocartelle configurate.
7. Registra ogni evento valido nel file di log.
8. Copia automaticamente nel backup i file esistenti e modificati.
9. Mantiene nel backup la stessa struttura delle cartelle originali.

Il programma può essere fermato manualmente dalla console con:

```text
Ctrl + C
```

---

## Backup automatico

Quando viene rilevato un file valido, il programma crea una copia nella cartella di backup.

Il backup mantiene il percorso relativo rispetto alla cartella monitorata.

Esempio:

```text
C:\Work\marconilab\clienti\cliente1\documento.txt
```

viene copiato in:

```text
C:\Work\backup_marconilab\clienti\cliente1\documento.txt
```

Se la cartella di destinazione non esiste, viene creata automaticamente.

---

## File di log

Gli eventi vengono registrati nel file:

```text
log\monitor.log
```

Ogni riga del log contiene:

- data e ora dell'evento;
- tipo di evento rilevato;
- percorso del file interessato;
- eventuale conferma di backup;
- eventuali errori durante il backup.

Esempio:

```text
[2026-05-29 10:15:32] - Evento: modified | File: C:\Work\marconilab\clienti\file.txt
[2026-05-29 10:15:32] Backup aggiornato: C:\Work\backup_marconilab\clienti\file.txt
```

---

## Ambiente Python

Il progetto viene eseguito all'interno di un ambiente virtuale Python dedicato.

Percorso previsto:

```text
C:\venv\commit_final
```

---

## Librerie utilizzate

Attualmente vengono utilizzate le librerie:

- `watchfiles`, per monitorare le modifiche ai file;
- `pathlib`, per gestire i percorsi in modo più sicuro;
- `shutil`, per copiare i file nella cartella di backup;
- `time`, per inserire data e ora nei messaggi di log.

---

## Avvio del programma

Per avviare il programma, posizionarsi nella cartella del progetto ed eseguire:

```bash
python src/monitor.py
```

All'avvio il programma mostra un messaggio simile a:

```text
--- monitor.py attivo su C:\Work\marconilab ---
Premi Ctrl + C per fermarlo se sei in console.
```

---

## Organizzazione del lavoro

Il progetto viene sviluppato da:

- Carloumberto Olivieri
- Simone Volpe

---

## Difficoltà incontrate

Durante lo sviluppo del progetto è stato necessario:

- comprendere il funzionamento della libreria `watchfiles`;
- definire correttamente la struttura delle cartelle;
- separare la cartella del progetto dalla cartella aziendale monitorata;
- gestire correttamente i percorsi dei file;
- configurare il sistema di backup automatico;
- leggere i percorsi da un file di configurazione esterno;
- limitare il monitoraggio solo alle sottocartelle richieste.

---

## Possibili miglioramenti

In futuro il sistema potrebbe essere esteso con:

- generazione automatica di report CSV;
- backup incrementale;
- controllo dell'integrità dei file;
- gestione avanzata degli errori;
- interfaccia più semplice per l'avvio e l'arresto;
- infrastruttura di backup su macchina virtuale;
- filtri sulle estensioni dei file.

---

## Stato attuale del progetto

Attualmente il progetto comprende:

- monitoraggio delle cartelle tramite la libreria `watchfiles`;
- registrazione degli eventi nel file di log;
- utilizzo della libreria `pathlib` per la gestione dei percorsi;
- lettura dei percorsi da file `conf.conf`;
- backup automatico dei file modificati;
- mantenimento della struttura originale nel backup;
- monitoraggio limitato alle sottocartelle configurate;
- arresto manuale da console tramite `Ctrl + C`.

Sono ancora da completare:

- generazione dei report CSV;
- organizzazione della macchina virtuale per il backup;
- eventuali funzioni aggiuntive richieste dal cliente.

---

## Versione attuale

Versione software: **3.2**

Ultimo aggiornamento: **29/05/2026** (solo Simone)

Funzionalità operative:

- monitoraggio dei file;
- registrazione eventi;
- gestione configurazione tramite file esterno;
- backup automatico dei file modificati;
- monitoraggio solo delle sottocartelle specificate (tramite file esterno);
- mantenimento della struttura delle cartelle nel backup;
- gestione degli errori durante il backup;
- arresto manuale del programma da console.

Funzionalità in sviluppo:

- report CSV;
- infrastruttura di backup su macchina virtuale;
- filtri avanzati sui file;
- backup incrementale.

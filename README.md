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
- file di log per la registrazione delle informazioni di esecuzione;
- sistema di backup automatico dei file modificati;
- filtro sulle sottocartelle da monitorare;
- report CSV contenente gli eventi rilevati sui file monitorati;
- macchina virtuale utilizzata come server di backup, ancora da implementare.

---

## Struttura del progetto

```text
commit_final/
│
├── data/
│   └── file.csv
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
path_cartella_backup="C:\Work2\backup"
sottocartelle_da_monitorare="clienti,preventivi,amministrazione"
path_file_csv="../data/file.csv"
```

Il programma legge il file di configurazione all'avvio e recupera:

- percorso della cartella da osservare;
- percorso della cartella di backup;
- elenco delle sottocartelle da monitorare;
- percorso del file CSV utilizzato per il report degli eventi.

Le righe vuote, le righe commentate con `#` e le righe senza `=` vengono ignorate.

---

## Funzionamento

Il programma esegue le seguenti operazioni:

1. Legge i percorsi dal file `conf.conf`.
2. Crea le cartelle `log` e `data`, se non esistono.
3. Registra l'avvio del programma nel file `monitor.log`.
4. Avvia il monitoraggio della cartella configurata.
5. Rileva gli eventi sui file:
   - creazione;
   - modifica;
   - eliminazione.
6. Controlla che il file appartenga a una delle sottocartelle configurate.
7. Registra l'evento nel file CSV.
8. Copia automaticamente nel backup i file creati o modificati.
9. Mantiene nel backup la stessa struttura delle cartelle originali.
10. In caso di eliminazione del file, registra l'evento ma non elimina la copia presente nel backup.

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
C:\Work2\backup\clienti\cliente1\documento.txt
```

Se la cartella di destinazione non esiste, viene creata automaticamente.

In caso di eliminazione di un file monitorato, la copia già presente nel backup non viene eliminata.

---

## Report CSV

Gli eventi rilevati sui file vengono registrati nel file CSV configurato nel file `conf.conf`.

Percorso predefinito:

```text
data\file.csv
```

Il file CSV contiene:

- data e ora dell'evento;
- tipo di evento;
- percorso del file;
- dimensione del file;
- data ultima modifica;
- esito del backup.

Esempio:

```text
data_ora;evento;file;dimensione;ultima_modifica;backup
2026-06-04 10:15:20;creazione;clienti\test.txt;120;2026-06-04 10:15:18;OK
2026-06-04 10:20:35;eliminazione;clienti\test.txt;N/D;N/D;NON CANCELLATO
```

Gli eventi vengono scritti in italiano. La libreria `watchfiles` rileva internamente gli eventi, ma il programma li converte nei termini:

- creazione;
- modifica;
- eliminazione.

---

## File di log

Il file:

```text
log\monitor.log
```

contiene esclusivamente informazioni di esecuzione del programma.

Vengono registrati:

- avvio del programma;
- arresto del programma;
- esito delle operazioni di backup;
- eventuali errori durante il backup;
- eliminazione di file monitorati.

Esempio:

```text
[2026-06-04 10:15:00] Programma avviato
[2026-06-04 10:15:20] Backup aggiornato: C:\Work2\backup\clienti\test.txt
[2026-06-04 10:20:35] Eliminato file nella cartella monitorata
[2026-06-04 10:30:00] Programma terminato dall'utente
```

Gli eventi di creazione e modifica dei file non vengono più scritti nel log, ma vengono registrati nel report CSV.

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
- `time`, per inserire data e ora nei messaggi di log e nel CSV.

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
- limitare il monitoraggio solo alle sottocartelle richieste;
- separare le informazioni operative del log dai dati degli eventi salvati nel CSV.

---

## Possibili miglioramenti

In futuro il sistema potrebbe essere esteso con:

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
- registrazione degli eventi in file CSV;
- registrazione delle informazioni operative nel file di log;
- utilizzo della libreria `pathlib` per la gestione dei percorsi;
- lettura dei percorsi da file `conf.conf`;
- backup automatico dei file creati e modificati;
- mantenimento della struttura originale nel backup;
- monitoraggio limitato alle sottocartelle configurate;
- gestione delle eliminazioni senza cancellazione delle copie di backup;
- arresto controllato da console tramite `Ctrl + C`.

Sono ancora da completare:

- organizzazione della macchina virtuale per il backup;
- eventuali funzioni aggiuntive richieste dal cliente;
- eventuale backup incrementale;
- filtri avanzati sulle estensioni dei file.

---

## Versione attuale

Versione software: **4.0**

Ultimo aggiornamento: **04/06/2026**

Funzionalità operative:

- monitoraggio dei file;
- registrazione eventi nel file CSV;
- log riservato alle informazioni di esecuzione;
- gestione configurazione tramite file esterno;
- backup automatico dei file creati e modificati;
- monitoraggio solo delle sottocartelle specificate;
- mantenimento della struttura delle cartelle nel backup;
- gestione degli errori durante il backup;
- eliminazione registrata senza cancellazione del backup;
- arresto manuale del programma da console.

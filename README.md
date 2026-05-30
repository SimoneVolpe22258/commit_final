# Sistema di Backup e Monitoraggio

## Descrizione del progetto

Questo progetto è stato sviluppato per il corso di Informatica della classe 3SI serale.

L'obiettivo è realizzare un sistema in grado di monitorare alcune cartelle aziendali, registrare le modifiche effettuate sui file e creare copie di backup automatiche.

Il progetto prende come riferimento uno scenario aziendale nel quale è necessario proteggere documenti importanti e mantenere traccia delle operazioni svolte.

---

## Componenti del sistema

Il sistema è composto da:

- Programma Python per il monitoraggio dei file;
- File di log per la registrazione degli eventi;
- Sistema di backup automatico;
- Report CSV con informazioni sui file monitorati; (ancora da implementare)
- Macchina virtuale utilizzata come server di backup. (ancora da implementare)

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
│   └── monitor.py
├── conf.conf
├── CHANGELOG.txt
└── README.md
```

---

## Cartelle monitorate

Il programma controlla la cartella:

```text
C:\Work\marconilab
```

Le cartelle principali monitorate sono:

- clienti
- preventivi
- amministrazione

---

## Funzionamento

Il programma esegue le seguenti operazioni:

1. Avvio del monitoraggio delle cartelle.
2. Rilevazione di:
   - creazione file;
   - modifica file;
   - eliminazione file.
3. Registrazione degli eventi nel file di log.
4. Creazione automatica delle copie di backup.
5. Generazione dei report CSV. (funzionalità prevista)

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

- watchfiles
- pathlib
- shutil

---

## Organizzazione del lavoro

Il progetto viene sviluppato da:

- Carloumberto Olivieri
- Simone Volpe

---

## Difficoltà incontrate

Durante le prime fasi del progetto è stato necessario:

- comprendere il funzionamento della libreria watchfiles;
- definire correttamente la struttura delle cartelle;
- separare la cartella del progetto dalla cartella aziendale monitorata;
- gestire correttamente i percorsi dei file;
- configurare il sistema di backup automatico.

---

## Possibili miglioramenti

In futuro il sistema potrebbe essere esteso con:

- filtri sulle estensioni dei file;
- backup incrementale;
- controllo dell'integrità dei file;
- gestione avanzata degli errori;
- generazione automatica di report CSV.

---

## Stato attuale del progetto

Attualmente il progetto comprende:

- monitoraggio delle cartelle tramite la libreria watchfiles;
- registrazione degli eventi nel file di log;
- utilizzo della libreria pathlib per la gestione dei percorsi;
- lettura dei percorsi da file conf.conf;
- backup automatico dei file modificati.

Sono ancora da completare:

- generazione dei report CSV;
- organizzazione della macchina virtuale per il backup;
- eventuali funzioni aggiuntive richieste dal cliente.

---

## Versione attuale

Versione software: **3.0**

Ultimo aggiornamento: **29/05/2026**

Funzionalità operative:

- monitoraggio dei file;
- registrazione eventi;
- gestione configurazione tramite file esterno;
- backup automatico dei file modificati.

Funzionalità in sviluppo:

- report CSV;
- infrastruttura di backup su macchina virtuale.
- gestione arresto monitoraggio
- monitoraggio solo su cartelle specifiche


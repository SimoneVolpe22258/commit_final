[README.md](https://github.com/user-attachments/files/28333896/README.md)
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
- Sistema di backup automatico; (ancora da implementare)
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
├── CHANGELOG.txt
└── README.md
```

---

## Cartelle monitorate

Il programma controlla la cartella:

```text
C:\Work\marconilab
```

All'interno di questa cartella sono presenti le directory aziendali:

```text
marconilab/
├── clienti/
├── preventivi/
├── amministrazione/
├── immagini/
├── logs/
├── backup/
└── config/
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
4. Creazione delle copie di backup.
5. Generazione dei report CSV.

---

## Ambiente Python

Il progetto viene eseguito all'interno di un ambiente virtuale Python dedicato.

Percorso previsto:

```text
C:\venv\commit_final
```

L'ambiente virtuale consente di installare le librerie necessarie senza modificare la configurazione generale del sistema operativo.

---

## Librerie utilizzate

Attualmente viene utilizzata la libreria:

- watchfiles

La libreria permette di rilevare automaticamente le modifiche effettuate nelle cartelle monitorate.

---

## Organizzazione del lavoro

Il progetto viene sviluppato da:

- Carloumberto Olivieri
- Simone Volpe


Entrambi partecipano all'analisi, alla progettazione e allo sviluppo del software.

Carloumberto cura inoltre:

- il Giornale di Bordo;
- l'aggiornamento del file CHANGELOG.

---

## Difficoltà incontrate

Durante le prime fasi del progetto è stato necessario:

- comprendere il funzionamento della libreria watchfiles;
- definire correttamente la struttura delle cartelle;
- separare la cartella del progetto dalla cartella aziendale monitorata;
- organizzare il lavoro in modo progressivo.

---

## Possibili miglioramenti

In futuro il sistema potrebbe essere esteso con:

- filtri sulle estensioni dei file;
- backup incrementale;
- controllo dell'integrità dei file;
- configurazione tramite file esterno;
- gestione avanzata degli errori.

---

## Stato attuale del progetto

Attualmente è stata realizzata la struttura iniziale dell'applicazione Python con:

- funzione di scrittura del log;
- funzione principale di avvio;
- predisposizione del monitoraggio delle cartelle tramite watchfiles.
- utilizzo libreria pathlib

Le funzionalità verranno completate nelle successive fasi di sviluppo.

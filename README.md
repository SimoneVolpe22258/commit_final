# Sistema di Backup e Monitoraggio

> Sistema professionale di monitoraggio, backup, controllo di coerenza e recupero documentale con interfaccia web locale.

**Versione attuale:** Rev. 8.3  
**Ultimo aggiornamento:** 07/06/2026

---

# 1. Introduzione

Il progetto nasce per rispondere a una necessità comune negli ambienti aziendali: monitorare costantemente una cartella di lavoro, mantenere una copia di sicurezza aggiornata dei documenti e consentire il recupero controllato dei file eliminati.

A differenza dei sistemi di sincronizzazione tradizionali, questo software adotta una filosofia di **storicizzazione documentale**, nella quale il backup viene considerato un archivio di sicurezza e non una semplice replica bidirezionale.

---

# 2. Obiettivi del progetto

- Monitorare automaticamente le modifiche ai file.
- Eseguire backup automatici in tempo reale.
- Conservare i documenti eliminati dall'origine.
- Mantenere traccia delle operazioni effettuate.
- Consentire il controllo della coerenza del backup.
- Permettere il recupero selettivo dei documenti.
- Fornire una dashboard web semplice e immediata.

---

# 3. Caratteristiche principali

| Funzionalità | Stato |
|------------|--------|
| Monitoraggio realtime | ✅ |
| Backup automatico | ✅ |
| Configurazione tramite file esterno | ✅ |
| Report CSV eventi | ✅ |
| Log operativo | ✅ |
| Controllo iniziale backup | ✅ |
| Dashboard Web | ✅ |
| Cache prestazionale report | ✅ |
| Copia manuale nel backup | ✅ |
| Controllo inverso backup → origine | ✅ |
| Ripristino selettivo | ✅ |
| Apertura percorsi da web | ✅ |
| Logo personalizzabile | ✅ |
| Compatibilità Windows | ✅ |
| Compatibilità Linux | ✅ |
| Compatibilità macOS | ✅ |

---

# 4. Architettura del sistema

```text
Cartella Monitorata
        │
        ▼
     monitor.py
        │
 ┌──────┼──────────┐
 ▼      ▼          ▼
Backup  CSV       Log
        │
        ▼
 Dashboard Web
```

---

# 5. Filosofia di funzionamento

Il sistema è stato progettato seguendo il principio:

```text
Origine ─────► Backup
```

e non:

```text
Origine ◄────► Backup
```

Questo significa che:

- il backup rappresenta la copia di sicurezza;
- i file eliminati nell'origine non vengono cancellati dal backup;
- il recupero dei documenti è sempre manuale;
- non vengono eseguite cancellazioni automatiche;
- non vengono sovrascritti file esistenti durante il ripristino.

Questa scelta consente di utilizzare il backup come archivio storico dei documenti.

---

# 6. Struttura del progetto

```text
commit_final/
│
├── data/
│   └── file.csv
│
├── log/
│   └── monitor.log
│
├── src/
│   ├── monitor.py
│   ├── conf.conf
│   └── logo.png
│
├── README.md
└── CHANGELOG.txt
```

---

# 7. Configurazione

Esempio di configurazione:

```text
path_cartella_da_osservare="C:\Tecnico"
path_cartella_backup="d:\BakupAutomaticoConPythonMonitor\Tecnico"
sottocartelle_da_monitorare="*"
path_file_csv="../data/file.csv"
path_logo_web="logo.png"
```

## Parametri

### path_cartella_da_osservare

Cartella principale da monitorare.

### path_cartella_backup

Percorso della cartella di backup.

### sottocartelle_da_monitorare

Elenco delle sottocartelle monitorate oppure `*` per monitorare tutto.

### path_file_csv

Percorso del report CSV degli eventi.

### path_logo_web

Logo visualizzato nella dashboard web.

---

# 8. Funzionamento operativo

All'avvio il programma:

1. legge la configurazione;
2. verifica i percorsi;
3. esegue il controllo iniziale del backup;
4. aggiorna la cache del report;
5. avvia il server web locale;
6. attiva il monitoraggio realtime.

---

# 9. Dashboard Web

La dashboard è disponibile all'indirizzo:

```text
http://127.0.0.1:5000
```

Funzionalità disponibili:

- visualizzazione file mancanti nel backup;
- visualizzazione backup non aggiornati;
- selezione dei file da aggiornare;
- aggiornamento manuale del backup;
- ricalcolo report;
- visualizzazione logo aziendale;
- apertura percorsi origine e backup.

---

# 10. Controllo inverso e ripristino

Dalla Rev. 8.0 il sistema introduce il controllo inverso:

```text
Backup ─────► Origine
```

Utilizzato esclusivamente per recuperare documenti mancanti.

Caratteristiche:

- selezione manuale dei file;
- conferma obbligatoria;
- registrazione log;
- registrazione CSV;
- nessuna cancellazione;
- nessuna sovrascrittura.

---

# 11. Report CSV

Il file CSV registra:

- data e ora;
- tipo evento;
- file coinvolto;
- percorso completo;
- dimensione;
- ultima modifica;
- esito dell'operazione.

Eventi principali:

- added
- modified
- deleted
- controllo_iniziale
- copia_da_pagina_web
- ripristino_da_backup

---

# 12. File di Log

Il log registra:

- avvio e arresto programma;
- backup automatici;
- errori;
- aggiornamenti cache;
- controlli iniziali;
- operazioni da dashboard;
- ripristini documentali;
- apertura percorsi.

---

# 13. Compatibilità

## Windows

Apertura percorsi tramite Esplora File.

## Linux

Apertura percorsi tramite xdg-open.

## macOS

Apertura percorsi tramite open.

---

# 14. Sicurezza

Il sistema implementa diverse misure di protezione:

- validazione dei percorsi;
- protezione contro percorsi esterni;
- nessuna cancellazione automatica;
- nessuna sovrascrittura automatica;
- conferma esplicita per i ripristini;
- gestione delle eccezioni.

---

# 15. Cronologia del progetto

Le modifiche dettagliate sono documentate nel file:

```text
CHANGELOG.txt
```

---

# 16. Roadmap futura

Possibili sviluppi:

- ricerca avanzata nel report;
- esportazione Excel;
- esportazione PDF;
- autenticazione utenti;
- gestione ruoli;
- database SQLite;
- versioning documentale;
- notifiche email.

---

# Autore

## Versioni 1.0 - 6.x

- Carloumberto Olivieri
- Simone Volpe

## Versioni 7.0 e successive

- Simone Volpe

---

# Licenza

Progetto sviluppato a scopo didattico e formativo nell'ambito del corso di Informatica.

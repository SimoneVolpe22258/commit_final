
# Sistema di Backup e Monitoraggio

## Descrizione

Sistema sviluppato da Carloumberto Olivieri e Simone Volpe per il monitoraggio di cartelle aziendali, la registrazione degli eventi sui file, il backup automatico e la conservazione storica dei documenti.

Il progetto è evoluto da semplice monitor di filesystem fino a piattaforma di controllo backup con interfaccia web locale, controllo di coerenza, ripristino selettivo e compatibilità multipiattaforma.

Versione attuale: REV. 8.3

---

## Evoluzione del progetto

### Rev. 1.x
- Struttura iniziale del progetto
- Introduzione di watchfiles
- Logging di base
- Separazione delle funzioni

### Rev. 2.0
- Introduzione del file conf.conf
- Configurazione esterna dei percorsi

### Rev. 3.x
- Backup automatico
- Utilizzo di pathlib
- Gestione delle sottocartelle monitorate

### Rev. 4.0
- Introduzione CSV eventi
- Separazione log operativo / eventi file
- Gestione eliminazioni
- Conservazione file eliminati nel backup

### Rev. 5.0
- Controllo iniziale backup
- Report web locale
- Verifica file mancanti e non aggiornati
- Copia manuale da pagina web

### Rev. 6.0
- Cache del report
- Ottimizzazione prestazioni
- Aggiornamento periodico
- Pulsante ricalcolo manuale

### Rev. 7.0
- Logo configurabile
- Visualizzazione versione software
- Migliorie interfaccia web

### Rev. 8.0
- Controllo inverso backup -> origine
- Ripristino selettivo
- Conferma operazione
- Logging e CSV del ripristino

### Rev. 8.1
- Apertura percorsi origine e backup

### Rev. 8.2
- Apertura percorsi anche nella pagina di ripristino

### Rev. 8.3
- Compatibilità Windows
- Compatibilità Linux
- Compatibilità macOS
- Apertura cartelle multipiattaforma

---

## Funzionalità attuali

- Monitoraggio realtime
- Backup automatico
- Backup mantenuto per storicizzazione
- CSV eventi
- Log operativo
- Controllo iniziale backup
- Report web
- Cache prestazionale
- Logo personalizzabile
- Ripristino selettivo
- Apertura percorsi
- Compatibilità multipiattaforma

---

## Filosofia del sistema

Origine -> Backup

Il backup è la copia di sicurezza.

In caso di eliminazione di un file nell'origine:
- il file NON viene cancellato dal backup;
- l'evento viene registrato;
- il file può essere recuperato tramite controllo inverso.

Questo comportamento è intenzionale e costituisce il sistema di storicizzazione documentale.

---

## Compatibilità

- Windows
- Linux
- macOS

---

## Autori

- Carloumberto Olivieri
- Simone Volpe

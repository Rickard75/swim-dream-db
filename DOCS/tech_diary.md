# Tech Diary of  Jr. Data Scientist
Questo file riassume i **TIL** (*Today I learnt*) durante il mio percorso di formazione come data scientist: database, terminali, sistemi operativi, programmi, linguaggi, tips utili e altro incontrato durante il viaggio. 

Le mie regole:
- inserisci la data
- inserisci il tag (tag disponibili: `HW`,`GIT`, `SHELL`, `PYTHON`, `SQL`)
- alla fine del giorno riassumi in una frase il TIL registrandone la data nella sezione `DIARIO`

Enjoy! :D

Data: `06-apr-2026`
Autore: `Riccardo`

## DIARIO
- `2026-04-06`: come scopiazzare roba da github; una volta c'erano le macchine da scrivere; comandi strani da shell-vellarsi; vedere i commit al volo 


## `2026-04-06`

### [GIT] commands: Clone vs Fork vs Pull
- **clone** = scarico il repo in locale per lavorarci
- **fork** = copio il repo di qualcun altro su GitHub
- **pull** = aggiorno un repo già clonato

### [HW] Legacy delle macchine da scrivere: `core.autocrlf`
- **Windows** usa `CRLF` (*Carriage Return + Line Feed*), **Linux**/**Mac** usano `LF` (*Line Feed*)
- `git config --global core.autocrlf true` → così **Git** converte automaticamente
- i file su GitHub restano sempre `LF`

### [SHELL] Log comandi su file `2>&1`
- `2` = canale stderr (errori)
- `1` = canale stdout (output normale)
- `2>&1` = manda gli errori nello stesso flusso dell'output normale
- esempio `echo $PSVersionTable 2>&1 | tee -a log.txt` esegue il comando e salva l'output nel file come *appended*

### [SHELL] Definizioni & Storia
- **kernel** - ponte tra SW e HW 
- **shell** - interprete dei comandi sul terminale
- **terminale** - interfaccia di dialogo dove si usa linguaggio comprensibile al kernel interpretato dalla shell
- **Mac/Win/Lin** - Steve e Linus usano sistemi Unix-like (e.g. `ubuntu/zsh`, dove c'è già GIT incorporato), mentre Bill no (e.g. la versione più moderna per Windows è `Powershell`, senza GIT integrato)

### [GIT] Visualizzare storia commit
- `git log --oneline --graph`

### [HW] Porte di un PC
```
Il tuo computer (localhost)
├── Porta 5432  →  PostgreSQL in ascolto qui
├── Porta 80    →  Server web HTTP
├── Porta 443   →  Server web HTTPS
├── Porta 22    →  SSH (connessione remota)
└── Porta 8080  →  Spesso usata per app in sviluppo
```

### [SQL] Creare un db
- usando il terminale: `psql -U postgres -c "CREATE DATABASE swimming_db ENCODING 'UTF8';"`
- da GUI: `Database`>`Create`
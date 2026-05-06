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
- `2026-04-22`: leggere stato e staging in Git; togliere file dallo stage; ripristinare modifiche; rinominare branch locale e remoto


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

## `2026-04-09`
### [GIT] Using versioning with a team
- `git log --oneline --graph`
- per una modifica creo il mio branch: `git branch bugfix/duplicated_entries`
- carico il branch sull'internet: `git push --set-upstream origin bugfix/duplicated_entries`
- mi sposto nel branch `git checkout bugfix/duplicated_entries`
- edito qui il codice
- `git diff` mi mostra la differenza con quanto c'è nell'ultimo commit
- faccio un `git add .`, poi il `git commit -m "bugfix: deleted duplicated entry of dyn_thr_m"` e quindi il `git push` nel branch di feature **locale**
- `git switch development` unisco le storie dei branch
- `git merge bugfix/duplicated_entries` unisco le storie dei branch e poi `git push` fa il push nell'origin

## `2026-04-22`
### [GIT] Stato repo e staging
- `git status` mostra branch corrente, stato sincronizzazione con origin e file staged/unstaged
- `git diff --staged` mostra cosa finirà nel prossimo commit
- `git restore --staged DOCS/db_architecture.md` toglie il file dallo stage ma mantiene le modifiche nel working tree
- `git restore DOCS/db_architecture.md` annulla le modifiche locali al file

### [GIT] Branching: rinominare un branch
- `git branch -m feature/tables` rinomina il branch corrente (comando usato in pratica)
- `git branch -m vecchio_nome nuovo_nome` rinomina un branch specifico non necessariamente checkoutato
- `git push origin -u nuovo_nome` pubblica il nuovo branch e imposta l'upstream
- `git push origin --delete vecchio_nome` elimina il vecchio nome branch dal remote
- `git fetch -p` pulisce i riferimenti remoti non piu esistenti

### [GIT] Mettere da parte il lavoro temporaneamente
- `git stash` salva modifiche non committate per poter cambiare branch in sicurezza con `git switch <nome_branch>`



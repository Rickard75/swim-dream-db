# Guida al Terminale per Data Scientist
> Riferimento pratico — dal kernel ai comandi quotidiani
> Autore: swim-dream-db project | Aggiornato: Aprile 2026

---

## 1. Il Kernel — cos'è il cuore del sistema

Il **kernel** è il livello più basso del sistema operativo. Fa da intermediario tra i programmi e l'hardware (CPU, RAM, disco, rete). Non lo tocchi mai direttamente — ci parli attraverso la shell.

```
[ Programmi tuoi: Python, VSCode, PostgreSQL ]
            ↓
       [ Shell / Terminale ]
            ↓
          [ Kernel ]
            ↓
    [ Hardware: CPU, RAM, Disco ]
```

| Sistema | Kernel |
|---|---|
| Linux (Ubuntu) | Linux kernel — open source |
| macOS | XNU (Darwin) — derivato da Unix |
| Windows | Windows NT kernel — proprietario Microsoft |

**Perché ti interessa:** macOS e Linux hanno lo stesso antenato (Unix) — per questo i comandi del terminale sono quasi identici. Windows è completamente diverso.

---

## 2. Shell — cos'è e perché esistono tipi diversi

La **shell** è il programma che legge quello che scrivi nel terminale e lo esegue. È l'interprete tra te e il kernel.

| Shell | Sistema | Note |
|---|---|---|
| **bash** | Linux, macOS (vecchio default) | Bourne Again Shell — la più diffusa |
| **zsh** | macOS (default da Catalina 2019) | Bash migliorata — stessa sintassi + features |
| **PowerShell** | Windows (default moderno) | Completamente diversa da bash — oggetti invece di testo |
| **cmd.exe** | Windows (legacy) | Vecchissima, da evitare |
| **fish** | Linux/Mac opzionale | User friendly ma meno usata in produzione |

**Regola pratica:** bash e zsh sono intercambiabili per il 95% dei comandi quotidiani. PowerShell ha sintassi diversa — `Get-Command` invece di `which`, `$env:PATH` invece di `$PATH`.

### Come sai quale shell stai usando?
```bash
echo $SHELL        # Linux/Mac
$PSVersionTable    # PowerShell
```

---

## 3. Terminale vs Shell vs Console — differenze

Termini spesso confusi, significati diversi:

| Termine | Cos'è | Esempio |
|---|---|---|
| **Terminale** | Il programma con la finestra nera | Terminal.app, Windows Terminal, iTerm2 |
| **Shell** | L'interprete dentro il terminale | bash, zsh, PowerShell |
| **Console** | Terminale fisico/di sistema (termine storico) | Oggi usato come sinonimo di terminale |
| **CLI** | Command Line Interface — qualsiasi interfaccia a testo | Tutti i comandi che scrivi |
| **REPL** | Read-Eval-Print Loop — shell interattiva | psql, python, node |

**Analogia:** il terminale è la finestra del ristorante, la shell è il cameriere che prende l'ordine, il kernel è la cucina.

---

## 4. Differenze pratiche Linux / macOS / Windows

### Filesystem e path
| Concetto | Linux/Mac | Windows |
|---|---|---|
| Separatore cartelle | `/` | `\` |
| Root del sistema | `/` | `C:\` |
| Home utente | `/home/chiara` o `~/` | `C:\Users\Chiara` |
| File nascosti | iniziano con `.` (es. `.gitignore`) | attributo nascosto |
| Case sensitive | **Sì** — `File.txt` ≠ `file.txt` | No — `File.txt` = `file.txt` |

### Gestori di pacchetti
| Sistema | Gestore | Comando tipo |
|---|---|---|
| Ubuntu/Debian | `apt` | `sudo apt install postgresql` |
| macOS | `homebrew` | `brew install postgresql` |
| Windows | `winget` | `winget install postgresql` |
| Python (tutti) | `pip` | `pip install pandas` |
| Node.js (tutti) | `npm` | `npm install express` |

### Permessi
Su Linux/Mac ogni file ha proprietario e permessi (`rwx`). Su Windows il sistema è diverso (ACL). Per questo su Linux/Mac certi comandi vogliono `sudo` davanti — esegui come superutente.

```bash
sudo apt install postgresql   # sudo = "run as administrator"
```

Su Windows l'equivalente è aprire PowerShell "come amministratore".

---

## 5. PATH — la variabile più importante

Il **PATH** è una variabile d'ambiente che contiene una lista di cartelle. Quando scrivi un comando, il sistema cerca l'eseguibile in quelle cartelle nell'ordine in cui sono elencate.

### Come funziona
```bash
# Scrivi:
brew --version

# Il sistema cerca brew in:
/usr/local/bin        ← lo trova qui ✅
/usr/bin
/bin
/usr/sbin
# se non lo trova da nessuna parte → "command not found"
```

### Come vedi il PATH attuale
```bash
echo $PATH            # Linux/Mac — lista separata da :
$env:PATH             # PowerShell — lista separata da ;
```

### Come aggiungi qualcosa al PATH (Linux/Mac)
```bash
# Temporaneo — vale solo per questa sessione
export PATH="/nuova/cartella:$PATH"

# Permanente — scrivi nel file di configurazione della shell
echo 'export PATH="/nuova/cartella:$PATH"' >> ~/.zshrc   # zsh
echo 'export PATH="/nuova/cartella:$PATH"' >> ~/.bashrc  # bash
```

### Perché i conflitti di PATH sono comuni
Se hai Python 3.11 e Python 3.12 installati, il comando `python` usa quello che trova **prima** nel PATH. Questo causa bug sottili e difficili da trovare.

```bash
which python          # ti dice quale python sta usando
which python3
python --version      # verifica la versione attiva
```

---

## 6. Variabili d'ambiente

Le **variabili d'ambiente** sono coppie chiave=valore che i programmi leggono per configurarsi. Il PATH è la più famosa, ma ce ne sono tante.

### Sintassi
```bash
# Leggi una variabile
echo $HOME            # /Users/chiara
echo $USER            # chiara
echo $PATH

# Imposta una variabile (temporanea)
export NOME="valore"

# Imposta permanente → scrivi in ~/.zshrc o ~/.bashrc
```

### Il file .env
Nei progetti si usa un file `.env` per le variabili sensibili:
```
# .env — NON committare su Git
POSTGRES_PASSWORD=miapassword
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://localhost:5432/swimming_db
```

I programmi Python lo leggono con la libreria `python-dotenv`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("POSTGRES_PASSWORD")
```

**Regola d'oro:** `.env` va sempre in `.gitignore`. Mai su GitHub.

---

## 7. Pacchetti e dipendenze

Un **pacchetto** è un programma o libreria distribuita in formato installabile.

Una **dipendenza** è un pacchetto che ne richiede un altro per funzionare. Esempio: PostgreSQL dipende da OpenSSL. Quando installi PostgreSQL, il gestore di pacchetti installa OpenSSL automaticamente.

```
PostgreSQL
├── openssl          (dipendenza diretta)
├── krb5             (dipendenza diretta)
│   └── libcom_err   (dipendenza transitiva)
└── readline         (dipendenza diretta)
```

### Conflitti di dipendenze
Il problema più comune: due programmi richiedono versioni diverse della stessa libreria.

```
Programma A → richiede libX versione 1.2
Programma B → richiede libX versione 2.0
```

**Soluzione in Python:** gli **ambienti virtuali** (`venv`) isolano le dipendenze per progetto.

```bash
# Crea ambiente virtuale
python -m venv venv

# Attivalo (Mac/Linux)
source venv/bin/activate

# Attivalo (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Installa pacchetti (vanno solo in questo ambiente)
pip install pandas sqlalchemy

# Salva le dipendenze del progetto
pip freeze > requirements.txt

# Disattiva
deactivate
```

---

## 8. Comandi base — Linux/Mac e Windows a confronto

### Navigazione filesystem
| Operazione | Linux/Mac (bash/zsh) | Windows (PowerShell) |
|---|---|---|
| Dove sono? | `pwd` | `pwd` o `Get-Location` |
| Lista file | `ls` | `ls` o `dir` |
| Lista dettagliata | `ls -la` | `ls -Force` |
| Cambia cartella | `cd percorso` | `cd percorso` |
| Torna indietro | `cd ..` | `cd ..` |
| Vai alla home | `cd ~` | `cd ~` |

### Gestione file
| Operazione | Linux/Mac | Windows |
|---|---|---|
| Crea file vuoto | `touch file.txt` | `ni file.txt` |
| Crea cartella | `mkdir cartella` | `mkdir cartella` |
| Crea albero cartelle | `mkdir -p a/b/c` | `mkdir -Force a\b\c` |
| Copia file | `cp origine dest` | `cp origine dest` |
| Sposta/rinomina | `mv origine dest` | `mv origine dest` |
| Elimina file | `rm file.txt` | `rm file.txt` |
| Elimina cartella | `rm -rf cartella` | `rm -r cartella` |

### Lettura file
| Operazione | Linux/Mac | Windows |
|---|---|---|
| Mostra contenuto | `cat file.txt` | `cat file.txt` |
| Mostra prime righe | `head file.txt` | `gc file.txt -Head 10` |
| Mostra ultime righe | `tail file.txt` | `gc file.txt -Tail 10` |
| Cerca testo | `grep "testo" file` | `sls "testo" file` |

### Processi e sistema
| Operazione | Linux/Mac | Windows |
|---|---|---|
| Processi attivi | `ps aux` | `Get-Process` |
| Uccidi processo | `kill PID` | `Stop-Process -Id PID` |
| Uso disco | `df -h` | `Get-PSDrive` |
| Chi sono | `whoami` | `whoami` |

### Operatori universali (funzionano ovunque)
```bash
|    # pipe — passa output di A come input di B
     # es: ls | grep .py  →  lista solo file .py

>    # redirect — scrive output in un file (sovrascrive)
     # es: echo "ciao" > file.txt

>>   # redirect append — aggiunge in fondo al file
     # es: echo "riga" >> file.txt

&&   # esegui B solo se A è andato a buon fine
     # es: git add . && git commit -m "msg"
```

---

## 9. Dove installare le cose — regola generale

| Cosa | Dove va | Perché |
|---|---|---|
| Applicazioni con GUI | `/Applications` (Mac) — `C:\Program Files` (Win) | Standard di sistema |
| Tool da terminale | `/usr/local/bin` (Mac via brew) — nel PATH (Win) | Accessibili da shell |
| Librerie Python di progetto | `venv/` dentro il progetto | Isolamento dipendenze |
| Librerie Python globali | evita — usa sempre venv | Prevenire conflitti |
| File di progetto | `~/Desktop/progetto` o `~/progetti/` | Dove vuoi tu |
| Credenziali e password | `.env` nel progetto (nel .gitignore) | Sicurezza |
| Configurazioni shell | `~/.zshrc` (zsh) — `~/.bashrc` (bash) | Caricato ad ogni apertura |

---

## 10. File di configurazione della shell

Ogni volta che apri un terminale, la shell carica automaticamente dei file di configurazione. È lì che metti il PATH, gli alias, le variabili d'ambiente permanenti.

| Shell | File caricato al login | File caricato sempre |
|---|---|---|
| bash | `~/.bash_profile` o `~/.bashrc` | `~/.bashrc` |
| zsh | `~/.zprofile` | `~/.zshrc` |
| PowerShell | `$PROFILE` | `$PROFILE` |

### Alias — scorciatoie personalizzate
```bash
# Scrivi in ~/.zshrc o ~/.bashrc
alias ll='ls -la'
alias gs='git status'
alias gp='git push'
alias dc='docker-compose'

# Dopo aver modificato il file, ricaricalo senza riavviare:
source ~/.zshrc
```

---

## 11. Git — comandi quotidiani del DS

```bash
# Setup iniziale (una volta sola)
git config --global user.name "Tuo Nome"
git config --global user.email "tua@email.com"
git config --global core.editor nano

# Flusso di lavoro base
git status                          # cosa è cambiato?
git add .                           # prepara tutto per il commit
git add file.py                     # prepara solo un file
git commit -m "feat: aggiungi tabella esercizi"
git push                            # carica su GitHub
git pull                            # scarica aggiornamenti da GitHub

# Storico
git log                             # storia dei commit
git log --oneline                   # versione compatta

# Branch (rami paralleli)
git branch                          # lista branch
git checkout -b nome-branch         # crea e passa a nuovo branch
git checkout main                   # torna al branch principale
git merge nome-branch               # unisce branch nel corrente
```

### Convenzione messaggi commit
```
feat:     nuova funzionalità
fix:      correzione bug
docs:     documentazione
chore:    setup, configurazione, manutenzione
refactor: riscrittura codice senza cambiare funzionalità
test:     aggiunta test
style:    formattazione, niente di funzionale
```

---

## 12. Conflitti comuni e come risolverli

### "command not found"
```bash
# Causa: il comando non è nel PATH
# Soluzione 1: verifica se è installato
which brew
which python3

# Soluzione 2: aggiungi al PATH
export PATH="/percorso/del/programma:$PATH"
```

### "Permission denied"
```bash
# Causa: non hai i permessi
# Soluzione Mac/Linux: usa sudo
sudo comando

# Soluzione: cambia i permessi del file
chmod +x script.sh     # rendi eseguibile
```

### "Port already in use"
```bash
# Causa: un altro programma usa la stessa porta (es. PostgreSQL su 5432)
# Trova chi usa la porta
lsof -i :5432          # Mac/Linux
netstat -ano | findstr :5432   # Windows

# Uccidi il processo (usa il PID dall'output sopra)
kill -9 PID            # Mac/Linux
Stop-Process -Id PID   # Windows
```

### Versioni Python multiple
```bash
python --version       # quale versione è attiva?
python3 --version
which python
which python3

# Soluzione: usa sempre venv per ogni progetto
# così la versione è isolata e controllata
```

---

## 13. Tool utili per un Data Scientist

### Nel terminale
| Tool | Cosa fa | Installa con |
|---|---|---|
| `htop` | Monitor processi interattivo (top migliore) | `brew install htop` |
| `tree` | Mostra struttura cartelle ad albero | `brew install tree` |
| `jq` | Leggi e filtra JSON da terminale | `brew install jq` |
| `csvkit` | Lavora con CSV da terminale | `pip install csvkit` |
| `pgcli` | Client PostgreSQL con autocompletamento | `pip install pgcli` |

### Online
| Risorsa | Cosa trovi |
|---|---|
| `explainshell.com` | Incolla un comando, ti spiega ogni pezzo |
| `tldr.sh` | Man page semplificate con esempi pratici |
| `devhints.io` | Cheat sheet per git, bash, docker, ecc. |
| `stackoverflow.com` | Risposta a qualsiasi errore tu incontri |
| `docs.postgresql.org` | Documentazione ufficiale PostgreSQL |
| `github.com` | Codice open source, portfolio, collaborazione |

### VSCode — estensioni utili per DS
```
Python                    (Microsoft)
Pylance                   (Microsoft)
PostgreSQL                (Chris Kolkman)
GitLens                   (GitKraken)
Rainbow CSV               (mechatroner)
indent-rainbow            (oderwat)
.env                      (mikestead)
Jupyter                   (Microsoft)
```

---

## 14. Come imparare — percorso consigliato

### Livello 1 — Basi terminale (1-2 settimane)
- `pwd`, `ls`, `cd`, `mkdir`, `touch`, `cp`, `mv`, `rm`
- `cat`, `grep`, `|`, `>`, `>>`
- Risorsa: [linuxcommand.org](https://linuxcommand.org)

### Livello 2 — Git (1 settimana)
- `init`, `add`, `commit`, `push`, `pull`, `status`, `log`
- Risorsa: [learngitbranching.js.org](https://learngitbranching.js.org) — interattivo e visuale

### Livello 3 — Python ambiente (1 settimana)
- `venv`, `pip`, `requirements.txt`
- variabili d'ambiente, `.env`
- Risorsa: documentazione ufficiale Python

### Livello 4 — SQL e PostgreSQL (in corso con questo progetto!)
- DDL: `CREATE TABLE`, `ALTER TABLE`
- DML: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- `JOIN`, `GROUP BY`, `WHERE`, subquery
- Risorsa: [pgexercises.com](https://pgexercises.com)

### Livello 5 — Strumenti avanzati (ongoing)
- Docker
- Shell scripting (`.sh`)
- cron job (automazione)
- SSH (connessione remota)

---

## 15. Glossario rapido

| Termine | Definizione |
|---|---|
| **kernel** | Nucleo del SO — gestisce hardware e risorse |
| **shell** | Interprete dei comandi — bash, zsh, PowerShell |
| **terminale** | Programma con interfaccia grafica che contiene la shell |
| **PATH** | Lista di cartelle dove il sistema cerca gli eseguibili |
| **variabile d'ambiente** | Coppia chiave=valore letta dai programmi |
| **pacchetto** | Programma o libreria distribuita in formato installabile |
| **dipendenza** | Pacchetto richiesto da un altro pacchetto |
| **gestore di pacchetti** | Tool che installa/rimuove pacchetti (apt, brew, winget, pip) |
| **venv** | Ambiente virtuale Python — isola le dipendenze di un progetto |
| **sudo** | Esegui come superutente (admin) su Linux/Mac |
| **pipe** | `\|` — passa l'output di un comando come input al successivo |
| **redirect** | `>` — manda l'output in un file invece che a schermo |
| **alias** | Scorciatoia personalizzata per un comando lungo |
| **daemon** | Programma in background (es. PostgreSQL come servizio) |
| **porta** | Numero che identifica un servizio di rete (PostgreSQL = 5432) |
| **localhost** | Il tuo stesso computer — IP 127.0.0.1 |
| **dotfile** | File di configurazione nascosto che inizia con `.` |
| **shebang** | `#!/bin/bash` — prima riga di uno script, dice quale shell usare |
| **stdin/stdout/stderr** | Input standard / Output standard / Output errori |
| **PID** | Process ID — numero univoco di un processo in esecuzione |
| **Git** | Sistema di controllo versione distribuito |
| **repository** | Cartella tracciata da Git — locale o remota (GitHub) |
| **commit** | Snapshot salvato della storia del progetto |
| **branch** | Ramo parallelo di sviluppo |
| **merge** | Unione di due branch |
| **remote** | Repository remoto (GitHub, GitLab) |
| **push/pull** | Carica/scarica commit dal remote |
| **WSL** | Windows Subsystem for Linux — Linux dentro Windows |
| **Docker** | Contenitori — ambienti isolati e riproducibili |

---

*Documento generato durante il progetto swim-dream-db — Aprile 2026*
*GitHub: github.com/Rickard75/swim-dream-db*

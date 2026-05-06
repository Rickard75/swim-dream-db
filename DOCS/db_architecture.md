# Swim Dream Database Architecture
## ENTITÀ PRINCIPALI
### CLAUDIA

```
PostgreSQL
├── esercizio (difficoltà, livello, elemento tecnico, età, obiettivo didattico)
├── stile (crawl, dorso, rana, delfino, misti, sincro, pallanuoto)
├── allenamento (tipologia, distanza, data, fase stagionale)
├── sezione (riscaldamento, centrale, tipologia, defaticamento)
├── blocco_esercizio (ripetizioni, distanza, tempo, attrezzatura)
├── piscina (nome, città, corsie, vasca, servizi)
├── recensione (voto, testo, data)
├── istruttore (nome, qualifiche, brevetti, esperienza, età)
├── brevetto (nome, ente, livello, scadenza)
├── corso (nome, livello, piscina, istruttore)
├── record (categoria, gara, tempo, atleta, data, vasca)
└── progressione_didattica (livello, prerequisiti, esercizi, obiettivi)
```
Dopo analisi di un allenamento tipo, **struttura rinnovata** e adattata:

```
-- ============ ENTITÀ CORE ============
CREATE TABLE disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    prerequisiti TEXT,
    elementi_tecnici_specifici TEXT
);

CREATE TABLE stile (
    id_stile SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL, -- SL, DF, DO, RA, MISTI
    acronimo VARCHAR(5), -- SL, DF, DO, RA
    descrizione TEXT,
    id_disciplina INT REFERENCES disciplina(id_disciplina)
);

-- ============ ALLENAMENTO ============
CREATE TABLE allenamento (
    id_allenamento SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    tipologia VARCHAR(50), -- tecnico, aerobico, misto, potenza
    distanza_totale INT, -- 3200m nel tuo caso
    obiettivo TEXT,
    note TEXT
);

CREATE TABLE sezione (
    id_sezione SERIAL PRIMARY KEY,
    id_allenamento INT REFERENCES allenamento(id_allenamento),
    ordine INT NOT NULL, -- 1 = riscaldamento, 2 = centrale, 3 = defaticamento
    nome VARCHAR(100), -- "Riscaldamento", "Lavoro Tecnico Dorso"
    distanza_sezione INT
);

-- ============ SERIE (IL CUORE) ============
CREATE TABLE serie (
    id_serie SERIAL PRIMARY KEY,
    id_sezione INT REFERENCES sezione(id_sezione),
    ordine INT NOT NULL,
    
    -- Struttura serie
    ripetizioni INT NOT NULL, -- 6 in "6x100"
    distanza INT NOT NULL, -- 100 in "6x100"
    
    -- Timing
    tempo_partenza VARCHAR(20), -- "1:30", "1:45", oppure NULL se continuo
    recupero_secondi INT,
    
    -- Esecuzione
    modalita VARCHAR(50), -- 'superficie', 'sub', 'apnea', 'misto'
    focus_tecnico TEXT, -- "focus trazione", "braccio alto"
    
    note TEXT -- "3gb, 3" scivolo, sub, finisco a delfino completo"
);

-- ============ PATTERN STILE (PER ROTAZIONI) ============
CREATE TABLE serie_pattern_stile (
    id_pattern SERIAL PRIMARY KEY,
    id_serie INT REFERENCES serie(id_serie),
    sequenza INT NOT NULL, -- 1, 2, 3 per "uno SL, uno DF/DO, uno RA/SL"
    id_stile_primario INT REFERENCES stile(id_stile), -- SL
    id_stile_secondario INT REFERENCES stile(id_stile), -- DO (se misto tipo SL/DO)
    percentuale_primario INT DEFAULT 100, -- 50% se è 50/50 SL/DO
    
    UNIQUE(id_serie, sequenza)
);

-- ============ ATTREZZATURA ============
CREATE TABLE attrezzatura (
    id_attrezzatura SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL, -- pinne, palette, pull buoy, elastici, tavoletta
    categoria VARCHAR(30) -- gambe, braccia, galleggiamento, resistenza
);

CREATE TABLE serie_attrezzatura (
    id_serie INT REFERENCES serie(id_serie),
    id_attrezzatura INT REFERENCES attrezzatura(id_attrezzatura),
    obbligatoria BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id_serie, id_attrezzatura)
);

-- ============ ESERCIZI (CATALOGO TECNICO) ============
CREATE TABLE esercizio (
    id_esercizio SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    descrizione TEXT,
    id_stile INT REFERENCES stile(id_stile),
    
    -- Categorizzazione
    categoria VARCHAR(50), -- tecnica, respirazione, gambata, bracciata, virata
    livello VARCHAR(20), -- base, intermedio, avanzato
    
    focus_primario TEXT -- "trazione sottacqua", "rollata spalla", "presa acqua"
);

-- ============ PROGRESSIONE DIDATTICA ============
CREATE TABLE progressione_didattica (
    id_progressione SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    id_stile INT REFERENCES stile(id_stile),
    livello_partenza VARCHAR(50),
    livello_arrivo VARCHAR(50),
    durata_settimane INT,
    prerequisiti TEXT
);

CREATE TABLE progressione_esercizi (
    id_progressione INT REFERENCES progressione_didattica(id_progressione),
    id_esercizio INT REFERENCES esercizio(id_esercizio),
    settimana INT,
    ordine INT,
    PRIMARY KEY (id_progressione, id_esercizio, settimana)
);

-- ============ UTENTI ============
CREATE TABLE allievo (
    id_allievo SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    data_nascita DATE,
    livello_attuale VARCHAR(50),
    obiettivo TEXT,
    note_mediche TEXT
);

CREATE TABLE istruttore (
    id_istruttore SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cognome VARCHAR(100) NOT NULL,
    qualifiche TEXT[],
    anni_esperienza INT,
    specializzazione VARCHAR(100) -- tecnica, agonistica, salvamento
);

-- ============ CORSI ============
CREATE TABLE corso (
    id_corso SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    id_istruttore INT REFERENCES istruttore(id_istruttore),
    id_disciplina INT REFERENCES disciplina(id_disciplina),
    livello VARCHAR(50),
    data_inizio DATE,
    data_fine DATE,
    frequenza_settimanale INT -- 2, 3, 4 volte/settimana
);

CREATE TABLE corso_allievi (
    id_corso INT REFERENCES corso(id_corso),
    id_allievo INT REFERENCES allievo(id_allievo),
    PRIMARY KEY (id_corso, id_allievo)
);

-- ============ PISCINE E RECENSIONI ============
CREATE TABLE piscina (
    id_piscina SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    citta VARCHAR(100),
    indirizzo TEXT,
    lunghezza_vasca INT, -- 25m o 50m
    numero_corsie INT,
    temperatura_acqua DECIMAL(3,1),
    servizi TEXT[] -- ['spogliatoio', 'doccia calda', 'sauna', 'bar']
);

CREATE TABLE recensione (
    id_recensione SERIAL PRIMARY KEY,
    id_piscina INT REFERENCES piscina(id_piscina),
    id_utente INT, -- potrebbe essere allievo o istruttore
    voto INT CHECK (voto BETWEEN 1 AND 5),
    testo TEXT,
    data_recensione DATE DEFAULT CURRENT_DATE
);

-- ============ RISULTATI GARE ============
CREATE TABLE risultato (
    id_risultato SERIAL PRIMARY KEY,
    id_allievo INT REFERENCES allievo(id_allievo),
    id_stile INT REFERENCES stile(id_stile),
    distanza INT, -- 50, 100, 200, 400, 800, 1500
    tempo_secondi DECIMAL(6,2), -- 65.43 per 1:05.43
    data_gara DATE,
    nome_gara VARCHAR(200),
    vasca INT, -- 25 o 50
    categoria VARCHAR(50) -- Esordienti A, Ragazzi, Juniores, etc
);

CREATE TABLE brevetto (
    id_brevetto SERIAL PRIMARY KEY,
    id_allievo INT REFERENCES allievo(id_allievo),
    nome_brevetto VARCHAR(100), -- "Salvamento", "Istruttore FIN 1°", etc
    data_conseguimento DATE,
    ente_certificatore VARCHAR(100) -- FIN, FIPSAS, etc
);
```


### RICK
Per stare bene in acqua l'**ALLIEVO** necessita di raggiungere un **RISULTATO** in una **DISCIPLINA** tra quelle acquatiche. Per ottenerlo è fondamentale l'**ISTRUTTORE** che lo segue in **PISCINA**, dotata di **RECENSIONE** sulla cui base si può valutare il best fit. L'allievo alla fine otterrà il **BREVETTO** attraverso la frequenza del **CORSO** e lo svolgimento della **PROGRESSIONE_DIDATTICA** proposta tramite una sequenza multilaterale di diverse tipologie di **ESERCIZIO** utilizzati per apprendere la tecnica dello **STILE** di interesse. L'**ALLENAMENTO** consiste in tre **SEZIONI** - in genere riscaldamento, lavoro centrale e defaticamento - composte da un numero variabile di **SERIE** 

**ITALIANO**
```
PostgreSQL
├── allievo (nome, età, weekly_freq, livello_partenza, livello_obiettivo, record, note)
├── risulato (categoria, gara, tempo, atleta, data, vasca)
├── disciplina (nome, prerequisiti, elementi_tecnici_specifici)
├── istruttore (nome, età, qualifiche, anni_esperienza, orario disponibilità, filosofia)
├── piscina (nome, città, corsie, vasca, spogliatoio, doccia, segreteria, tariffe)
├── recensione (piscina, voto, testo, data)
├── brevetto (nome, alias, obiettivi_didattici)
├── corso (livello, allievi, orario, obiettivi, durata)
├── progressione_didattica (prerequisiti, esercizi, obiettivo)
├── esercizio (disciplina, stile_principale, gambe, braccia, descrizione)
├── stile (nome, descrizione, progressione_didattica)
├── allenamento (tipologia_tecnica, distanza_allenamento, data, obiettivo)
├── sezione (nome, serie, distanza_sezione)
├── serie (ripetizioni, distanza_serie, tempo, attrezzatura) 
```

**ENGLISH**
```
PostgreSQL
├── student (name, age, weekly_frequency, starting_level, target_level, record, notes)
├── result (category, competition, time, athlete, date, pool_length)
├── discipline (name, prerequisites, specific_technical_elements)
├── instructor (name, age, qualifications, years_experience, availability_schedule, philosophy)
├── swimming_pool (name, city, lanes, pool_type, changing_room, shower, reception, pricing)
├── review (swimming_pool, rating, text, date)
├── certification (name, legacy_name, learning_objectives)
├── course (level, students, schedule, objectives, duration)
├── training_progression (prerequisites, exercises, objective)
├── exercise (discipline, main_stroke, legs, arms, description)
├── stroke (name, description, training_progression)
├── training (technical_type, training_distance, date, objective)
├── section (name, sets, section_distance)
├── set (repetitions, set_distance, time, equipment)
```
## STRUTTURA REPOSITORY (Claudia tip)
Struttura consigliata

swim-school-db/
├── schema/
│   ├── create_tables.sql
│   └── constraints.sql
├── data/
│   ├── seed/
│   │   ├── discipline.sql
│   │   ├── stili.sql
│   │   └── esercizi_base.sql
│   └── entry/
│       ├── allievi.sql
│       ├── istruttori.sql
│       └── corsi.sql
├── migrations/
│   └── 001_initial_schema.sql
├── scripts/
│   └── import_data.sh
└── README.md
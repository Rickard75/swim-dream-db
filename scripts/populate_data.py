'''
"""
~~~~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~><(((('>~~~~~~~~~ | SWIM DREAM DB - Your Acquatic Trainer | ~~~~~~~~><(((('>~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ | ~~~~~~~~~~~~~~~~~~~~~~~~~


Description:
    
Author          : Riccardo Carroccio
Creation Date   : 2026-04-22
Last Update     : 2026-04-22
Version         : 1.0.0

Input:
    -
    -

Output:
    - connection to PostgreSQL database
    - insertion of fundamental catalogues
    - insertion of one master swimming training session

Dependencies:
    - pandas
    - numpy
    - 
    
Usage:
    python populate_data.py

Notes:
    - data insertion with direct INSERT operations (to develop idempotency)
    - 
'''

# Libraries
import os
import psycopg2
from dotenv import load_dotenv      # reads .env of the repo
from datetime import date

load_dotenv()

# Connection configuration variables
required = ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DATA", "POSTGRES_USER", "POSTGRES_PASS_PGSQL"]
missing = [k for k in required if not os.getenv(k)]
if missing:
    raise ValueError(f"Variabili .env mancanti: {', '.join(missing)}")

# PgSQL connection opening with params from .env
conn = psycopg2.connect(
    host     = os.getenv("POSTGRES_HOST", "localhost"),     # 2nd arg = alternative default 
    port     = int(os.getenv("POSTGRES_PORT", 5432)),
    database = os.getenv("POSTGRES_DATA", "swimming_db"),
    user     = os.getenv("POSTGRES_USER"),
    password = os.getenv("POSTGRES_PASS_PGSQL")
)
cur = conn.cursor() # object to execute query and commands on db

# ~~~~~~~~><(((('>~~~~~~~~~ DATA ENTRY into db tables with compact method ~~~~~~~~><(((('>~~~~~~~~~

first_swim_class = [
    {"Guidoski", 27, 3, "MASTER 2", "master"}
]

# ├── student (name, age, weekly_frequency, starting_level, target_level, record, notes)


''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GRAVEYARD START~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ============ 1. DISCIPLINE ============
discipline = [
    ('Nuoto', 'Saper galleggiare', 'Propulsione in acqua con tecniche codificate'),
    ('Nuoto Pinnato', 'Nuoto base', 'Uso pinne monopinna o bipinna'),
    ('Pallanuoto', 'Nuoto intermedio', 'Gioco di squadra acquatico'),
    ('Nuoto Sincronizzato', 'Nuoto avanzato', 'Coreografie acquatiche'),
    ('Salvamento', 'Nuoto avanzato', 'Tecniche di soccorso acquatico')
]

# executemany inserisce una lista di tuple in un solo blocco logico (piu compatto di tanti execute).
cur.executemany(
    "INSERT INTO disciplina (nome, prerequisiti, elementi_tecnici_specifici) VALUES (%s, %s, %s)",
    discipline
)

# ============ 2. STILI ============
stili = [
    ('Stile Libero', 'SL', 'Il crawl, stile più veloce', 1),
    ('Dorso', 'DO', 'Unico stile supino', 1),
    ('Rana', 'RA', 'Stile simmetrico, bracciata circolare', 1),
    ('Delfino/Farfalla', 'DF', 'Bracciata simultanea, ondulazione', 1),
    ('Misti', 'MX', 'Combinazione dei 4 stili', 1)
]

# Ogni tupla rispetta l'ordine delle colonne: nome, acronimo, descrizione, id_disciplina.
cur.executemany(
    "INSERT INTO stile (nome, acronimo, descrizione, id_disciplina) VALUES (%s, %s, %s, %s)",
    stili
)

# ============ 3. ATTREZZATURA ============
attrezzature = [
    ('Pinne', 'gambe'),
    ('Palette', 'braccia'),
    ('Pull Buoy', 'galleggiamento'),
    ('Tavoletta', 'gambe'),
    ('Elastici', 'resistenza'),
    ('Boccaglio frontale', 'respirazione'),
    ('Palette da dita', 'braccia'),
    ('Cavigliere', 'resistenza')
]

# Catalogo attrezzatura: utile per collegare una serie a uno o piu strumenti.
cur.executemany(
    "INSERT INTO attrezzatura (nome, categoria) VALUES (%s, %s)",
    attrezzature
)

# ============ 4. ESERCIZI BASE ============
esercizi_base = [
    # STILE LIBERO
    ('3SL3DO', 'Tre bracciate stile, tre bracciate dorso', 1, 'tecnica', 'base', 'Rollata e coordinazione'),
    ('Punto morto SL', 'Bracciata con pausa mano davanti', 1, 'tecnica', 'intermedio', 'Allungo e scivolamento'),
    ('Respirazione 3-5-7', 'Respirare ogni 3, 5 o 7 bracciate', 1, 'respirazione', 'base', 'Controllo respiratorio'),
    
    # DORSO
    ('Braccio alto dorso', 'Recupero con braccio teso alto', 2, 'tecnica', 'intermedio', 'Postura spalla'),
    ('Doppia bracciata DO', 'Due bracciate simultanee', 2, 'tecnica', 'base', 'Simmetria bracciata'),
    
    # RANA
    ('2 gambate 1 bracciata', 'Due gambate per ogni bracciata', 3, 'tecnica', 'intermedio', 'Timing gambata'),
    
    # DELFINO
    ('Gambata delfino', 'Solo ondulazione, braccia ferme', 4, 'gambata', 'base', 'Ondulazione del corpo'),
    ('Delfino subacqueo', 'Ondulazione in apnea', 4, 'tecnica', 'avanzato', 'Potenza e apnea')
]

# Insert massivo di esercizi tecnici di base per diversi stili.
cur.executemany(
    """INSERT INTO esercizio (nome, descrizione, id_stile, categoria, livello, focus_primario) 
       VALUES (%s, %s, %s, %s, %s, %s)""",
    esercizi_base
)

# ============ 5. IL TUO ALLENAMENTO ============
# Inserisci l'allenamento del 22 aprile 2024
# RETURNING id_allenamento: recupera subito l'ID generato per creare le relazioni figlie.
cur.execute(
    """INSERT INTO allenamento (data, tipologia, distanza_totale, obiettivo) 
       VALUES (%s, %s, %s, %s) RETURNING id_allenamento""",
    (date(2024, 4, 22), 'tecnico-misto', 3200, 'Lavoro tecnico multi-stile con apnea')
)
# fetchone()[0] prende il primo valore della prima riga restituita (l'ID appena creato).
id_allenamento = cur.fetchone()[0]

# Sezione 1: Riscaldamento
# Ogni sezione appartiene all'allenamento tramite FK id_allenamento.
cur.execute(
    """INSERT INTO sezione (id_allenamento, ordine, nome, distanza_sezione) 
       VALUES (%s, %s, %s, %s) RETURNING id_sezione""",
    (id_allenamento, 1, 'Riscaldamento Aerobico', 600)
)
id_sezione_1 = cur.fetchone()[0]

# Serie: 6x100 uno SL, uno DF/DO, uno RA/SL
# Questa serie e collegata alla sezione 1 tramite id_sezione_1.
cur.execute(
    """INSERT INTO serie (id_sezione, ordine, ripetizioni, distanza, modalita, note)
       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_serie""",
    (id_sezione_1, 1, 6, 100, 'superficie', 'Rotazione stili: SL, DF/DO, RA/SL')
)
id_serie_1 = cur.fetchone()[0]

# Pattern: 1=SL, 2=DF/DO, 3=RA/SL
# Tabella ponte che descrive una rotazione di stili all'interno della stessa serie.
cur.executemany(
    """INSERT INTO serie_pattern_stile (id_serie, sequenza, id_stile_primario, id_stile_secondario, percentuale_primario)
       VALUES (%s, %s, %s, %s, %s)""",
    [
        (id_serie_1, 1, 1, None, 100),  # SL puro
        (id_serie_1, 2, 4, 2, 50),       # DF/DO 50-50
        (id_serie_1, 3, 3, 1, 50)        # RA/SL 50-50
    ]
)

# Sezione 2: Lavoro apnea con pinne
# Nuova sezione nello stesso allenamento.
cur.execute(
    """INSERT INTO sezione (id_allenamento, ordine, nome, distanza_sezione) 
       VALUES (%s, %s, %s, %s) RETURNING id_sezione""",
    (id_allenamento, 2, 'Apnea e Pinnato', 200)
)
id_sezione_2 = cur.fetchone()[0]

# Serie: 8x25 sub con pinne 4DF, 4SL
# Serie apnea associata alla sezione 2.
cur.execute(
    """INSERT INTO serie (id_sezione, ordine, ripetizioni, distanza, modalita, note)
       VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_serie""",
    (id_sezione_2, 1, 8, 25, 'sub', '4 delfino, 4 stile libero')
)
id_serie_apnea = cur.fetchone()[0]

# Aggiungi pinne
# Inserisce il legame serie-attrezzatura cercando l'ID di 'Pinne' via sottoquery.
cur.execute(
    """INSERT INTO serie_attrezzatura (id_serie, id_attrezzatura) 
       VALUES (%s, (SELECT id_attrezzatura FROM attrezzatura WHERE nome = 'Pinne'))""",
    (id_serie_apnea,)
)

# Conferma tutte le operazioni pendenti nella transazione.
conn.commit()
# Chiusura risorse DB.
cur.close()
conn.close()

# Output finale di conferma per terminale.
print("✅ Database popolato con successo!")
print(f"   - Allenamento ID: {id_allenamento}")
print(f"   - Totale distanza: 3200m")

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GRAVEYARD END
'''
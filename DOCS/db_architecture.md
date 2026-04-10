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
### RICK
Per stare bene in acqua l'**ALLIEVO** necessita di raggiungere un **RISULTATO** in una **DISCIPLINA** tra quelle acquatiche. Per ottenerlo è fondamentale l'**ISTRUTTORE** che lo segue in **PISCINA**, dotata di **RECENSIONE** sulla cui base si può valutare il best fit. L'allievo alla fine otterrà il **BREVETTO** attraverso la frequenza del **CORSO** e lo svolgimento della **PROGRESSIONE_DIDATTICA** proposta tramite una sequenza multilaterale di diverse tipologie di **ESERCIZIO** utilizzati per apprendere la tecnica dello **STILE** di interesse. L'**ALLENAMENTO** consiste in tre **SEZIONI** - in genere riscaldamento, lavoro centrale e defaticamento - composte da un numero variabile di **SERIE**

```
PostgreSQL
├── allievo (nome, età, frequenza, livello_partenza, livello_obiettivo, record, note)
├── risulato (categoria, gara, tempo, atleta, data, vasca)
├── disciplina (nome, prerequisiti, elementi_tecnici_specifici)
├── istruttore (nome, età, qualifiche, anni_esperienza, orario disponibilità, filosofia)
├── piscina (nome, città, corsie, vasca, spogliatoio, doccia, segreteria, tariffe)
├── recensione (piscina, voto, testo, data)
├── brevetto (obiettivi_didattici)
├── corso (livello, allievi, orario, obiettivi, durata)
├── progressione_didattica (prerequisiti, esercizi, obiettivo)
├── esercizio (disciplina, stile_principale, gambe, braccia, descrizione)
├── stile (nome, descrizione, progressione_didattica)
├── allenamento (tipologia_tecnica, distanza_allenamento, data, obiettivo)
├── sezione (nome, serie, distanza_sezione)
├── serie (ripetizioni, distanza_serie, tempo, attrezzatura) 
```

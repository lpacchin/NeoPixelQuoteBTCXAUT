# Function Reference — INDEX (fotografia)

> Data: `2026-08-15` · SHA: `98a053e`  
> Proiezione derivata da `funcref.views` — rigenerata ad ogni assemblaggio.

## Sintesi

- Funzioni vive (ACTIVE): **36**
- Endpoint HTTP: **0**
- Moduli: **4**
- Copertura prosa LLM: **36/36** (100%)
- Moduli stale: non calcolabile in questa proiezione (richiede lo stato SHA precedente per il diff — demandato all'enforcement Plan E/F).

## Mappa di sistema (dominio → moduli)

> NOTA: nessun dominio configurato per questo progetto (`--domains` / env `FUNCREF_DOMAINS`, o preset `@<nome>`). I moduli sono elencati senza raggruppamento per dominio — nessun dominio inventato (CONTRACT #1).

**Moduli** (4, ordine alfabetico): `code`, `conf bck`, `scroll`, `webUI`

## Indice per route

| Metodo · Path | Funzione |
|---|---|
| — | nessun endpoint nell'inventario |

## Indice per env-var

| Env var | Letta da |
|---|---|
| — | nessuna env var letta in un corpo funzione |

## Security invariants

### Endpoint → auth_gate

| Metodo · Path | auth_gate |
|---|---|
| — | nessun endpoint |

### Endpoint senza gate di auth (`auth_gate == none`)

- nessuno (ogni endpoint ha un gate riconosciuto)

### Env var sensibili (match TOKEN|KEY|SECRET|PASSWORD) → chi le legge

> Solo NOMI delle variabili: i valori non compaiono mai (CONTRACT #5).

| Env var (nome) | Letta da |
|---|---|
| — | nessuna env var sensibile letta in un corpo funzione |

## Shared state (punti di contesa)

### Acquisizione lock (serializzazione / contesa) — `lock`

_(nessuna funzione con questo segnale)_

### Scrittura DB (cursore .execute*) — `db-write`

_(nessuna funzione con questo segnale)_

### Spawn di thread (background) — `thread`

_(nessuna funzione con questo segnale)_

### Scrittura file su disco — `file-write`

_(nessuna funzione con questo segnale)_

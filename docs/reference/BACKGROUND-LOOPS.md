# Function Reference — BACKGROUND-LOOPS

> Data: `2026-08-15` · SHA: `98a053e`  
> Proiezione derivata da `funcref.views` — rigenerata ad ogni assemblaggio.

> Candidati loop = funzioni con segnale di side-effect `thread` (spawn di thread). Lo **stato on/off NON è assunto**: i gate `*_AUTO`/`*_INTERVAL` sono letti a livello modulo (fuori dal corpo funzione), quindi non sono legati meccanicamente al singolo loop dall'inventario — vedi la unit systemd per lo stato reale (CLAUDE.md).

## Env-gate riconosciute (`*_AUTO` / `*_INTERVAL`)

_(nessuna env var `*_AUTO`/`*_INTERVAL` catturata in un corpo funzione: sono lette a livello modulo — vedi unit systemd)_

## Candidati loop (spawn thread)

_(nessuna funzione con segnale `thread` nell'inventario)_

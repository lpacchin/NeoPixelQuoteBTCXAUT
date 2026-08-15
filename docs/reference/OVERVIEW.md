# Function Reference — OVERVIEW (cosa fa il progetto, per aree)

> Data: `2026-08-15` · SHA: `98a053e`  
> Generato da `funcref.overview` — sintesi grounded, ACTIVE-only. Le aree sono una sintesi tematica ancorata a moduli reali dell'inventario; i moduli citati esistono tutti (gate anti-allucinazione).

## Cosa fa

Sistema per visualizzare su una matrice LED i prezzi correnti e le metriche giornaliere di criptovalute recuperate dall'API Bybit, includendo routine di rendering, gestione della connessione WiFi e logging diagnostico.

## Aree / capability

### Visualizzazione e rendering pixel

Funzioni per pulire il display, impostare singoli pixel e disegnare stringhe di testo come pattern sulla matrice LED, incluse eventuali animazioni iniziali.

Moduli: [`code`](code.md), [`conf bck`](conf bck.md), [`scroll`](scroll.md), [`webUI`](webUI.md)

### Acquisizione dati crypto e connettività

Recupero da Bybit di prezzo, massimo e minimo 24h per simboli come BTC e XAUT, con gestione di sessioni HTTP e connessione WiFi nei moduli che la prevedono.

Moduli: [`code`](code.md), [`conf bck`](conf bck.md), [`scroll`](scroll.md), [`webUI`](webUI.md)

### Composizione contenuti e diagnostica

Costruzione di segmenti di testo per lo scorrimento a partire dai dati crypto e registrazione di messaggi con timestamp per diagnostica e logging semplice.

Moduli: [`code`](code.md), [`conf bck`](conf bck.md), [`scroll`](scroll.md), [`webUI`](webUI.md)

## Flussi chiave

_(nessun flusso seed definito)_

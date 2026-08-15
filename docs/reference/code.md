# Reference: code

> SHA: `98a053e` · Copertura LLM: 8/8  
> Fotografia generata da `funcref.generate` — overview ACTIVE-only, storico completo nel corpo.

## Module Overview

Il modulo `code` possiede **8** funzioni ACTIVE, di cui **0** endpoint HTTP.  
Dipende da (chiamate uscenti cross-module): nessun modulo interno.  
È usato da (chiamate entranti cross-module): nessun modulo interno.

| Funzione | Firma | Route | Scopo |
|---|---|---|---|
| [`code.clear_display`](#code.clear_display) | `clear_display()` | `—` | Spegne o pulisce il display impostando tutti i pixel a nero e aggiornando la matrice LED. |
| [`code.draw_text`](#code.draw_text) | `draw_text(text, x_offset, color=WHITE)` | `—` | Disegna una stringa di testo come pattern di pixel a partire da un offset orizzontale, usando mappe di carattere predefinite. |
| [`code.get_crypto_data`](#code.get_crypto_data) | `get_crypto_data(requests, symbol)` | `—` | Recupera da Bybit prezzo, massimo e minimo 24h di una criptovaluta (BTC o XAUT) e li restituisce in un dizionario, oppure None in caso di errore. |
| [`code.log`](#code.log) | `log(message)` | `—` | Registra un messaggio con timestamp basato su tempo monotonic per diagnostica e logging semplice. |
| [`code.set_pixel`](#code.set_pixel) | `set_pixel(x, y, color)` | `—` | Imposta il colore di un pixel alle coordinate specificate se l'indice risultante è valido. |
| [`code.startup_animation`](#code.startup_animation) | `startup_animation()` | `—` | Esegue una sequenza di animazioni di avvio sulla matrice LED, alternando riempimento, lampeggio, dissolvenza e spegnimento graduale. |
| [`code.test_bybit`](#code.test_bybit) | `test_bybit()` | `—` | Mostra la scritta "BYBIT" su una matrice LED per verificare il layout, mantenendola visibile per 3 secondi. |
| [`code.xy_to_index`](#code.xy_to_index) | `xy_to_index(x, y)` | `—` | Converte coordinate 2D in indice lineare pixel, gestendo orientamento verticale/orizzontale, serpentina e righe invertite. |

---

<!-- fn:code.clear_display -->
## `code.clear_display` <a name="code.clear_display"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `clear_display()`  
**Async**: no  
**Posizione**: `code.py:50`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`code.startup_animation`](#code.startup_animation)  

**Scopo**: Spegne o pulisce il display impostando tutti i pixel a nero e aggiornando la matrice LED.

**Input**: Nessun parametro.

**Output**: Nessun valore di ritorno; aggiorna lo stato del display senza segnalare eccezioni.

**Gotcha**: —

<!-- fn:code.draw_text -->
## `code.draw_text` <a name="code.draw_text"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `draw_text(text, x_offset, color=WHITE)`  
**Async**: no  
**Posizione**: `code.py:183`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`code.set_pixel`](#code.set_pixel)  
**Chiamata da**: —  

**Scopo**: Disegna una stringa di testo come pattern di pixel a partire da un offset orizzontale, usando mappe di carattere predefinite.

**Input**: text: stringa iterabile; x_offset: int o float convertito a int; color: valore colore accettato da set_pixel (default WHITE).

**Output**: None; nessun valore di ritorno esplicito. Nessuna eccezione sollevata esplicitamente.

**Gotcha**: Caratteri non presenti in CHARS ignorati silenziosamente; x_offset troncato a intero; pixel fuori dall'intervallo 0 <= x_pos+x < MATRIX_WIDTH e fuori dalle righe y 0..7 vengono scartati.

<!-- fn:code.get_crypto_data -->
## `code.get_crypto_data` <a name="code.get_crypto_data"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `get_crypto_data(requests, symbol)`  
**Async**: no  
**Posizione**: `code.py:196`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`code.log`](#code.log)  
**Chiamata da**: —  

**Scopo**: Recupera da Bybit prezzo, massimo e minimo 24h di una criptovaluta (BTC o XAUT) e li restituisce in un dizionario, oppure None in caso di errore.

**Input**: requests: oggetto con metodo get (tipicamente modulo/sessione requests); symbol: stringa, solo 'BTC$' è mappato a BTC, ogni altro valore è mappato a XAUT.

**Output**: Dizionario {'price','high','low'} con valori float, oppure None se requests è None o la chiamata/parsing fallisce.

**Gotcha**: Il parametro symbol non è passato direttamente all'API: qualunque valore diverso da 'BTC$' interroga il simbolo XAUT. La funzione dipende dalla struttura esatta della risposta Bybit e richiede che 'gc' e 'log' siano disponibili nel namespace.

<!-- fn:code.log -->
## `code.log` <a name="code.log"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `log(message)`  
**Async**: no  
**Posizione**: `code.py:46`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`code.get_crypto_data`](#code.get_crypto_data), [`code.startup_animation`](#code.startup_animation), [`code.test_bybit`](#code.test_bybit)  

**Scopo**: Registra un messaggio con timestamp basato su tempo monotonic per diagnostica e logging semplice.

**Input**: message: qualsiasi oggetto, convertito in stringa tramite f-string; nessun vincolo di tipo o lunghezza.

**Output**: Ritorna None; stampa su stdout; nessuna eccezione dichiarata.

**Gotcha**: Il timestamp usa time.monotonic(), quindi non è un orario di calendario ma un tempo relativo arbitrario; l'output va su stdout e non viene intercettato o salvato.

<!-- fn:code.set_pixel -->
## `code.set_pixel` <a name="code.set_pixel"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `set_pixel(x, y, color)`  
**Async**: no  
**Posizione**: `code.py:72`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`code.xy_to_index`](#code.xy_to_index)  
**Chiamata da**: [`code.draw_text`](#code.draw_text), [`code.startup_animation`](#code.startup_animation), [`code.test_bybit`](#code.test_bybit)  

**Scopo**: Imposta il colore di un pixel alle coordinate specificate se l'indice risultante è valido.

**Input**: x, y: coordinate (tipicamente interi) per il calcolo dell'indice; color: valore colore.

**Output**: Nessun valore di ritorno; se l'indice non è nell'intervallo [0, NUM_LEDS) non fa nulla.

**Gotcha**: Dipende dalla funzione xy_to_index per la validazione; le coordinate invalide vengono silenziosamente ignorate; usa variabili globali pixels e NUM_LEDS.

<!-- fn:code.startup_animation -->
## `code.startup_animation` <a name="code.startup_animation"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `startup_animation()`  
**Async**: no  
**Posizione**: `code.py:78`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`code.clear_display`](#code.clear_display), [`code.log`](#code.log), [`code.set_pixel`](#code.set_pixel)  
**Chiamata da**: —  

**Scopo**: Esegue una sequenza di animazioni di avvio sulla matrice LED, alternando riempimento, lampeggio, dissolvenza e spegnimento graduale.

**Input**: Nessun parametro.

**Output**: Nessun valore di ritorno (None); nessuna eccezione dichiarata.

**Gotcha**: Richiede variabili globali MATRIX_WIDTH, MATRIX_HEIGHT, BLACK, pixels e costanti colore; usa attese bloccanti con time.sleep.

<!-- fn:code.test_bybit -->
## `code.test_bybit` <a name="code.test_bybit"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `test_bybit()`  
**Async**: no  
**Posizione**: `code.py:164`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`code.log`](#code.log), [`code.set_pixel`](#code.set_pixel)  
**Chiamata da**: —  

**Scopo**: Mostra la scritta "BYBIT" su una matrice LED per verificare il layout, mantenendola visibile per 3 secondi.

**Input**: nessun parametro

**Output**: ritorna None; nessuna eccezione prevista

**Gotcha**: dipende da variabili globali (MATRIX_WIDTH, CHARS, BLACK, WHITE, pixels) e assume che la larghezza del testo sia len(text)*6

<!-- fn:code.xy_to_index -->
## `code.xy_to_index` <a name="code.xy_to_index"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `xy_to_index(x, y)`  
**Async**: no  
**Posizione**: `code.py:55`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`code.set_pixel`](#code.set_pixel)  

**Scopo**: Converte coordinate 2D in indice lineare pixel, gestendo orientamento verticale/orizzontale, serpentina e righe invertite.

**Input**: x, y: interi; coordinate da validare rispetto a MATRIX_WIDTH e MATRIX_HEIGHT.

**Output**: Intero: indice pixel calcolato, oppure -1 se le coordinate sono fuori matrice.

**Gotcha**: Il calcolo dipende dalle costanti globali MATRIX_WIDTH, MATRIX_HEIGHT, VERTICAL, SERPENTINE e REVERSE_ROWS; non viene verificato il tipo di x e y.

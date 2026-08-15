# Reference: scroll

> SHA: `98a053e` · Copertura LLM: 8/8  
> Fotografia generata da `funcref.generate` — overview ACTIVE-only, storico completo nel corpo.

## Module Overview

Il modulo `scroll` possiede **8** funzioni ACTIVE, di cui **0** endpoint HTTP.  
Dipende da (chiamate uscenti cross-module): nessun modulo interno.  
È usato da (chiamate entranti cross-module): nessun modulo interno.

| Funzione | Firma | Route | Scopo |
|---|---|---|---|
| [`scroll.clear_display`](#scroll.clear_display) | `clear_display()` | `—` | Pulisce il display azzerando i pixel e mostrando l'aggiornamento. |
| [`scroll.connect_wifi`](#scroll.connect_wifi) | `connect_wifi()` | `—` | Stabilisce la connessione WiFi, crea una sessione requests con socketpool e contesto SSL e aggiorna il display con esito positivo o errore. |
| [`scroll.draw_text`](#scroll.draw_text) | `draw_text(text, x_offset, color=WHITE)` | `—` | Disegna il testo fornito sulla matrice LED, convertendolo in maiuscolo e accendendo i pixel corrispondenti a ogni carattere. |
| [`scroll.get_crypto_data`](#scroll.get_crypto_data) | `get_crypto_data(requests, symbol)` | `—` | Recupera i dati ticker correnti di una criptovaluta dall'API Bybit, restituendo prezzo, massimo e minimo delle ultime 24 ore. |
| [`scroll.log`](#scroll.log) | `log(message)` | `—` | Registra un messaggio su stdout anteponendo un timestamp basato sul tempo monotonic. |
| [`scroll.set_pixel`](#scroll.set_pixel) | `set_pixel(x, y, color)` | `—` | Imposta un singolo pixel alle coordinate indicate, se valide, per accendere o cambiare il colore del LED corrispondente. |
| [`scroll.test_bybit`](#scroll.test_bybit) | `test_bybit()` | `—` | Visualizza la scritta "BYBIT" centrata sul display a matrice per verificare il layout, poi pulisce lo schermo dopo 3 secondi. |
| [`scroll.xy_to_index`](#scroll.xy_to_index) | `xy_to_index(x, y)` | `—` | Converte coordinate 2D (x,y) nell'indice lineare del pixel nella strip LED, rispettando orientamento verticale/orizzontale, serpentina e righe invertite. |

---

<!-- fn:scroll.clear_display -->
## `scroll.clear_display` <a name="scroll.clear_display"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `clear_display()`  
**Async**: no  
**Posizione**: `scroll.py:51`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`scroll.log`](#scroll.log)  
**Chiamata da**: [`scroll.connect_wifi`](#scroll.connect_wifi), [`scroll.test_bybit`](#scroll.test_bybit)  

**Scopo**: Pulisce il display azzerando i pixel e mostrando l'aggiornamento.

**Input**: nessun parametro

**Output**: nessun valore di ritorno esplicito (None)

**Gotcha**: —

<!-- fn:scroll.connect_wifi -->
## `scroll.connect_wifi` <a name="scroll.connect_wifi"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `connect_wifi()`  
**Async**: no  
**Posizione**: `scroll.py:538`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`scroll.clear_display`](#scroll.clear_display), [`scroll.log`](#scroll.log), [`scroll.set_pixel`](#scroll.set_pixel)  
**Chiamata da**: —  

**Scopo**: Stabilisce la connessione WiFi, crea una sessione requests con socketpool e contesto SSL e aggiorna il display con esito positivo o errore.

**Input**: nessun parametro

**Output**: Restituisce un oggetto adafruit_requests.Session in caso di successo, oppure None in caso di eccezione durante la connessione o la creazione della sessione.

**Gotcha**: Utilizza variabili globali come WIFI_SSID, WIFI_PASSWORD, MATRIX_WIDTH e pixels; non propaga eccezioni ma le cattura e restituisce None, mostrando un pixel rosso sul display.

<!-- fn:scroll.draw_text -->
## `scroll.draw_text` <a name="scroll.draw_text"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `draw_text(text, x_offset, color=WHITE)`  
**Async**: no  
**Posizione**: `scroll.py:520`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`scroll.set_pixel`](#scroll.set_pixel)  
**Chiamata da**: —  

**Scopo**: Disegna il testo fornito sulla matrice LED, convertendolo in maiuscolo e accendendo i pixel corrispondenti a ogni carattere.

**Input**: text: str; x_offset: int, posizione orizzontale di partenza; color: default WHITE.

**Output**: Ritorna None; nessuna eccezione esplicita.

**Gotcha**: I caratteri non presenti in CHARS vengono ignorati; il testo è forzato a uppercase; ogni carattere occupa 5 pixel di larghezza.

<!-- fn:scroll.get_crypto_data -->
## `scroll.get_crypto_data` <a name="scroll.get_crypto_data"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `get_crypto_data(requests, symbol)`  
**Async**: no  
**Posizione**: `scroll.py:574`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`scroll.log`](#scroll.log)  
**Chiamata da**: —  

**Scopo**: Recupera i dati ticker correnti di una criptovaluta dall'API Bybit, restituendo prezzo, massimo e minimo delle ultime 24 ore.

**Input**: requests: oggetto con metodo get che restituisce response con .json() e .close(); symbol: stringa, atteso 'Bitcoin' (qualsiasi altro valore viene mappato a 'XAUT').

**Output**: Dict con chiavi price, high, low (float) in caso di successo; None se requests è None o in caso di eccezione.

**Gotcha**: Il mapping dei simboli è binario: solo 'Bitcoin' usa 'BTC', ogni altro valore usa 'XAUT'; utilizza la variabile globale 'gc' senza importarla localmente.

<!-- fn:scroll.log -->
## `scroll.log` <a name="scroll.log"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `log(message)`  
**Async**: no  
**Posizione**: `scroll.py:47`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`scroll.clear_display`](#scroll.clear_display), [`scroll.connect_wifi`](#scroll.connect_wifi), [`scroll.get_crypto_data`](#scroll.get_crypto_data), [`scroll.test_bybit`](#scroll.test_bybit)  

**Scopo**: Registra un messaggio su stdout anteponendo un timestamp basato sul tempo monotonic.

**Input**: message: stringa o valore interpolabile in f-string (deve supportare __str__ o __format__).

**Output**: Ritorna implicitamente None; non solleva eccezioni se message è formattabile.

**Gotcha**: Richiede che `time` sia importato nel modulo; il timestamp non è un'ora reale ma secondi da un punto arbitrario (monotonic).

<!-- fn:scroll.set_pixel -->
## `scroll.set_pixel` <a name="scroll.set_pixel"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `set_pixel(x, y, color)`  
**Async**: no  
**Posizione**: `scroll.py:81`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`scroll.xy_to_index`](#scroll.xy_to_index)  
**Chiamata da**: [`scroll.connect_wifi`](#scroll.connect_wifi), [`scroll.draw_text`](#scroll.draw_text), [`scroll.test_bybit`](#scroll.test_bybit)  

**Scopo**: Imposta un singolo pixel alle coordinate indicate, se valide, per accendere o cambiare il colore del LED corrispondente.

**Input**: x, y: interi con coordinate del pixel; color: valore colore (es. intero RGB). Nessuna validazione esplicita sui tipi o sui range in ingresso.

**Output**: Ritorna None; se l'indice calcolato è fuori intervallo [0, NUM_LEDS) non produce eccezioni e non applica modifiche.

**Gotcha**: Coordinate fuori range vengono ignorate silenziosamente; NUM_LEDS è una costante/globale di contesto, non un parametro della funzione.

<!-- fn:scroll.test_bybit -->
## `scroll.test_bybit` <a name="scroll.test_bybit"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `test_bybit()`  
**Async**: no  
**Posizione**: `scroll.py:492`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`scroll.clear_display`](#scroll.clear_display), [`scroll.log`](#scroll.log), [`scroll.set_pixel`](#scroll.set_pixel)  
**Chiamata da**: —  

**Scopo**: Visualizza la scritta "BYBIT" centrata sul display a matrice per verificare il layout, poi pulisce lo schermo dopo 3 secondi.

**Input**: nessun parametro

**Output**: ritorna None; nessuno stato/eccezione dichiarato

**Gotcha**: dipende da costanti/globali MATRIX_WIDTH, CHARS, WHITE e dall'oggetto pixels; i caratteri non presenti in CHARS vengono saltati senza errore

<!-- fn:scroll.xy_to_index -->
## `scroll.xy_to_index` <a name="scroll.xy_to_index"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `xy_to_index(x, y)`  
**Async**: no  
**Posizione**: `scroll.py:57`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`scroll.set_pixel`](#scroll.set_pixel)  

**Scopo**: Converte coordinate 2D (x,y) nell'indice lineare del pixel nella strip LED, rispettando orientamento verticale/orizzontale, serpentina e righe invertite.

**Input**: x e y: interi 0-based; se fuori dai limiti di MATRIX_WIDTH/MATRIX_HEIGHT la funzione restituisce -1.

**Output**: Intero non negativo: indice del pixel nella strip; -1 per coordinate fuori matrice; nessuna eccezione sollevata.

**Gotcha**: Dipende da costanti globali MATRIX_WIDTH, MATRIX_HEIGHT, VERTICAL, SERPENTINE e REVERSE_ROWS; l'ordine dell'indice cambia con VERTICAL e l'inversione con SERPENTINE/REVERSE_ROWS.

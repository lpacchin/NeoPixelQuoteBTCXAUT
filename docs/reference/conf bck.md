# Reference: conf bck

> SHA: `98a053e` · Copertura LLM: 9/9  
> Fotografia generata da `funcref.generate` — overview ACTIVE-only, storico completo nel corpo.

## Module Overview

Il modulo `conf bck` possiede **9** funzioni ACTIVE, di cui **0** endpoint HTTP.  
Dipende da (chiamate uscenti cross-module): nessun modulo interno.  
È usato da (chiamate entranti cross-module): nessun modulo interno.

| Funzione | Firma | Route | Scopo |
|---|---|---|---|
| [`conf bck.build_segments`](#conf_bck.build_segments) | `build_segments()` | `—` | Costruisce una lista di segmenti di testo formattati per ciascuna etichetta in LABEL1 e LABEL2, estraendo prezzo, massimo e minimo dalla struttura crypto. |
| [`conf bck.clear_display`](#conf_bck.clear_display) | `clear_display()` | `—` | Reimposta il display riempiendo la matrice LED con il colore nero e aggiornando la visualizzazione. |
| [`conf bck.connect_wifi`](#conf_bck.connect_wifi) | `connect_wifi()` | `—` | Stabilisce la connessione Wi-Fi e restituisce una sessione HTTP pronta all'uso, gestendo anche feedback visivi e log. |
| [`conf bck.draw_text`](#conf_bck.draw_text) | `draw_text(text, x_offset, color=WHITE)` | `—` | Disegna una stringa di testo sulla matrice LED convertendola in sprite per carattere e impostando i pixel accesi tramite set_pixel. |
| [`conf bck.get_crypto_data`](#conf_bck.get_crypto_data) | `get_crypto_data(sess, symbol)` | `—` | Recupera da Bybit i dati di prezzo corrente, massimo e minimo 24h per un simbolo spot e li restituisce normalizzati in float. |
| [`conf bck.log`](#conf_bck.log) | `log(msg)` | `—` | Permette di tracciare eventi con timestamp monotonic. |
| [`conf bck.read_config_file`](#conf_bck.read_config_file) | `read_config_file(filename='scroll.conf')` | `—` | Carica e interpreta un file di configurazione key=value, sovrascrivendo i valori predefiniti con quelli letti dal file; gestisce errori di lettura e parsing senza propagarli. |
| [`conf bck.set_pixel`](#conf_bck.set_pixel) | `set_pixel(x, y, color)` | `—` | Imposta il colore di un pixel LED se le coordinate sono valide. |
| [`conf bck.xy_to_index`](#conf_bck.xy_to_index) | `xy_to_index(x, y)` | `—` | Converte coordinate (x,y) in indice lineare di matrice LED, applicando layout verticale/orizzontale, serpentina e righe invertite. |

---

<!-- fn:conf bck.build_segments -->
## `conf bck.build_segments` <a name="conf_bck.build_segments"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `build_segments()`  
**Async**: no  
**Posizione**: `conf bck.py:201`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: —  

**Scopo**: Costruisce una lista di segmenti di testo formattati per ciascuna etichetta in LABEL1 e LABEL2, estraendo prezzo, massimo e minimo dalla struttura crypto.

**Input**: Nessun parametro; utilizza variabili globali LABEL1, LABEL2, crypto e costanti colore.

**Output**: Lista di dizionari con chiavi 'text', 'col', 'len' per ciascun segmento; nessuna eccezione gestita esplicitamente.

**Gotcha**: Assume che crypto[lbl] contenga le chiavi 'col', 'price', 'trend', 'high', 'low' e che i valori numerici siano convertibili a int; dipende da stato globale non passato come argomento.

<!-- fn:conf bck.clear_display -->
## `conf bck.clear_display` <a name="conf_bck.clear_display"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `clear_display()`  
**Async**: no  
**Posizione**: `conf bck.py:91`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`conf bck.connect_wifi`](#conf_bck.connect_wifi)  

**Scopo**: Reimposta il display riempiendo la matrice LED con il colore nero e aggiornando la visualizzazione.

**Input**: nessun parametro

**Output**: None; nessuna eccezione prevista

**Gotcha**: Utilizza oggetti globali `pixels` e `BLACK`; presuppone che la matrice sia già inizializzata.

<!-- fn:conf bck.connect_wifi -->
## `conf bck.connect_wifi` <a name="conf_bck.connect_wifi"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `connect_wifi()`  
**Async**: no  
**Posizione**: `conf bck.py:132`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`conf bck.clear_display`](#conf_bck.clear_display), [`conf bck.log`](#conf_bck.log)  
**Chiamata da**: —  

**Scopo**: Stabilisce la connessione Wi-Fi e restituisce una sessione HTTP pronta all'uso, gestendo anche feedback visivi e log.

**Input**: Nessun parametro; usa le variabili globali WIFI_SSID e WIFI_PASSWORD.

**Output**: Restituisce un oggetto adafruit_requests.Session in caso di successo, oppure None se la connessione o la creazione della sessione fallisce; non rilancia eccezioni perché vengono catturate.

**Gotcha**: Richiede hardware Wi-Fi configurato e credenziali globali valide; in caso di errore il chiamante deve gestire il valore None.

<!-- fn:conf bck.draw_text -->
## `conf bck.draw_text` <a name="conf_bck.draw_text"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `draw_text(text, x_offset, color=WHITE)`  
**Async**: no  
**Posizione**: `conf bck.py:118`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`conf bck.set_pixel`](#conf_bck.set_pixel)  
**Chiamata da**: —  

**Scopo**: Disegna una stringa di testo sulla matrice LED convertendola in sprite per carattere e impostando i pixel accesi tramite set_pixel.

**Input**: text: stringa/iterabile di caratteri; x_offset: intero, ascissa iniziale; color: valore colore accettato da set_pixel, default WHITE.

**Output**: None; non solleva eccezioni esplicite.

**Gotcha**: Il testo viene convertito in maiuscolo; i caratteri non presenti in CHARS sono saltati; il disegno è ritagliato orizzontalmente ai limiti di MATRIX_WIDTH.

<!-- fn:conf bck.get_crypto_data -->
## `conf bck.get_crypto_data` <a name="conf_bck.get_crypto_data"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `get_crypto_data(sess, symbol)`  
**Async**: no  
**Posizione**: `conf bck.py:149`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`conf bck.log`](#conf_bck.log)  
**Chiamata da**: —  

**Scopo**: Recupera da Bybit i dati di prezzo corrente, massimo e minimo 24h per un simbolo spot e li restituisce normalizzati in float.

**Input**: sess: oggetto con metodo get(url, headers) che espone .json()/.close(); symbol: stringa simbolo spot (es. "BTCUSDT").

**Output**: In successo: dict {price, high, low} float; None se sess è None, ret_code != 0, lista vuota o eccezione.

**Gotcha**: Assume che il primo elemento di result.list contenga lastPrice, highPrice24h, lowPrice24h; le eccezioni sono tutte catturate e loggate, quindi la funzione non propaga errori.

<!-- fn:conf bck.log -->
## `conf bck.log` <a name="conf_bck.log"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `log(msg)`  
**Async**: no  
**Posizione**: `conf bck.py:88`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`conf bck.connect_wifi`](#conf_bck.connect_wifi), [`conf bck.get_crypto_data`](#conf_bck.get_crypto_data)  

**Scopo**: Permette di tracciare eventi con timestamp monotonic.

**Input**: msg: qualsiasi valore formattabile tramite f-string; nessun vincolo di tipo.

**Output**: Nessun ritorno esplicito (None implicito); può sollevare eccezioni se msg non supporta la formattazione.

**Gotcha**: Richiede che `time` sia importato nel modulo; `time.monotonic()` non è il tempo di sistema ma un orologio monotonic.

<!-- fn:conf bck.read_config_file -->
## `conf bck.read_config_file` <a name="conf_bck.read_config_file"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `read_config_file(filename='scroll.conf')`  
**Async**: no  
**Posizione**: `conf bck.py:11`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: —  

**Scopo**: Carica e interpreta un file di configurazione key=value, sovrascrivendo i valori predefiniti con quelli letti dal file; gestisce errori di lettura e parsing senza propagarli.

**Input**: filename: stringa opzionale, percorso del file di configurazione (default 'scroll.conf').

**Output**: Restituisce sempre un dict con chiavi di configurazione e valori tipizzati (str, float, int); in caso di OSError stampa un messaggio e restituisce i valori di default.

**Gotcha**: Se una riga contiene '=' ma il parsing del valore fallisce (es. int non valido senza punto decimale), la chiave non viene aggiornata, mantenendo il valore di default eventualmente presente.

<!-- fn:conf bck.set_pixel -->
## `conf bck.set_pixel` <a name="conf_bck.set_pixel"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `set_pixel(x, y, color)`  
**Async**: no  
**Posizione**: `conf bck.py:108`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`conf bck.xy_to_index`](#conf_bck.xy_to_index)  
**Chiamata da**: [`conf bck.draw_text`](#conf_bck.draw_text)  

**Scopo**: Imposta il colore di un pixel LED se le coordinate sono valide.

**Input**: x e y: interi coordinati; color: valore compatibile con l'elemento di pixels.

**Output**: None; nessun valore di ritorno o eccezione prevista.

**Gotcha**: Se l'indice calcolato è fuori dall'intervallo 0..NUM_LEDS-1, la funzione non esegue alcuna assegnazione.

<!-- fn:conf bck.xy_to_index -->
## `conf bck.xy_to_index` <a name="conf_bck.xy_to_index"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `xy_to_index(x, y)`  
**Async**: no  
**Posizione**: `conf bck.py:96`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`conf bck.set_pixel`](#conf_bck.set_pixel)  

**Scopo**: Converte coordinate (x,y) in indice lineare di matrice LED, applicando layout verticale/orizzontale, serpentina e righe invertite.

**Input**: x e y interi attesi; coordinate entro x in [0, MATRIX_WIDTH-1] e y in [0, MATRIX_HEIGHT-1].

**Output**: Intero indice base 0 se coordinate valide, -1 se fuori matrice; nessuna eccezione.

**Gotcha**: Il verso di scansione dipende dalle costanti globali VERTICAL, SERPENTINE e REVERSE_ROWS; con REVERSE_ROWS=True l'inversione avviene su colonne/righe pari invece che dispari.

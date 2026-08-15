# Reference: webUI

> SHA: `98a053e` · Copertura LLM: 11/11  
> Fotografia generata da `funcref.generate` — overview ACTIVE-only, storico completo nel corpo.

## Module Overview

Il modulo `webUI` possiede **11** funzioni ACTIVE, di cui **0** endpoint HTTP.  
Dipende da (chiamate uscenti cross-module): nessun modulo interno.  
È usato da (chiamate entranti cross-module): nessun modulo interno.

| Funzione | Firma | Route | Scopo |
|---|---|---|---|
| [`webUI.clear_display`](#webUI.clear_display) | `clear_display()` | `—` | Esegue la routine di pulizia del display, registrando l'operazione prima di pulire la matrice di pixel. |
| [`webUI.connect_wifi`](#webUI.connect_wifi) | `connect_wifi()` | `—` | Stabilisce la connessione WiFi, crea sessione requests e socketpool/SSL context e fornisce feedback visivo sulla matrice. |
| [`webUI.draw_text`](#webUI.draw_text) | `draw_text(text, x_offset, color=WHITE)` | `—` | Disegna una stringa di testo sulla matrice LED convertendola in maiuscolo e accendendo i pixel dei caratteri noti a partire da un offset orizzontale. |
| [`webUI.generate_scroll_segments`](#webUI.generate_scroll_segments) | `generate_scroll_segments()` | `—` | Costruisce i segmenti visuali per lo scorrimento combinando simbolo, prezzo, high e low dai dati crypto configurati. |
| [`webUI.get_crypto_data`](#webUI.get_crypto_data) | `get_crypto_data(requests, symbol)` | `—` | Recupera da Bybit i dati correnti di prezzo, massimo e minimo giornaliero per un simbolo crypto, adattando i nomi visualizzati ai simboli API. |
| [`webUI.log`](#webUI.log) | `log(message)` | `—` | Registra un messaggio con timestamp monotonico, utile per tracciare eventi in ordine temporale. |
| [`webUI.set_pixel`](#webUI.set_pixel) | `set_pixel(x, y, color)` | `—` | Imposta un singolo pixel LED alle coordinate (x,y) calcolando l'indice lineare e aggiornando l'array globale pixels se l'indice rientra nel range valido. |
| [`webUI.show_ip`](#webUI.show_ip) | `show_ip()` | `—` | Mostra sul display a matrice l'indirizzo IP Wi-Fi, centrandolo e mantenendolo visibile per 3 secondi. |
| [`webUI.update_crypto_data`](#webUI.update_crypto_data) | `update_crypto_data()` | `—` | Aggiorna il dizionario globale dei dati criptovalute per tutti i simboli configurati e rigenera i segmenti di scorrimento dell'interfaccia. |
| [`webUI.web_page`](#webUI.web_page) | `web_page()` | `—` | Genera l'HTML della pagina di controllo LED Matrix con form per aggiornare simboli e impostazioni. |
| [`webUI.xy_to_index`](#webUI.xy_to_index) | `xy_to_index(x, y)` | `—` | Converte coordinate logiche x,y nell'indice lineare del pixel nella strip LED, gestendo layout verticali/orizzontali e serpentina. |

---

<!-- fn:webUI.clear_display -->
## `webUI.clear_display` <a name="webUI.clear_display"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `clear_display()`  
**Async**: no  
**Posizione**: `webUI.py:61`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`webUI.log`](#webUI.log)  
**Chiamata da**: [`webUI.connect_wifi`](#webUI.connect_wifi), [`webUI.show_ip`](#webUI.show_ip)  

**Scopo**: Esegue la routine di pulizia del display, registrando l'operazione prima di pulire la matrice di pixel.

**Input**: Nessun parametro.

**Output**: Restituisce None; nessuna eccezione esplicita.

**Gotcha**: Assume che le variabili globali `pixels` e `BLACK` esistano e che il display sia già inizializzato; un errore su globals non è gestito.

<!-- fn:webUI.connect_wifi -->
## `webUI.connect_wifi` <a name="webUI.connect_wifi"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `connect_wifi()`  
**Async**: no  
**Posizione**: `webUI.py:543`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`webUI.clear_display`](#webUI.clear_display), [`webUI.log`](#webUI.log), [`webUI.set_pixel`](#webUI.set_pixel)  
**Chiamata da**: —  

**Scopo**: Stabilisce la connessione WiFi, crea sessione requests e socketpool/SSL context e fornisce feedback visivo sulla matrice.

**Input**: Nessun parametro; usa variabili globali WIFI_SSID e WIFI_PASSWORD.

**Output**: Restituisce tupla (requests, pool) in caso di successo; (None, None) se la connessione o la creazione della sessione fallisce.

**Gotcha**: Richiede hardware WiFi e variabili globali configurate; modifica temporaneamente il display a LED e può sollevare eccezioni gestite.

<!-- fn:webUI.draw_text -->
## `webUI.draw_text` <a name="webUI.draw_text"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `draw_text(text, x_offset, color=WHITE)`  
**Async**: no  
**Posizione**: `webUI.py:525`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`webUI.set_pixel`](#webUI.set_pixel)  
**Chiamata da**: [`webUI.show_ip`](#webUI.show_ip)  

**Scopo**: Disegna una stringa di testo sulla matrice LED convertendola in maiuscolo e accendendo i pixel dei caratteri noti a partire da un offset orizzontale.

**Input**: text: stringa/iterabile di caratteri, convertita in maiuscolo; x_offset: int, coordinata x iniziale; color: valore colore opzionale, default WHITE, passato a set_pixel.

**Output**: Nessun valore di ritorno (None). Non solleva eccezioni documentate: i caratteri non presenti in CHARS vengono ignorati.

**Gotcha**: Il testo viene forzato in maiuscolo e i caratteri sconosciuti sono saltati silenziosamente. Il clipping controlla solo x_pos+x < MATRIX_WIDTH: x_offset negativo può generare coordinate negative passate a set_pixel.

<!-- fn:webUI.generate_scroll_segments -->
## `webUI.generate_scroll_segments` <a name="webUI.generate_scroll_segments"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `generate_scroll_segments()`  
**Async**: no  
**Posizione**: `webUI.py:683`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`webUI.update_crypto_data`](#webUI.update_crypto_data)  

**Scopo**: Costruisce i segmenti visuali per lo scorrimento combinando simbolo, prezzo, high e low dai dati crypto configurati.

**Input**: Nessun parametro; dipende dalle variabili globali config, crypto_data e dalle costanti WHITE, CYAN, PURPLE.

**Output**: None (nessun return esplicito); può sollevare KeyError o TypeError se config/crypto_data non contengono i campi attesi o i valori non sono convertibili a int.

**Gotcha**: Presuppone che ogni simbolo in config['symbols'] sia presente in crypto_data e che i campi price, high e low siano numerici; la lunghezza di ogni segmento deve riflettere il testo effettivo.

<!-- fn:webUI.get_crypto_data -->
## `webUI.get_crypto_data` <a name="webUI.get_crypto_data"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `get_crypto_data(requests, symbol)`  
**Async**: no  
**Posizione**: `webUI.py:579`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`webUI.log`](#webUI.log)  
**Chiamata da**: [`webUI.update_crypto_data`](#webUI.update_crypto_data)  

**Scopo**: Recupera da Bybit i dati correnti di prezzo, massimo e minimo giornaliero per un simbolo crypto, adattando i nomi visualizzati ai simboli API.

**Input**: requests: oggetto con metodo get() HTTP; symbol: stringa non nulla, confrontata case-insensitive con BITCOIN/BTC, altrimenti mappata a XAUT.

**Output**: Dict con chiavi price, high, low (float) oppure None in caso di richiesta mancante o errore API/parsing.

**Gotcha**: Il simbolo non BITCOIN/BTC viene forzato a XAUT; utilizza gc e log come nomi globali; eventuali chiavi mancanti nella risposta API generano eccezione catturata e restituiscono None.

<!-- fn:webUI.log -->
## `webUI.log` <a name="webUI.log"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `log(message)`  
**Async**: no  
**Posizione**: `webUI.py:57`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`webUI.clear_display`](#webUI.clear_display), [`webUI.connect_wifi`](#webUI.connect_wifi), [`webUI.get_crypto_data`](#webUI.get_crypto_data), [`webUI.show_ip`](#webUI.show_ip)  

**Scopo**: Registra un messaggio con timestamp monotonico, utile per tracciare eventi in ordine temporale.

**Input**: message: qualsiasi oggetto formattabile come stringa; nessun vincolo di tipo.

**Output**: None; può sollevare NameError se `time` non è importato nel modulo.

**Gotcha**: Richiede `import time` nel contesto; il timestamp è relativo (time.monotonic) e non un orario di calendario.

<!-- fn:webUI.set_pixel -->
## `webUI.set_pixel` <a name="webUI.set_pixel"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `set_pixel(x, y, color)`  
**Async**: no  
**Posizione**: `webUI.py:91`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`webUI.xy_to_index`](#webUI.xy_to_index)  
**Chiamata da**: [`webUI.connect_wifi`](#webUI.connect_wifi), [`webUI.draw_text`](#webUI.draw_text)  

**Scopo**: Imposta un singolo pixel LED alle coordinate (x,y) calcolando l'indice lineare e aggiornando l'array globale pixels se l'indice rientra nel range valido.

**Input**: x, y: coordinate numeriche intere; color: valore colore accettato dal backend (es. tupla RGB). Nessuna validazione esplicita dei tipi.

**Output**: Nessun ritorno (None). Se l'indice calcolato è fuori da [0, NUM_LEDS), non esegue scrittura e termina silenziosamente.

**Gotcha**: Se xy_to_index restituisce un indice fuori range la funzione non solleva eccezioni; NUM_LEDS e pixels sono variabili globali, ma nessun side effect è segnalato.

<!-- fn:webUI.show_ip -->
## `webUI.show_ip` <a name="webUI.show_ip"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `show_ip()`  
**Async**: no  
**Posizione**: `webUI.py:512`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`webUI.clear_display`](#webUI.clear_display), [`webUI.draw_text`](#webUI.draw_text), [`webUI.log`](#webUI.log)  
**Chiamata da**: —  

**Scopo**: Mostra sul display a matrice l'indirizzo IP Wi-Fi, centrandolo e mantenendolo visibile per 3 secondi.

**Input**: Nessun parametro.

**Output**: Ritorna implicitamente None; nessuna eccezione esplicita.

**Gotcha**: Usa variabili globali (MATRIX_WIDTH, WHITE, wifi, pixels) e blocca l'esecuzione per 3 secondi con time.sleep.

<!-- fn:webUI.update_crypto_data -->
## `webUI.update_crypto_data` <a name="webUI.update_crypto_data"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `update_crypto_data()`  
**Async**: no  
**Posizione**: `webUI.py:751`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`webUI.generate_scroll_segments`](#webUI.generate_scroll_segments), [`webUI.get_crypto_data`](#webUI.get_crypto_data)  
**Chiamata da**: —  

**Scopo**: Aggiorna il dizionario globale dei dati criptovalute per tutti i simboli configurati e rigenera i segmenti di scorrimento dell'interfaccia.

**Input**: Nessun parametro; legge le variabili globali 'crypto_data' (dizionario) e 'config' (con chiave 'symbols').

**Output**: Non restituisce alcun valore; modifica il dizionario globale 'crypto_data' e chiama 'generate_scroll_segments()' senza gestire eccezioni.

**Gotcha**: Assume che 'config["symbols"]' sia presente e iterabile e che 'crypto_data' sia un dizionario già inizializzato; la chiamata a 'get_crypto_data' può fallire senza che la funzione lo gestisca.

<!-- fn:webUI.web_page -->
## `webUI.web_page` <a name="webUI.web_page"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `web_page()`  
**Async**: no  
**Posizione**: `webUI.py:624`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: —  

**Scopo**: Genera l'HTML della pagina di controllo LED Matrix con form per aggiornare simboli e impostazioni.

**Input**: nessun parametro; usa la variabile globale `config`.

**Output**: Ritorna una stringa HTML (str); può sollevare eccezioni se `config` o le sue chiavi non sono disponibili.

**Gotcha**: La funzione dipende da una variabile globale `config` con chiavi `symbols`, `brightness`, `scroll_speed`, `scroll_delay` e non esegue escaping dei valori interpolati.

<!-- fn:webUI.xy_to_index -->
## `webUI.xy_to_index` <a name="webUI.xy_to_index"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `xy_to_index(x, y)`  
**Async**: no  
**Posizione**: `webUI.py:67`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`webUI.set_pixel`](#webUI.set_pixel)  

**Scopo**: Converte coordinate logiche x,y nell'indice lineare del pixel nella strip LED, gestendo layout verticali/orizzontali e serpentina.

**Input**: Due interi x e y; valori fuori dagli intervalli [0, MATRIX_WIDTH-1] e [0, MATRIX_HEIGHT-1] restituiscono -1.

**Output**: Intero: indice del pixel >=0 oppure -1 se le coordinate sono fuori matrice; nessuna eccezione.

**Gotcha**: Il risultato dipende dai flag globali VERTICAL, SERPENTINE e REVERSE_ROWS; i limiti sono controllati prima dell'accesso agli indici.

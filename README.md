# NeoPixelQuoteBTCXAUT

Firmware CircuitPython per matrice NeoPixel 32x8 - Display quotazioni BTC e XAUT (oro tokenizzato) con scrolling.

## Descrizione

Visualizza quotazioni Bitcoin e XAUT (Tether Gold) su una matrice NeoPixel WS2812B 32x8 pixel. Include tre modalita operative: display statico con prezzi e variazioni, scrolling continuo dei dati, e interfaccia web per configurazione remota. Supporta layout serpentina verticale.

## Funzionalita

- **Quotazioni BTC e XAUT** in tempo reale da API web
- **Tre modalita operative**:
  - `code.py` - Display statico con prezzi, High/Low, variazione percentuale
  - `scroll.py` - Scrolling continuo con prezzi e High/Low
  - `webUI.py` - Interfaccia web per configurazione e controllo remoto
- **Colori per asset**: arancione (BTC), oro (XAUT)
- **Indicazione variazione**: verde (positiva), rosso (negativa)
- **High/Low** in ciano e viola
- **Layout matrice configurabile**: serpentina, verticale, reverse rows
- **Luminosita regolabile** (hardware e via web)
- **Animazione di startup**
- **Server HTTP integrato** (modalita webUI) per controllo da browser
- **File di configurazione** `scroll.conf` per parametri scrolling

## Stack Tecnologico

- **Microcontrollore**: ESP32-S3 (o compatibile CircuitPython)
- **Display**: Matrice NeoPixel WS2812B 32x8 (256 LED)
- **Linguaggio**: CircuitPython
- **Librerie**: neopixel, adafruit_requests, adafruit_connection_manager, adafruit_httpserver
- **Pin dati**: IO38 / D38

## Configurazione

Credenziali Wi-Fi nel file `settings.toml`.

## Struttura File

| File/Cartella | Descrizione |
|---------------|-------------|
| `code.py` | Modalita display statico con prezzi BTC/XAUT |
| `scroll.py` | Modalita scrolling continuo |
| `webUI.py` | Modalita con interfaccia web per controllo remoto |
| `conf bck.py` | Backup configurazione |
| `scroll.conf` | Parametri configurazione scrolling |
| `price.txt` | Cache locale prezzi |
| `lib/` | Librerie CircuitPython |
| `sd/` | File su SD card |
| `settings.toml` | Configurazione Wi-Fi |
| `boot_out.txt` | Output boot CircuitPython |

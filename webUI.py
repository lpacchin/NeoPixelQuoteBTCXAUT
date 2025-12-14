# main_web.py - Versione con interfaccia web e visualizzazione IP
import board
import neopixel
import time
import wifi
import socketpool
import adafruit_requests
import gc
import adafruit_connection_manager
import microcontroller
from adafruit_httpserver import Server, Request, Response

# --- CONFIGURAZIONE ---
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
NUM_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN = board.D38
BRIGHTNESS = 0.3

WIFI_SSID = "lupa"
WIFI_PASSWORD = "780130bmw."

# Configurazione layout matrice
# Cambia questi valori in base al tuo layout
SERPENTINE = True      # True se il layout è a serpentina, False se è lineare
VERTICAL = True        # True se le strip corrono verticalmente, False se orizzontalmente
REVERSE_ROWS = False   # True se le righe dispari vanno da destra a sinistra

# Colori più vividi per miglior visibilità
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0)    # Bitcoin - più intenso
GOLD = (255, 200, 0)      # Gold - più intenso
RED = (255, 0, 0)         # Negativo
GREEN = (0, 255, 0)       # Positivo
BLUE = (0, 0, 255)        # Connessione
WHITE = (255, 255, 255)   # Per test
CYAN = (0, 255, 255)      # Per High
PURPLE = (255, 0, 255)    # Per Low

# Configurazione globale modificabile tramite web
config = {
    "symbols": ["Bitcoin", "Gold"],
    "brightness": BRIGHTNESS,
    "scroll_speed": 1,
    "scroll_delay": 0.03
}

# --- INIZIALIZZAZIONE HARDWARE ---
print("[INIT] Inizializzazione NeoPixel...")
pixels = neopixel.NeoPixel(
    DATA_PIN, NUM_LEDS,
    brightness=config["brightness"],
    auto_write=False
)

# --- FUNZIONI DI UTILITÀ ---
def log(message):
    """Funzione per log con timestamp"""
    print(f"[{time.monotonic():.1f}s] {message}")

def clear_display():
    """Pulisce il display"""
    log("Pulizia display")
    pixels.fill(BLACK)
    pixels.show()

def xy_to_index(x, y):
    """Converte coordinate x,y in indice del pixel nella strip"""
    if x < 0 or x >= MATRIX_WIDTH or y < 0 or y >= MATRIX_HEIGHT:
        return -1  # Fuori dai limiti

    if VERTICAL:
        # Layout verticale (le strip corrono dall'alto verso il basso)
        if SERPENTINE and ((x % 2 == 1) ^ REVERSE_ROWS):
            # Colonne dispari invertite in layout serpentina
            index = x * MATRIX_HEIGHT + (MATRIX_HEIGHT - 1 - y)
        else:
            # Colonne pari o layout non serpentina
            index = x * MATRIX_HEIGHT + y
    else:
        # Layout orizzontale (le strip corrono da sinistra a destra)
        if SERPENTINE and ((y % 2 == 1) ^ REVERSE_ROWS):
            # Righe dispari invertite in layout serpentina
            index = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
        else:
            # Righe pari o layout non serpentina
            index = y * MATRIX_WIDTH + x

    return index

def set_pixel(x, y, color):
    """Imposta un singolo pixel alle coordinate x,y"""
    index = xy_to_index(x, y)
    if 0 <= index < NUM_LEDS:
        pixels[index] = color

# Definizione caratteri 4x8 (più grandi e più leggibili)
# Ogni carattere è rappresentato da una matrice 4x8
CHARS = {
    'A': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'B': [
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [0,0,0,0]
    ],
    'C': [
        [0,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [0,1,1,1],
        [0,0,0,0]
    ],
    'D': [
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [0,0,0,0]
    ],
    'E': [
        [1,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    'F': [
        [1,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ],
    'G': [
        [0,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,1],
        [0,0,0,0]
    ],
    'H': [
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'I': [
        [1,1,1,1],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    'J': [
        [0,0,1,1],
        [0,0,1,1],
        [0,0,1,1],
        [0,0,1,1],
        [0,0,1,1],
        [1,0,1,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'K': [
        [1,0,0,1],
        [1,0,1,0],
        [1,1,0,0],
        [1,1,0,0],
        [1,0,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'L': [
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    'M': [
        [1,0,0,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'N': [
        [1,0,0,1],
        [1,1,0,1],
        [1,1,0,1],
        [1,0,1,1],
        [1,0,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'O': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'P': [
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ],
    'Q': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,1,1],
        [1,0,0,1],
        [0,1,1,1],
        [0,0,0,0]
    ],
    'R': [
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [1,0,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'S': [
        [0,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [0,1,1,0],
        [0,0,0,1],
        [0,0,0,1],
        [1,1,1,0],
        [0,0,0,0]
    ],
    'T': [
        [1,1,1,1],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'U': [
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'V': [
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'W': [
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,1],
        [1,1,1,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'X': [
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,0,0,0]
    ],
    'Y': [
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ],
    'Z': [
        [1,1,1,1],
        [0,0,0,1],
        [0,0,1,0],
        [0,1,0,0],
        [0,1,0,0],
        [1,0,0,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    '0': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    '1': [
        [0,1,1,0],
        [1,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,1,1,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    '2': [
        [0,1,1,0],
        [1,0,0,1],
        [0,0,0,1],
        [0,0,1,0],
        [0,1,0,0],
        [1,0,0,0],
        [1,1,1,1],
        [0,0,0,0]
    ],
    '3': [
        [1,1,1,0],
        [0,0,0,1],
        [0,0,0,1],
        [0,1,1,0],
        [0,0,0,1],
        [0,0,0,1],
        [1,1,1,0],
        [0,0,0,0]
    ],
    '4': [
        [0,0,1,0],
        [0,1,1,0],
        [1,0,1,0],
        [1,0,1,0],
        [1,1,1,1],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,0,0]
    ],
    '5': [
        [1,1,1,1],
        [1,0,0,0],
        [1,1,1,0],
        [0,0,0,1],
        [0,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    '6': [
        [0,1,1,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    '7': [
        [1,1,1,1],
        [0,0,0,1],
        [0,0,1,0],
        [0,0,1,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,0,0,0]
    ],
    '8': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    '9': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,1],
        [0,0,0,1],
        [0,0,0,1],
        [0,1,1,0],
        [0,0,0,0]
    ],
    ' ': [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    ':': [
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    '-': [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ],
    '.': [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]
    ],
    '/': [
        [0,0,0,1],
        [0,0,0,1],
        [0,0,1,0],
        [0,0,1,0],
        [0,1,0,0],
        [0,1,0,0],
        [1,0,0,0],
        [0,0,0,0]
    ],
}

def show_ip():
    """Mostra l'IP sul display"""
    ip_str = str(wifi.radio.ipv4_address)
    log(f"Mostrando IP: {ip_str}")
    clear_display()

    # Mostra l'IP centrato
    x_start = (MATRIX_WIDTH - len(ip_str) * 5) // 2
    draw_text(ip_str, x_start, WHITE)
    pixels.show()
    time.sleep(3)
    clear_display()

def draw_text(text, x_offset, color=WHITE):
    """Disegna il testo alla posizione x_offset"""
    text = text.upper()

    # Per ogni carattere
    for i, char in enumerate(text):
        if char in CHARS:
            char_pattern = CHARS[char]
            x_pos = x_offset + i * 5

            # Per ogni riga e colonna del carattere
            for y in range(8):
                for x in range(4):
                    if char_pattern[y][x]:
                        if 0 <= x_pos + x < MATRIX_WIDTH:  # Solo se visibile
                            set_pixel(x_pos + x, y, color)

# --- FUNZIONI RETE ---
def connect_wifi():
    log("Connessione WiFi in corso...")
    try:
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
        log(f"WiFi connesso, IP: {wifi.radio.ipv4_address}")

        # Usa connection_manager per ottenere sia socketpool che ssl_context
        log("Creazione socketpool e ssl_context...")
        pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

        # Crea la sessione requests con entrambi i parametri
        log("Creazione sessione requests...")
        requests = adafruit_requests.Session(pool, ssl_context)

        # Visualizza connessione riuscita
        for i in range(MATRIX_WIDTH):
            set_pixel(i, 0, BLUE)
        pixels.show()
        time.sleep(1)
        clear_display()

        log("Garbage collection dopo connessione...")
        gc.collect()
        log(f"Memoria libera: {gc.mem_free()} bytes")
        return requests, pool
    except Exception as e:
        log(f"Errore connessione WiFi: {e}")
        # Visualizza errore
        for i in range(MATRIX_WIDTH):
            set_pixel(i, 0, RED)
        pixels.show()
        time.sleep(1)
        clear_display()
        return None, None

def get_crypto_data(requests, symbol):
    if requests is None:
        log("Impossibile ottenere dati: requests è None")
        return None

    # Mappa i nomi visualizzati ai simboli API
    api_symbol = "BTC" if symbol.upper() in ["BITCOIN", "BTC"] else "XAUT"

    try:
        log(f"Richiesta dati per {symbol} (API: {api_symbol})...")
        url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={api_symbol}USDT"
        log(f"URL: {url}")

        log("Esecuzione GET request...")
        r = requests.get(url, headers={"User-Agent":"CircuitPython"})

        log("Parsing JSON response...")
        res = r.json()

        log("Chiusura connessione...")
        r.close()  # Chiudi subito la connessione

        # Estrai i dati
        log("Estrazione dati...")
        result = res["result"]["list"][0]
        data = {
            "price": float(result["lastPrice"]),
            "high": float(result["highPrice24h"]),
            "low": float(result["lowPrice24h"])
        }
        log(f"Dati ottenuti: {data}")

        # Forza la garbage collection dopo operazioni di rete
        log("Pulizia memoria...")
        del res
        gc.collect()
        log(f"Memoria libera: {gc.mem_free()} bytes")
        return data
    except Exception as e:
        log(f"Errore API: {e}")
        log(f"Memoria libera: {gc.mem_free()} bytes")
        gc.collect()
        return None

# --- FUNZIONI WEB SERVER ---
def web_page():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>LED Matrix Control</title>
        <style>
            body {{ font-family: Arial; text-align: center; margin: 20px; }}
            .control {{ margin: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }}
            input, select {{ margin: 10px; padding: 5px; }}
            button {{ background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>LED Matrix Control</h1>

        <div class="control">
            <h2>Symbols</h2>
            <form action="/update" method="post">
                <div>
                    <label>Symbol 1:</label>
                    <input type="text" name="symbol1" value="{config['symbols'][0]}">
                </div>
                <div>
                    <label>Symbol 2:</label>
                    <input type="text" name="symbol2" value="{config['symbols'][1]}">
                </div>
                <button type="submit">Update Symbols</button>
            </form>
        </div>

        <div class="control">
            <h2>Display Settings</h2>
            <form action="/settings" method="post">
                <div>
                    <label>Brightness (0.1-1.0):</label>
                    <input type="range" min="0.1" max="1.0" step="0.1" name="brightness" value="{config['brightness']}">
                    <span>{config['brightness']}</span>
                </div>
                <div>
                    <label>Scroll Speed (1-5):</label>
                    <input type="range" min="1" max="5" name="scroll_speed" value="{config['scroll_speed']}">
                    <span>{config['scroll_speed']}</span>
                </div>
                <div>
                    <label>Scroll Delay (0.01-0.1):</label>
                    <input type="range" min="0.01" max="0.1" step="0.01" name="scroll_delay" value="{config['scroll_delay']}">
                    <span>{config['scroll_delay']}</span>
                </div>
                <button type="submit">Update Settings</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

# --- FUNZIONI PER SCROLL SEGMENTS ---
def generate_scroll_segments():
    """Genera i segmenti di scrolling in base ai simboli configurati"""
    global scroll_segments

    scroll_segments = []
    for symbol in config["symbols"]:
        if symbol in crypto_data:
            data = crypto_data[symbol]

            # Segmento 1: Nome simbolo
            scroll_segments.append({
                "text": symbol,
                "color": data["color"],
                "length": len(symbol)
            })

            # Spazio dopo il simbolo
            scroll_segments.append({
                "text": " ",
                "color": WHITE,
                "length": 1
            })

            # Segmento 2: Prezzo attuale
            price_text = f"{int(data['price'])}"
            scroll_segments.append({
                "text": price_text,
                "color": data["trend_color"],
                "length": len(price_text)
            })

            # Spazio dopo il prezzo
            scroll_segments.append({
                "text": " ",
                "color": WHITE,
                "length": 1
            })

            # Segmento 3: High
            high_text = f"H:{int(data['high'])}"
            scroll_segments.append({
                "text": high_text,
                "color": CYAN,
                "length": len(high_text)
            })

            # Spazio dopo High
            scroll_segments.append({
                "text": " ",
                "color": WHITE,
                "length": 1
            })

            # Segmento 4: Low
            low_text = f"L:{int(data['low'])}"
            scroll_segments.append({
                "text": low_text,
                "color": PURPLE,
                "length": len(low_text)
            })

            # Aggiungi uno spazio extra tra i set di dati
            scroll_segments.append({
                "text": "   ",
                "color": WHITE,
                "length": 3
            })

def update_crypto_data():
    """Aggiorna i dati delle criptovalute"""
    global crypto_data

    for symbol in config["symbols"]:
        # Assegna un colore predefinito in base al simbolo
        if symbol.upper() in ["BITCOIN", "BTC"]:
            color = ORANGE
        elif symbol.upper() in ["GOLD", "XAUT"]:
            color = GOLD
        else:
            color = WHITE

        # Inizializza il simbolo se non esiste
        if symbol not in crypto_data:
            crypto_data[symbol] = {
                "price": 0,
                "high": 0,
                "low": 0,
                "prev_price": None,
                "color": color,
                "trend_color": WHITE
            }

        # Aggiorna il colore in caso sia cambiato il simbolo
        crypto_data[symbol]["color"] = color

        # Ottieni i dati aggiornati
        data = get_crypto_data(requests, symbol)
        if data:
            crypto_data[symbol]["prev_price"] = crypto_data[symbol]["price"]
            crypto_data[symbol]["price"] = data["price"]
            crypto_data[symbol]["high"] = data["high"]
            crypto_data[symbol]["low"] = data["low"]

            # Aggiorna il colore della tendenza
            if crypto_data[symbol]["prev_price"] is None:
                crypto_data[symbol]["trend_color"] = WHITE
            elif data["price"] > crypto_data[symbol]["prev_price"]:
                crypto_data[symbol]["trend_color"] = GREEN
            else:
                crypto_data[symbol]["trend_color"] = RED

    # Rigenera i segmenti di scrolling
    generate_scroll_segments()

# --- MAIN LOOP ---
# Inizializzazione
log("=== AVVIO PROGRAMMA ===")
log(f"Memoria libera: {gc.mem_free()} bytes")

log("Pulizia display iniziale...")
clear_display()

log("Avvio connessione WiFi...")
requests, pool = connect_wifi()
if not requests:
    log("Prima connessione fallita, riprovo...")
    time.sleep(5)
    requests, pool = connect_wifi()  # Riprova una volta

# Inizializza il server web se la connessione è riuscita
server = None
if requests and pool:
    # Mostra l'IP per 3 secondi
    show_ip()

    # Avvia il server web
    try:
        server = Server(pool)

        # Definisci le route
        @server.route("/")
        def base(request):
            # Versione corretta della Response
            return Response(content_type="text/html", body=web_page())

        @server.route("/update", methods=["POST"])
        def update_symbols(request):
            global crypto_data, scroll_segments

            # Estrai i nuovi simboli dal form
            form_data = request.form_data
            symbol1 = form_data.get("symbol1", "Bitcoin")
            symbol2 = form_data.get("symbol2", "Gold")

            # Aggiorna la configurazione
            config["symbols"] = [symbol1, symbol2]

            # Aggiorna i dati e rigenera i segmenti di scrolling
            update_crypto_data()

            # Versione corretta della Response
            return Response(content_type="text/html", body=web_page())

        @server.route("/settings", methods=["POST"])
        def update_settings(request):
            # Estrai le nuove impostazioni dal form
            form_data = request.form_data
            brightness = float(form_data.get("brightness", 0.3))
            scroll_speed = int(form_data.get("scroll_speed", 1))
            scroll_delay = float(form_data.get("scroll_delay", 0.03))

            # Aggiorna la configurazione
            config["brightness"] = brightness
            config["scroll_speed"] = scroll_speed
            config["scroll_delay"] = scroll_delay

            # Applica le nuove impostazioni
            pixels.brightness = brightness

            # Versione corretta della Response
            return Response(content_type="text/html", body=web_page())

        # Avvia il server
        server.start(port=80)
        log(f"Server web avviato su http://{wifi.radio.ipv4_address}")
    except Exception as e:
        log(f"Errore avvio server web: {e}")
        server = None

# Inizializza i dati per entrambi i simboli all'inizio
crypto_data = {}
for symbol in config["symbols"]:
    data = get_crypto_data(requests, symbol)

    # Assegna un colore predefinito in base al simbolo
    if symbol.upper() in ["BITCOIN", "BTC"]:
        color = ORANGE
    elif symbol.upper() in ["GOLD", "XAUT"]:
        color = GOLD
    else:
        color = WHITE

    crypto_data[symbol] = {
        "price": data["price"] if data else 0,
        "high": data["high"] if data else 0,
        "low": data["low"] if data else 0,
        "prev_price": None,
        "color": color,
        "trend_color": WHITE
    }

# Configura lo scrolling continuo
scroll_position = MATRIX_WIDTH  # Inizia fuori dallo schermo a destra
scroll_segments = []

# Genera i segmenti di scrolling iniziali
generate_scroll_segments()

log("Inizio loop principale con scrolling continuo...")
# Loop principale con scrolling continuo
while True:
    try:
        # Gestisci le richieste web se il server è attivo
        if server:
            server.poll()

        # Verifica connessione WiFi
        if not wifi.radio.connected:
            log("WiFi disconnesso, riconnessione...")
            requests, pool = connect_wifi()
            if not requests:
                log("Riconnessione fallita")
                for i in range(MATRIX_WIDTH):
                    set_pixel(i, 0, RED)
                pixels.show()
                time.sleep(5)
                clear_display()
                continue

        # Calcola la lunghezza totale del testo di scrolling
        total_scroll_length = 0
        for segment in scroll_segments:
            total_scroll_length += segment["length"] * 5

        # Scrolling continuo
        clear_display()

        # Disegna tutti i segmenti nel testo di scrolling
        current_pos = scroll_position
        for segment in scroll_segments:
            draw_text(segment["text"], current_pos, segment["color"])
            current_pos += segment["length"] * 5

        # Mostra il frame
        pixels.show()

        # Aggiorna la posizione di scrolling
        scroll_position -= config["scroll_speed"]

        # Se il testo è completamente uscito a sinistra, ricomincia da destra
        if scroll_position < -total_scroll_length:
            scroll_position = MATRIX_WIDTH

            # Aggiorna i dati ad ogni ciclo completo
            log("Aggiornamento dati...")
            update_crypto_data()
            log("Dati aggiornati, continua scrolling...")

        # Breve pausa tra i frame
        time.sleep(config["scroll_delay"])

        # Garbage collection regolare
        gc.collect()

    except Exception as e:
        log(f"Eccezione nel loop principale: {e}")
        for i in range(MATRIX_WIDTH):
            set_pixel(i, 0, RED)
        pixels.show()
        gc.collect()
        time.sleep(5)
        clear_display()

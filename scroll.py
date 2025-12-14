# main_minimal.py - Versione con scrolling continuo e prezzi H/L con spaziatura
import board
import neopixel
import time
import wifi
import adafruit_requests
import gc
import adafruit_connection_manager
import microcontroller

# --- CONFIGURAZIONE ---
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
NUM_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN = board.D38
BRIGHTNESS = 0.008

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

# --- INIZIALIZZAZIONE HARDWARE ---
print("[INIT] Inizializzazione NeoPixel...")
pixels = neopixel.NeoPixel(
    DATA_PIN, NUM_LEDS,
    brightness=BRIGHTNESS,
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
}

def test_bybit():
    """Mostra BYBIT per verificare che il layout funzioni"""
    log("Mostrando BYBIT...")

    text = "BYBIT"
    text = text.upper()

    clear_display()

    # Disegna il testo centrato (senza scrolling)
    x_start = (MATRIX_WIDTH - (len(text) * 5)) // 2

    # Per ogni carattere
    for i, char in enumerate(text):
        if char in CHARS:
            char_pattern = CHARS[char]
            x_pos = x_start + i * 5

            # Per ogni riga e colonna del carattere
            for y in range(8):
                for x in range(4):
                    if char_pattern[y][x]:
                        set_pixel(x_pos + x, y, WHITE)

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
        return requests
    except Exception as e:
        log(f"Errore connessione WiFi: {e}")
        # Visualizza errore
        for i in range(MATRIX_WIDTH):
            set_pixel(i, 0, RED)
        pixels.show()
        time.sleep(1)
        clear_display()
        return None

def get_crypto_data(requests, symbol):
    if requests is None:
        log("Impossibile ottenere dati: requests è None")
        return None

    # Mappa i nomi visualizzati ai simboli API
    api_symbol = "BTC" if symbol == "Bitcoin" else "XAUT"

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

# --- MAIN LOOP ---
# Inizializzazione
log("=== AVVIO PROGRAMMA ===")
log(f"Memoria libera: {gc.mem_free()} bytes")

log("Pulizia display iniziale...")
clear_display()

# Test Bybit
test_bybit()

log("Avvio connessione WiFi...")
requests = connect_wifi()
if not requests:
    log("Prima connessione fallita, riprovo...")
    time.sleep(5)
    requests = connect_wifi()  # Riprova una volta

# Inizializza i dati per entrambi i simboli all'inizio
bitcoin_data = get_crypto_data(requests, "Bitcoin")
gold_data = get_crypto_data(requests, "Gold")

# Struttura dati per tenere traccia di tutti i dati necessari
crypto_data = {
    "Bitcoin": {
        "price": bitcoin_data["price"] if bitcoin_data else 0,
        "high": bitcoin_data["high"] if bitcoin_data else 0,
        "low": bitcoin_data["low"] if bitcoin_data else 0,
        "prev_price": None,
        "color": ORANGE,
        "trend_color": WHITE
    },
    "Gold": {
        "price": gold_data["price"] if gold_data else 0,
        "high": gold_data["high"] if gold_data else 0,
        "low": gold_data["low"] if gold_data else 0,
        "prev_price": None,
        "color": GOLD,
        "trend_color": WHITE
    }
}

# Configura lo scrolling continuo
scroll_position = MATRIX_WIDTH  # Inizia fuori dallo schermo a destra
scroll_speed = 1  # Pixel per frame
scroll_delay = 0.03  # Secondi tra i frame
spacer = 10  # Spazio tra i set di dati

# Prepara il testo iniziale da scrollare
scroll_segments = []
for symbol in ["Bitcoin", "Gold"]:
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

log("Inizio loop principale con scrolling continuo...")
# Loop principale con scrolling continuo
while True:
    try:
        # Verifica connessione WiFi
        if not wifi.radio.connected:
            log("WiFi disconnesso, riconnessione...")
            requests = connect_wifi()
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
        scroll_position -= scroll_speed

        # Se il testo è completamente uscito a sinistra, ricomincia da destra
        if scroll_position < -total_scroll_length:
            scroll_position = MATRIX_WIDTH

            # Aggiorna i dati ad ogni ciclo completo
            log("Aggiornamento dati...")

            # Aggiorna i prezzi
            for symbol in ["Bitcoin", "Gold"]:
                data = crypto_data[symbol]
                data["prev_price"] = data["price"]
                new_data = get_crypto_data(requests, symbol)

                if new_data:
                    data["price"] = new_data["price"]
                    data["high"] = new_data["high"]
                    data["low"] = new_data["low"]

                    # Aggiorna il colore della tendenza
                    if data["prev_price"] is None:
                        data["trend_color"] = WHITE
                    elif new_data["price"] > data["prev_price"]:
                        data["trend_color"] = GREEN
                    else:
                        data["trend_color"] = RED

            # Aggiorna il testo di scrolling
            scroll_segments = []
            for symbol in ["Bitcoin", "Gold"]:
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

            log("Dati aggiornati, continua scrolling...")

        # Breve pausa tra i frame
        time.sleep(scroll_delay)

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

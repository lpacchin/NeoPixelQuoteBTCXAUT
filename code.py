import board
import neopixel
import time
import wifi
import adafruit_requests
import gc
import adafruit_connection_manager

# --- CONFIGURAZIONE ---
MATRIX_WIDTH = 32
MATRIX_HEIGHT = 8
NUM_LEDS = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN = board.IO38
BRIGHTNESS = 0.1

# Configurazione layout matrice
SERPENTINE = True      # True se il layout è a serpentina
VERTICAL = True        # True se le strip corrono verticalmente
REVERSE_ROWS = False   # True se le righe dispari vanno da destra a sinistra

# Colori
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0)    # BTC$
GOLD = (255, 200, 0)      # XAUT$
RED = (255, 0, 0)         # Negativo
GREEN = (0, 255, 0)       # Positivo
BLUE = (0, 0, 255)        # Connessione
WHITE = (255, 255, 255)   # Test
CYAN = (0, 255, 255)      # High
PURPLE = (255, 0, 255)    # Low

# --- INIZIALIZZAZIONE HARDWARE ---
print("[INIT] Inizializzazione NeoPixel...")
pixels = neopixel.NeoPixel(
    DATA_PIN, NUM_LEDS,
    brightness=BRIGHTNESS,
    auto_write=False
)

# --- INIZIALIZZAZIONE RETE ---
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# --- FUNZIONI DI UTILITÀ ---
def log(message):
    """Log con timestamp"""
    print(f"[{time.monotonic():.1f}s] {message}")

def clear_display():
    """Pulisce il display"""
    pixels.fill(BLACK)
    pixels.show()

def xy_to_index(x, y):
    """Converte coordinate x,y in indice pixel"""
    if x < 0 or x >= MATRIX_WIDTH or y < 0 or y >= MATRIX_HEIGHT:
        return -1

    if VERTICAL:
        if SERPENTINE and ((x % 2 == 1) ^ REVERSE_ROWS):
            index = x * MATRIX_HEIGHT + (MATRIX_HEIGHT - 1 - y)
        else:
            index = x * MATRIX_HEIGHT + y
    else:
        if SERPENTINE and ((y % 2 == 1) ^ REVERSE_ROWS):
            index = y * MATRIX_WIDTH + (MATRIX_WIDTH - 1 - x)
        else:
            index = y * MATRIX_WIDTH + x
    return index

def set_pixel(x, y, color):
    """Imposta un pixel alle coordinate x,y"""
    index = xy_to_index(x, y)
    if 0 <= index < NUM_LEDS:
        pixels[index] = color

def startup_animation():
    """Animazione di startup"""
    log("Esecuzione animazione di startup...")
    colors = [ORANGE, GOLD, RED, GREEN, BLUE, CYAN, PURPLE, WHITE]

    # Effetto 1: Riempimento per colonna
    for x in range(MATRIX_WIDTH):
        for y in range(MATRIX_HEIGHT):
            set_pixel(x, y, colors[x % len(colors)])
        pixels.show()
        time.sleep(0.05)
    time.sleep(0.2)
    clear_display()

    # Effetto 2: Lampeggio alternato
    for _ in range(3):
        for x in range(MATRIX_WIDTH):
            for y in range(MATRIX_HEIGHT):
                set_pixel(x, y, colors[_ % len(colors)] if (x + y) % 2 == 0 else colors[(_ + 1) % len(colors)])
        pixels.show()
        time.sleep(0.3)
        clear_display()
        time.sleep(0.1)

    # Effetto 3: Dissolvenza colori
    for color in colors:
        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                set_pixel(x, y, color)
        pixels.show()
        time.sleep(0.1)
    time.sleep(0.2)

    # Spegnimento graduale
    for x in range(MATRIX_WIDTH - 1, -1, -1):
        for y in range(MATRIX_HEIGHT):
            set_pixel(x, y, BLACK)
        pixels.show()
        time.sleep(0.03)
    log("Animazione completata")

# Definizione caratteri 5x8
CHARS = {
    ' ': [[0]*5 for _ in range(8)],
    '-': [[0]*5 for _ in range(3)] + [[1]*5] + [[0]*5 for _ in range(4)],
    '.': [[0]*5 for _ in range(5)] + [[0,0,1,0,0], [0,0,1,0,0]] + [[0]*5],
    '0': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,1,1], [1,0,1,0,1], [1,1,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [0]*5],
    '1': [[0,0,1,0,0], [0,1,1,0,0], [1,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0], [0]*5],
    '2': [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,0,1], [0,0,0,1,0], [0,1,0,0,0], [1,0,0,0,0], [1,1,1,1,1], [0]*5],
    '3': [[1,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [0,0,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,0], [0]*5],
    '4': [[0,0,0,1,0], [0,0,1,1,0], [0,1,0,1,0], [1,0,0,1,0], [1,1,1,1,1], [0,0,0,1,0], [0,0,0,1,0], [0]*5],
    '5': [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,0], [0]*5],
    '6': [[0,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [0]*5],
    '7': [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,1,0], [0,0,0,1,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0]*5],
    '8': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [0]*5],
    '9': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,0,0,0,1], [0,1,1,1,0], [0]*5],
    'A': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0]*5],
    'B': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [0]*5],
    '₿': [[0,1,0,1,0], [1,1,1,1,0], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [0,1,0,1,0]],
    'C': [[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [0,1,1,1,1], [0]*5],
    'D': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [0]*5],
    'E': [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,1], [0]*5],
    'F': [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [0]*5],
    'G': [[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0]*5],
    'H': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0]*5],
    'I': [[0,1,1,1,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0], [0]*5],
    'J': [[0,0,1,1,1], [0,0,0,1,0], [0,0,0,1,0], [0,0,0,1,0], [1,0,0,1,0], [1,0,0,1,0], [0,1,1,0,0], [0]*5],
    'K': [[1,0,0,0,1], [1,0,0,1,0], [1,0,1,0,0], [1,1,0,0,0], [1,0,1,0,0], [1,0,0,1,0], [1,0,0,0,1], [0]*5],
    'L': [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,1], [0]*5],
    'M': [[1,0,0,0,1], [1,1,0,1,1], [1,0,1,0,1], [1,0,1,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0]*5],
    'N': [[1,0,0,0,1], [1,1,0,0,1], [1,0,1,0,1], [1,0,0,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0]*5],
    'O': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [0]*5],
    'P': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [0]*5],
    'Q': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,1,0,1], [1,0,0,1,0], [0,1,1,0,1], [0]*5],
    'R': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [1,0,1,0,0], [1,0,0,1,0], [1,0,0,0,1], [0]*5],
    'S': [[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [0,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,0], [0]*5],
    'T': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0]*5],
    'U': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [0]*5],
    'V': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0]*5],
    'W': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,1,0,1], [1,0,1,0,1], [1,1,0,1,1], [1,0,0,0,1], [0]*5],
    'X': [[1,0,0,0,1], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1], [1,0,0,0,1], [0]*5],
    'Y': [[1,0,0,0,1], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0]*5],
    'Z': [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0], [1,1,1,1,1], [0]*5],
    '$': [[0,0,1,0,0], [0,1,1,1,1], [1,0,1,0,0], [0,1,1,1,0], [0,0,1,0,1], [1,1,1,1,0], [0,0,1,0,0], [0]*5],
}

def test_bybit():
    """Mostra BYBIT per verificare il layout"""
    log("Mostrando BYBIT...")
    text = "BYBIT".upper()
    pixels.fill(BLACK)
    x_start = (MATRIX_WIDTH - (len(text) * 6)) // 2
    for i, char in enumerate(text):
        if char in CHARS:
            char_pattern = CHARS[char]
            x_pos = x_start + i * 6
            for y in range(8):
                for x in range(5):
                    if char_pattern[y][x]:
                        set_pixel(x_pos + x, y, WHITE)
    pixels.show()
    time.sleep(3)
    pixels.fill(BLACK)
    pixels.show()

def draw_text(text, x_offset, color=WHITE):
    """Disegna testo alla posizione x_offset"""
    text = text.upper()
    x_offset = int(x_offset)  # Converti in intero per evitare errori float
    for i, char in enumerate(text):
        if char in CHARS:
            char_pattern = CHARS[char]
            x_pos = x_offset + i * 6
            for y in range(8):
                for x in range(5):
                    if char_pattern[y][x] and 0 <= x_pos + x < MATRIX_WIDTH:
                        set_pixel(x_pos + x, y, color)

def get_crypto_data(requests, symbol):
    """Recupera dati cripto da Bybit"""
    if requests is None:
        log("Impossibile ottenere dati: requests è None")
        return None
    api_symbol = "BTC" if symbol == "BTC$" else "XAUT"
    try:
        log(f"Richiesta dati per {symbol} (API: {api_symbol})...")
        url = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={api_symbol}USDT"
        r = requests.get(url, headers={"User-Agent": "CircuitPython"})
        res = r.json()
        r.close()
        result = res["result"]["list"][0]
        data = {
            "price": float(result["lastPrice"]),
            "high": float(result["highPrice24h"]),
            "low": float(result["lowPrice24h"])
        }
        log(f"Dati ottenuti: {data}")
        del res
        gc.collect()
        log(f"Memoria libera: {gc.mem_free()} bytes")
        return data
    except Exception as e:
        log(f"Errore API: {e}")
        gc.collect()
        return None

# --- MAIN LOOP ---
log("=== AVVIO PROGRAMMA ===")
log(f"Memoria libera: {gc.mem_free()} bytes")
pixels.fill(BLACK)
pixels.show()

startup_animation()
test_bybit()

btc_data = get_crypto_data(requests, "BTC$")
xaut_data = get_crypto_data(requests, "XAUT$")

crypto_data = {
    "BTC$": {
        "price": btc_data["price"] if btc_data else 0,
        "high": btc_data["high"] if btc_data else 0,
        "low": btc_data["low"] if btc_data else 0,
        "prev_price": None,
        "color": ORANGE,
        "trend_color": WHITE
    },
    "XAUT$": {
        "price": xaut_data["price"] if xaut_data else 0,
        "high": xaut_data["high"] if xaut_data else 0,
        "low": xaut_data["low"] if xaut_data else 0,
        "prev_price": None,
        "color": GOLD,
        "trend_color": WHITE
    }
}

scroll_position = MATRIX_WIDTH
scroll_speed = 1  # Intero per evitare errori float
scroll_delay = 0.05
last_data_update = time.monotonic()
update_interval = 60

scroll_segments = []
for symbol in ["BTC$", "XAUT$"]:
    data = crypto_data[symbol]
    scroll_segments.extend([
        {"text": symbol, "color": data["color"], "length": len(symbol)},
        {"text": " ", "color": WHITE, "length": 1},
        {"text": f"{int(data['price'])}", "color": data["trend_color"], "length": len(f"{int(data['price'])}")},
        {"text": " ", "color": WHITE, "length": 1},
        {"text": f"H:{int(data['high'])}", "color": CYAN, "length": len(f"H:{int(data['high'])}")},
        {"text": " ", "color": WHITE, "length": 1},
        {"text": f"L:{int(data['low'])}", "color": PURPLE, "length": len(f"L:{int(data['low'])}")},
        {"text": "   ", "color": WHITE, "length": 3}
    ])

log("Inizio loop principale...")
while True:
    try:
        if not wifi.radio.connected:
            log("WiFi disconnesso, attendendo riconnessione...")
            pixels.fill(BLACK)
            for i in range(MATRIX_WIDTH):
                set_pixel(i, 0, RED)
            pixels.show()
            time.sleep(5)
            pixels.fill(BLACK)
            pixels.show()
            continue

        total_scroll_length = sum(segment["length"] * 6 for segment in scroll_segments)
        pixels.fill(BLACK)
        current_pos = scroll_position
        for segment in scroll_segments:
            draw_text(segment["text"], current_pos, segment["color"])
            current_pos += segment["length"] * 6
        pixels.show()

        scroll_position -= scroll_speed
        if scroll_position < -total_scroll_length:
            scroll_position = MATRIX_WIDTH
            if time.monotonic() - last_data_update > update_interval:
                log("Aggiornamento dati...")
                for symbol in ["BTC$", "XAUT$"]:
                    data = crypto_data[symbol]
                    data["prev_price"] = data["price"]
                    new_data = get_crypto_data(requests, symbol)
                    if new_data:
                        data["price"] = new_data["price"]
                        data["high"] = new_data["high"]
                        data["low"] = new_data["low"]
                        data["trend_color"] = WHITE if data["prev_price"] is None else GREEN if new_data["price"] > data["prev_price"] else RED
                scroll_segments = []
                for symbol in ["BTC$", "XAUT$"]:
                    data = crypto_data[symbol]
                    scroll_segments.extend([
                        {"text": symbol, "color": data["color"], "length": len(symbol)},
                        {"text": " ", "color": WHITE, "length": 1},
                        {"text": f"{int(data['price'])}", "color": data["trend_color"], "length": len(f"{int(data['price'])}")},
                        {"text": " ", "color": WHITE, "length": 1},
                        {"text": f"H:{int(data['high'])}", "color": CYAN, "length": len(f"H:{int(data['high'])}")},
                        {"text": " ", "color": WHITE, "length": 1},
                        {"text": f"L:{int(data['low'])}", "color": PURPLE, "length": len(f"L:{int(data['low'])}")},
                        {"text": "   ", "color": WHITE, "length": 3}
                    ])
                last_data_update = time.monotonic()
                gc.collect()
                log(f"Dati aggiornati, memoria libera: {gc.mem_free()} bytes")

        time.sleep(scroll_delay)

    except Exception as e:
        log(f"Eccezione: {e}")
        pixels.fill(RED)
        pixels.show()
        gc.collect()
        time.sleep(5)
        pixels.fill(BLACK)
        pixels.show()


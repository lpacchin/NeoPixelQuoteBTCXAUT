# main_minimal.py - Versione refactor con LABEL e controllo API
import board
import neopixel
import time
import wifi
import adafruit_requests
import gc
import adafruit_connection_manager

# --- LETTURA CONFIGURAZIONE ---
def read_config_file(filename="scroll.conf"):
    """Legge un file di configurazione personalizzato da SD"""
    config = {
        "SYMBOL1": "BTCUSDT",
        "LABEL1":  "Bitcoin",
        "SYMBOL2": "XAUUSDT",
        "LABEL2":  "Gold",
        "BRIGHTNESS": 0.008,
        "SCROLL_SPEED": 1,
        "SCROLL_DELAY": 0.03
    }
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = [x.strip() for x in line.split("=",1)]
                    if val.startswith('"') and val.endswith('"'):
                        config[key] = val[1:-1]
                    elif "." in val:
                        try:
                            config[key] = float(val)
                        except ValueError:
                            print(f"Errore parsing float {val} per {key}")
                    else:
                        try:
                            config[key] = int(val)
                        except ValueError:
                            print(f"Errore parsing int {val} per {key}")
        print(f"Configurazione caricata da {filename}")
    except OSError as e:
        print(f"Non posso leggere {filename}: {e}, uso valori di default")
    return config

# Carica configurazione
conf = read_config_file()
SYMBOL1      = conf["SYMBOL1"]
LABEL1       = conf["LABEL1"]
SYMBOL2      = conf["SYMBOL2"]
LABEL2       = conf["LABEL2"]
BRIGHTNESS   = conf["BRIGHTNESS"]
SCROLL_SPEED = conf["SCROLL_SPEED"]
SCROLL_DELAY = conf["SCROLL_DELAY"]

print(f"Config: {LABEL1}({SYMBOL1}), {LABEL2}({SYMBOL2}), brightness={BRIGHTNESS}, speed={SCROLL_SPEED}, delay={SCROLL_DELAY}")

# --- CREDENZIALI WIFI ---
WIFI_SSID     = "lupa"
WIFI_PASSWORD = "780130bmw."

# --- HARDWARE LED MATRIX ---
MATRIX_WIDTH   = 32
MATRIX_HEIGHT  = 8
NUM_LEDS       = MATRIX_WIDTH * MATRIX_HEIGHT
DATA_PIN       = board.D38
SERPENTINE     = True
VERTICAL       = True
REVERSE_ROWS   = False

# --- COLORI ---
BLACK   = (0,  0,  0)
ORANGE  = (255,100, 0)
GOLD    = (255,200, 0)
RED     = (255,  0,  0)
GREEN   = (0,  255,  0)
BLUE    = (0,    0,255)
WHITE   = (255,255,255)
CYAN    = (0,  255,255)
PURPLE  = (255,  0,255)

# Inizializza NeoPixel
print("[INIT] NeoPixel...")
pixels = neopixel.NeoPixel(DATA_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# --- FUNZIONI DI UTILITÀ DISPLAY ---
def log(msg):
    print(f"[{time.monotonic():.1f}s] {msg}")

def clear_display():
    #log("clear display")
    pixels.fill(BLACK)
    pixels.show()

def xy_to_index(x, y):
    if x<0 or x>=MATRIX_WIDTH or y<0 or y>=MATRIX_HEIGHT:
        return -1
    if VERTICAL:
        if SERPENTINE and ((x%2)==1) ^ REVERSE_ROWS:
            return x*MATRIX_HEIGHT + (MATRIX_HEIGHT-1-y)
        return x*MATRIX_HEIGHT + y
    else:
        if SERPENTINE and ((y%2)==1) ^ REVERSE_ROWS:
            return y*MATRIX_WIDTH + (MATRIX_WIDTH-1-x)
        return y*MATRIX_WIDTH + x

def set_pixel(x, y, color):
    idx = xy_to_index(x, y)
    if 0 <= idx < NUM_LEDS:
        pixels[idx] = color

# --- FONT 4x8 (omesso per brevità, aggiungi definizioni 0-9, A-Z, ':', spazio) ---
CHARS = {
    # ... completa secondo tuo font ...
}

def draw_text(text, x_offset, color=WHITE):
    text = text.upper()
    for i, ch in enumerate(text):
        if ch not in CHARS:
            continue
        sprite = CHARS[ch]
        for y in range(8):
            for x in range(4):
                if sprite[y][x]:
                    xx = x_offset + i*5 + x
                    if 0 <= xx < MATRIX_WIDTH:
                        set_pixel(xx, y, color)

# --- FUNZIONI RETE ---
def connect_wifi():
    log("Connecting WiFi...")
    try:
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
        log(f"Connected, IP={wifi.radio.ipv4_address}")
        pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        ssl  = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
        sess = adafruit_requests.Session(pool, ssl)
        pixels.fill(BLUE); pixels.show(); time.sleep(1); clear_display()
        gc.collect()
        log(f"Free mem: {gc.mem_free()}")
        return sess
    except Exception as e:
        log(f"WiFi error: {e}")
        pixels.fill(RED); pixels.show(); time.sleep(1); clear_display()
        return None

def get_crypto_data(sess, symbol):
    if sess is None:
        log("No session")
        return None
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}"
    try:
        r = sess.get(url, headers={"User-Agent":"CircuitPython"})
        res = r.json()
        r.close()
        # Controlla ret_code
        if res.get("ret_code", 0) != 0:
            log(f"API error: {res.get('ret_msg')}")
            return None
        tickers = res.get("result", {}).get("list")
        if not tickers:
            log("API error: no data returned")
            return None
        info = tickers[0]
        data = {
            "price": float(info["lastPrice"]),
            "high":  float(info["highPrice24h"]),
            "low":   float(info["lowPrice24h"])
        }
        gc.collect()
        return data
    except Exception as e:
        log(f"API exception: {e}")
        gc.collect()
        return None

# --- MAIN LOOP ---
log("=== START ===")
clear_display()

sess = connect_wifi()
data1 = get_crypto_data(sess, SYMBOL1)
data2 = get_crypto_data(sess, SYMBOL2)

# Inizializza struttura dati con LABEL come chiave
crypto = {
    LABEL1: {"symbol":SYMBOL1, "price":data1["price"] if data1 else 0,
             "high":data1["high"]     if data1 else 0,
             "low":data1["low"]       if data1 else 0,
             "prev":None, "col":ORANGE, "trend":WHITE},
    LABEL2: {"symbol":SYMBOL2, "price":data2["price"] if data2 else 0,
             "high":data2["high"]     if data2 else 0,
             "low":data2["low"]       if data2 else 0,
             "prev":None, "col":GOLD,   "trend":WHITE}
}

scroll_x = MATRIX_WIDTH

def build_segments():
    segs = []
    for lbl in [LABEL1, LABEL2]:
        d = crypto[lbl]
        segs.append({"text":lbl,                    "col":d["col"],   "len":len(lbl)})
        segs.append({"text":" ",                    "col":WHITE,      "len":1})
        price_str = str(int(d["price"]))
        segs.append({"text":price_str,              "col":d["trend"], "len":len(price_str)})
        segs.append({"text":" ",                    "col":WHITE,      "len":1})
        high_str = f"H:{int(d['high'])}"
        segs.append({"text":high_str,               "col":CYAN,       "len":len(high_str)})
        segs.append({"text":" ",                    "col":WHITE,      "len":1})
        low_str  = f"L:{int(d['low'])}"
        segs.append({"text":low_str,                "col":PURPLE,     "len":len(low_str)})
        segs.append({"text":"   ",                  "col":WHITE,      "len":3})
    return segs

segments = build_segments()

while True:
    try:
        if wifi.radio.ipv4_address is None:
            sess = connect_wifi()
        clear_display()
        xpos = scroll_x
        for seg in segments:
            draw_text(seg["text"], xpos, seg["col"])
            xpos += seg["len"] * 5
        pixels.show()

        scroll_x -= SCROLL_SPEED
        total_px = sum(seg["len"]*5 for seg in segments)
        if scroll_x < -total_px:
            scroll_x = MATRIX_WIDTH
            log("Updating data...")
            for lbl in [LABEL1, LABEL2]:
                entry = crypto[lbl]
                entry["prev"] = entry["price"]
                new = get_crypto_data(sess, entry["symbol"])
                if new:
                    entry["price"] = new["price"]
                    entry["high"]  = new["high"]
                    entry["low"]   = new["low"]
                    if entry["prev"] is None:
                        entry["trend"] = WHITE
                    elif entry["price"] > entry["prev"]:
                        entry["trend"] = GREEN
                    else:
                        entry["trend"] = RED
            segments = build_segments()

        time.sleep(SCROLL_DELAY)
        gc.collect()

    except Exception as e:
        log(f"Loop error: {e}")
        pixels.fill(RED); pixels.show(); time.sleep(1); clear_display(); gc.collect()

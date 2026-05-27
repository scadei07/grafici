import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ── 1. CONFIGURAZIONE E PARAMETRI ─────────────────────────────────────
SOGLIA_BUIO = 400     # Sotto questo valore di luce, il sistema considera che sia "buio"
TIMEOUT_LED = 5       # Per quanti secondi il lampione resta acceso dopo un movimento

# Liste per memorizzare la cronologia dei dati (i punti da disegnare)
lista_luce = []
lista_movimento = []
lista_lampione = []

# Variabili di stato del lampione
valore_luce = 800     # Partiamo da una situazione di "pieno giorno"
timer_lampione = 0    # Conta quanti secondi mancano allo spegnimento

# ── 2. LOGICA DI CONTROLLO (Come un Arduino) ──────────────────────────
def calcola_nuovi_dati():
    global valore_luce, timer_lampione
    
    # Simula la luce: cambia in modo graduale (scende verso la notte, poi risale)
    valore_luce += random.choice([-30, -10, 10, 30])
    valore_luce = max(0, min(1023, valore_luce)) # Forza il valore tra 0 e 1023
    
    # Simula il movimento: c'è il 20% di probabilità che passi qualcuno
    movimento = 1 if random.random() < 0.20 else 0
    
    # Logica di accensione
    buio = valore_luce < SOGLIA_BUIO
    
    if buio and movimento:
        timer_lampione = TIMEOUT_LED  # Rilevato movimento al buio: avvia/resetta il timer
        
    if timer_lampione > 0:
        lampione_acceso = 1
        timer_lampione -= 1          # Il tempo scorre...
    else:
        lampione_acceso = 0
        
    return valore_luce, movimento, lampione_acceso

# ── 3. CREAZIONE DELLA FINESTRA GRAFICA ───────────────────────────────
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
fig.canvas.manager.set_window_title("Dashboard Lampione Smart")

# ── 4. FUNZIONE DI AGGIORNAMENTO (Eseguita ad ogni frame) ──────────────
def aggiorna(frame):
    # Calcola i nuovi dati e aggiungili alle liste
    v_luce, v_mov, v_led = calcola_nuovi_dati()
    lista_luce.append(v_luce)
    lista_movimento.append(v_mov)
    lista_lampione.append(v_led)
    
    # Mantieni solo gli ultimi 40 dati per non intasare il grafico
    if len(lista_luce) > 40:
        lista_luce.pop(0)
        lista_movimento.pop(0)
        lista_lampione.pop(0)
        
    # Grafico 1: Luce (LDR)
    ax1.cla()
    ax1.plot(lista_luce, color="#58a6ff", label="Luce Attuale")
    ax1.axhline(SOGLIA_BUIO, color="red", linestyle="--", label="Soglia Buio")
    ax1.set_title("1. Sensore di Luce (LDR)")
    ax1.set_ylim(-50, 1100)
    ax1.legend(loc="upper left")

    # Grafico 2: Movimento (PIR)
    ax2.cla()
    ax2.step(range(len(lista_movimento)), lista_movimento, color="#3fb950")
    ax2.set_title("2. Sensore di Movimento (PIR) - [0 = No, 1 = Sì]")
    ax2.set_ylim(-0.2, 1.2)

    # Grafico 3: Stato Lampione (LED)
    ax3.cla()
    ax3.step(range(len(lista_lampione)), lista_lampione, color="#f0c040")
    ax3.set_title("3. Stato Lampione (LED) - [0 = Spento, 1 = Acceso]")
    ax3.set_ylim(-0.2, 1.2)
    
    plt.tight_layout()

# Avvia l'animazione: aggiorna lo schermo ogni 500 millisecondi (mezzo secondo)
ani = FuncAnimation(fig, aggiorna, interval=500, cache_frame_data=False)
plt.show()
import random  # Importa la libreria per generare numeri casuali (simula i sensori)
import time    # Importa la libreria per gestire il tempo (per fare le pause di 1 secondo)

# ── 1. PARAMETRI DI CONFIGURAZIONE ─────────────────────────────────────
SOGLIA_BUIO = 400      # Valore di luminosità sotto il quale il sistema considera che sia "buio"
TIMEOUT_LED = 3        # Numero di secondi per cui il lampione resta acceso dopo un movimento

valore_luce = 200     # Valore iniziale della luce (il programma parte simulando il giorno)
timer_lampione = 0     # Timer del lampione (all'avvio il lampione è spento)
cronologia_stati = []  # Lista (memoria) che conterrà le stringhe di testo da mostrare a schermo

print("=== AVVIO SIMULAZIONE LAMPIONE SMART ===")
print("Legenda: [L = Luce] | [M = Movimento (0/1)] | [❌ = Spento | 💡 = Acceso]\n")

# ── 2. CICLO IN TEMPO REALE (LOOP INFINITO) ───────────────────────────
while True:  # Avvia un ciclo infinito: tutto ciò che è dentro verrà eseguito a ripetizione
    # A) Simulazione Luce: sceglie a caso se sommare o sottrarre un valore tra quelli in lista
    valore_luce += random.choice([-50, -20, 20, 50])
    valore_luce = max(0, min(1023, valore_luce))  # Blocca il valore della luce tra 0 e 1023
    
    # B) Simulazione Movimento: genera 1 (passa qualcuno) con il 25% di probabilità, altrimenti 0
    movimento = 1 if random.random() < 0.25 else 0
    
    # C) Logica di controllo (Come un Arduino)
    buio = valore_luce < SOGLIA_BUIO  # Controlla se la luce attuale è inferiore alla soglia del buio
    
    if buio and movimento:  # Se è buio E contemporaneamente si muove qualcuno...
        timer_lampione = TIMEOUT_LED  # ...allora imposta (o ricarica) il timer a 3 secondi
        
    if timer_lampione > 0:  # Se il timer è maggiore di zero (il lampione deve stare acceso)...
        lampione_acceso = 1  # Imposta lo stato del lampione su 1 (ACCESO)
        timer_lampione -= 1  # Sottrae 1 secondo al timer per il ciclo successivo
    else:                   # Se invece il timer è arrivato a zero...
        lampione_acceso = 0  # Imposta lo stato del lampione su 0 (SPENTO)

# ── 3. COSTRUZIONE DEL GRAFICO TESTUALE ────────────────────────────
    icona = "💡" if lampione_acceso == 1 else "❌"  # Sceglie l'emoji in base allo stato del lampione
    
    # Crea una riga di testo che fotografa la situazione di questo preciso secondo
    riga_corrente = f"L:{valore_luce:4d} | M:{movimento} | {icona}"
    cronologia_stati.append(riga_corrente)  # Aggiunge questa riga in coda alla lista della cronologia
    
    if len(cronologia_stati) > 10:  # Se nella cronologia ci sono più di 10 secondi memorizzati...
        cronologia_stati.pop(0)     # ...cancella il secondo più vecchio (crea l'effetto scorrimento)
        
    print("\n" * 5)  # Stampa 5 righe vuote per distanziare i dati e pulire visivamente la schermata
    for stato in cronologia_stati:  # Prende uno alla volta i secondi memorizzati nella cronologia...
        print(stato)               # ...e li stampa a schermo (disegna il grafico riga per riga)
        
    time.sleep(1)  # Ferma il programma per esattamente 1 secondo prima di riniziare il ciclo
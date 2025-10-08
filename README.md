# Associazione matricole a macchine
Vari script Python per estrarre i dati dai file dove sono registrati i dati delle macchine di espressivo.

## Metodo
Da come è stato gestito il file si necessitano di almeno due passaggi:
1) La conversione dei dati delle macchine registrate con data e ddt
2) L'elaborazione di tutto il resto ovvero: fatture, macchine riparate, macchine spostate qua e là, macchine rottamate, cambi di proprietà, ecc...

Il metodo consiste nella:
1) Pulizia dei dati alla sorgente ovvero togliendo:
    1. la rimozione dei dati di cui il punto 2 precedente
    2. le righe e le colonne vuote
    3. ogni altra aberrazionne (rimuoverla o sistemarla)
2) Conto delle macchina e delle matricole, vedere dove differiscono
3) Ripetere i punti 1 e 2 finche non ci sono più errori
4) Eseguire lo script
5) Controlli sui dati in output:
    1. Numero di macchine deve corrispondere
    2. Le macchine senza matricole devono averre un numero sequenziale del tipo: C&S-001, GC-021, ...
6) Unire i dati in un unico file

## Output
date, model, matricola
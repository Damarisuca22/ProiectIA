"""Generarea celor 3 grafice de performanță."""

import time
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict
import sys
import os

# Adaugă calea pentru importuri
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backtracking import rezolva_tsp_backtracking
from hill_climbing_tsp import rezolva_tsp_hill_climbing


def genereaza_matrice(n: int, seed: int = 42) -> List[List[int]]:
    """Generează o matrice aleatorie simetrică."""
    random.seed(seed)
    matrice = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = random.randint(1, 100)
            matrice[i][j] = dist
            matrice[j][i] = dist
    
    return matrice


def ruleaza_experiment_cu_3_grafice():
    """Rulează experimentul și generează 3 grafice."""
    
    print("=" * 60)
    print("EXPERIMENT TSP - 3 GRAFICE")
    print("=" * 60)
    
    # Valori N pentru testare
    n_backtracking = [5, 6, 7, 8, 9, 10, 11, 12]
    n_hill_climbing = [5, 7, 10, 12, 15, 20, 25, 30, 40, 50]
    
    # Stocare rezultate
    timpi_bt = []
    timpi_hc = []
    n_bt_rez = []
    n_hc_rez = []
    
    # Rulează backtracking
    print("\n BACKTRACKING:")
    for n in n_backtracking:
        print(f"  Testare n={n}... ", end="")
        matrice = genereaza_matrice(n)
        
        try:
            start = time.perf_counter()
            traseu, cost = rezolva_tsp_backtracking(n, matrice)
            durata = time.perf_counter() - start
            
            n_bt_rez.append(n)
            timpi_bt.append(durata)
            print(f"OK - {durata:.4f}s")
        except Exception as e:
            print(f"Eroare: {e}")
    
    # Rulează hill climbing
    print("\n HILL CLIMBING:")
    for n in n_hill_climbing:
        print(f"  Testare n={n}... ", end="")
        matrice = genereaza_matrice(n)
        
        try:
            start = time.perf_counter()
            traseu, cost = rezolva_tsp_hill_climbing(n, matrice, restarturi=15)
            durata = time.perf_counter() - start
            
            n_hc_rez.append(n)
            timpi_hc.append(durata)
            print(f"OK - {durata:.4f}s")
        except Exception as e:
            print(f"Eroare: {e}")
    
    # Creează cele 3 grafice
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # GRAFIC 1: Scară liniară
    ax1.plot(n_bt_rez, timpi_bt, 'bo-', label='Backtracking', linewidth=2, markersize=8)
    ax1.plot(n_hc_rez, timpi_hc, 'rs-', label='Hill Climbing', linewidth=2, markersize=8)
    ax1.set_xlabel('Număr orașe (N)')
    ax1.set_ylabel('Timp (secunde)')
    ax1.set_title('1. Scară Liniară')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # GRAFIC 2: Scară logaritmică
    ax2.semilogy(n_bt_rez, timpi_bt, 'bo-', label='Backtracking', linewidth=2, markersize=8)
    ax2.semilogy(n_hc_rez, timpi_hc, 'rs-', label='Hill Climbing', linewidth=2, markersize=8)
    ax2.set_xlabel('Număr orașe (N)')
    ax2.set_ylabel('Timp (secunde) - scară log')
    ax2.set_title('2. Scară Logaritmică')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # GRAFIC 3: Bare pentru N comune
    n_comune = sorted(set(n_bt_rez) & set(n_hc_rez))
    timpi_bt_comuni = []
    timpi_hc_comuni = []
    
    for n in n_comune:
        idx_bt = n_bt_rez.index(n)
        idx_hc = n_hc_rez.index(n)
        timpi_bt_comuni.append(timpi_bt[idx_bt])
        timpi_hc_comuni.append(timpi_hc[idx_hc])
    
    x = np.arange(len(n_comune))
    width = 0.35
    
    ax3.bar(x - width/2, timpi_bt_comuni, width, label='Backtracking', color='blue', alpha=0.7)
    ax3.bar(x + width/2, timpi_hc_comuni, width, label='Hill Climbing', color='red', alpha=0.7)
    ax3.set_xlabel('Număr orașe (N)')
    ax3.set_ylabel('Timp (secunde)')
    ax3.set_title('3. Comparare Directă (N comune)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(n_comune)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Comparație Backtracking vs Hill Climbing pentru TSP', fontsize=16)
    plt.tight_layout()
    
    # Salvează graficul
    cale_iesire = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                               'comparare_3grafice.png')
    plt.savefig(cale_iesire, dpi=150, bbox_inches='tight')
    print(f"\n📊 Grafic salvat în: {cale_iesire}")
    
    # Afișează rezumat
    print("\n" + "=" * 60)
    print("REZUMAT")
    print("=" * 60)
    
    print("\n BACKTRACKING:")
    for n, t in zip(n_bt_rez, timpi_bt):
        print(f"  N={n:2d}: {t:.6f}s")
    
    print("\n HILL CLIMBING:")
    for n, t in zip(n_hc_rez, timpi_hc):
        print(f"  N={n:2d}: {t:.6f}s")
    
    # Găsește pragul de 30 secunde pentru backtracking
    for n, t in zip(n_bt_rez, timpi_bt):
        if t >= 30:
            print(f"\n  PRAG DE 30 SECUNDE: N={n} (timp={t:.2f}s)")
            break
    
    plt.show()
    
    return {
        'backtracking': {'n': n_bt_rez, 'timpi': timpi_bt},
        'hill_climbing': {'n': n_hc_rez, 'timpi': timpi_hc}
    }


if __name__ == "__main__":
    ruleaza_experiment_cu_3_grafice()
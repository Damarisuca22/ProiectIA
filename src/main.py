"""Punct principal de intrare pentru proiectul TSP."""

""" RULARE------------------
# Doar backtracking (cerinta A)
py src/main.py --backtracking date/orase.txt

# Doar hill climbing (cerinta B)
py src/main.py --hill-climbing date/orase.txt

# Comparatie intre A si B
py src/main.py --compare date/orase.txt
"""

import sys
import os
import argparse
import time

# Adauga calea pentru importuri
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.io_utils import citeste_matrice, salveaza_rezultat
from backtracking import rezolva_tsp_backtracking
from hill_climbing_tsp import rezolva_tsp_hill_climbing


def main():
    parser = argparse.ArgumentParser(description='Rezolvarea TSP')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--backtracking', metavar='FISIER', 
                       help='Ruleaza backtracking pe fisier')
    group.add_argument('--hill-climbing', metavar='FISIER', 
                       help='Ruleaza hill climbing pe fisier')
    group.add_argument('--compare', metavar='FISIER', 
                       help='Compara ambii algoritmi')
    
    parser.add_argument('--restarturi', type=int, default=10,
                        help='Numar reporniri pentru hill climbing')
    parser.add_argument('--output', '-o', metavar='FISIER',
                        help='Salveaza rezultatul')
    
    args = parser.parse_args()
    
    # Citeste fisierul de intrare
    fisier = args.backtracking or args.hill_climbing or args.compare
    try:
        n, matrice = citeste_matrice(fisier)
        print(f"\n Fisier: {fisier}")
        print(f" Numar orase: {n}")
    except Exception as e:
        print(f" Eroare: {e}")
        sys.exit(1)
    
    # Backtracking
    if args.backtracking:
        print("\n Ruleaza BACKTRACKING...")
        start = time.perf_counter()
        traseu, cost = rezolva_tsp_backtracking(n, matrice)
        durata = time.perf_counter() - start
        
        print(f"\nTraseu: {' -> '.join(map(str, traseu))} -> {traseu[0]}")
        print(f" Cost: {cost}")
        print(f"  Timp: {durata:.6f} secunde")
        
        if args.output:
            salveaza_rezultat(args.output, n, traseu, cost, durata, "backtracking")
            print(f" Salvat in: {args.output}")
    
    # Hill Climbing
    elif args.hill_climbing:
        print(f"\n Ruleaza HILL CLIMBING ({args.restarturi} reporniri)...")
        start = time.perf_counter()
        traseu, cost = rezolva_tsp_hill_climbing(
            n, matrice, restarturi=args.restarturi
        )
        durata = time.perf_counter() - start
        
        print(f"\n Traseu: {' -> '.join(map(str, traseu))} -> {traseu[0]}")
        print(f" Cost: {cost}")
        print(f"  Timp: {durata:.6f} secunde")
        
        if args.output:
            salveaza_rezultat(args.output, n, traseu, cost, durata, 
                              f"hill_climbing_{args.restarturi}")
            print(f" Salvat in: {args.output}")
    
    # Comparatie
    elif args.compare:
        print("\n COMPARATIE ALGORITMI")
        
        # Backtracking
        start = time.perf_counter()
        traseu_bt, cost_bt = rezolva_tsp_backtracking(n, matrice)
        durata_bt = time.perf_counter() - start
        
        print(f"\n BACKTRACKING:")
        print(f"  Traseu: {' -> '.join(map(str, traseu_bt))} -> {traseu_bt[0]}")
        print(f"  Cost: {cost_bt}")
        print(f"  Timp: {durata_bt:.6f}s")
        
        # Hill Climbing
        start = time.perf_counter()
        traseu_hc, cost_hc = rezolva_tsp_hill_climbing(
            n, matrice, restarturi=args.restarturi
        )
        durata_hc = time.perf_counter() - start
        
        print(f"\n HILL CLIMBING:")
        print(f"  Traseu: {' -> '.join(map(str, traseu_hc))} -> {traseu_hc[0]}")
        print(f"  Cost: {cost_hc}")
        print(f"  Timp: {durata_hc:.6f}s")
        
        # Diferenta
        if cost_bt > 0:
            diff = ((cost_hc - cost_bt) / cost_bt) * 100
            print(f"\n Diferenta cost: {diff:+.2f}%")
            print(f" Raport timp: {durata_bt/durata_hc:.2f}x")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write("COMPARATIE TSP\n")
                f.write("="*40 + "\n\n")
                f.write(f"Backtracking: {durata_bt:.6f}s, cost={cost_bt}\n")
                f.write(f"Hill Climbing: {durata_hc:.6f}s, cost={cost_hc}\n")
                f.write(f"Diferenta: {diff:+.2f}%\n")
            print(f"\n Salvat in: {args.output}")


if __name__ == "__main__":
    main()

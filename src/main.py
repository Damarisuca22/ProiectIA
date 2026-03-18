"""Punct principal de intrare pentru proiectul TSP."""

import sys
import os
import argparse
import time

# Adaugă calea pentru importuri
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.io_utils import citeste_matrice, salveaza_rezultat
from backtracking import rezolva_tsp_backtracking
from hill_climbing_tsp import rezolva_tsp_hill_climbing
from utils.performance import ruleaza_experiment_cu_3_grafice


def main():
    parser = argparse.ArgumentParser(description='Rezolvarea TSP')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--backtracking', metavar='FISIER', 
                       help='Rulează backtracking pe fișier')
    group.add_argument('--hill-climbing', metavar='FISIER', 
                       help='Rulează hill climbing pe fișier')
    group.add_argument('--compare', metavar='FISIER', 
                       help='Compară ambii algoritmi')
    group.add_argument('--experiment', action='store_true', 
                       help='Rulează experimentul cu 3 grafice')
    
    parser.add_argument('--restarturi', type=int, default=10,
                        help='Număr reporniri pentru hill climbing')
    parser.add_argument('--output', '-o', metavar='FISIER',
                        help='Salvează rezultatul')
    
    args = parser.parse_args()
    
    # Experiment cu 3 grafice
    if args.experiment:
        print(" Rulează experimentul cu 3 grafice...")
        ruleaza_experiment_cu_3_grafice()
        return
    
    # Citește fișierul de intrare
    fisier = args.backtracking or args.hill_climbing or args.compare
    try:
        n, matrice = citeste_matrice(fisier)
        print(f"\n Fișier: {fisier}")
        print(f" Număr orașe: {n}")
    except Exception as e:
        print(f" Eroare: {e}")
        sys.exit(1)
    
    # Backtracking
    if args.backtracking:
        print("\n Rulează BACKTRACKING...")
        start = time.perf_counter()
        traseu, cost = rezolva_tsp_backtracking(n, matrice)
        durata = time.perf_counter() - start
        
        print(f"\nTraseu: {' -> '.join(map(str, traseu))} -> {traseu[0]}")
        print(f" Cost: {cost}")
        print(f"  Timp: {durata:.6f} secunde")
        
        if args.output:
            salveaza_rezultat(args.output, n, traseu, cost, durata, "backtracking")
            print(f" Salvat în: {args.output}")
    
    # Hill Climbing
    elif args.hill_climbing:
        print(f"\n Rulează HILL CLIMBING ({args.restarturi} reporniri)...")
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
            print(f" Salvat în: {args.output}")
    
    # Comparație
    elif args.compare:
        print("\n COMPARAȚIE ALGORITMI")
        
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
        
        # Diferență
        if cost_bt > 0:
            diff = ((cost_hc - cost_bt) / cost_bt) * 100
            print(f"\n Diferență cost: {diff:+.2f}%")
            print(f" Raport timp: {durata_bt/durata_hc:.2f}x")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write("COMPARAȚIE TSP\n")
                f.write("="*40 + "\n\n")
                f.write(f"Backtracking: {durata_bt:.6f}s, cost={cost_bt}\n")
                f.write(f"Hill Climbing: {durata_hc:.6f}s, cost={cost_hc}\n")
                f.write(f"Diferență: {diff:+.2f}%\n")
            print(f"\n Salvat în: {args.output}")


if __name__ == "__main__":
    main()
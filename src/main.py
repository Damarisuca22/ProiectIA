"""Punct principal de intrare pentru proiectul TSP - CERINȚA 1: Backtracking"""

import sys
import os
import argparse
import time


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.io_utils import citeste_matrice, salveaza_rezultat
from backtracking import rezolva_tsp_backtracking


def main():
    parser = argparse.ArgumentParser(description='TSP - Backtracking (CERINȚA 1)')
    
   
    parser.add_argument('fisier', metavar='FISIER', 
                        help='Fișierul cu matricea de distanțe')
    
 
    parser.add_argument('--output', '-o', metavar='FISIER',
                        help='Salvează rezultatul în fișier')
    
    args = parser.parse_args()
    
    # Citește fișierul de intrare
    try:
        n, matrice = citeste_matrice(args.fisier)
        print(f"\n Fișier: {args.fisier}")
        print(f"  Număr orașe: {n}")
        print("\nMatricea de distanțe:")
        for i, rand in enumerate(matrice):
            print(f"  {i}: {rand}")
    except Exception as e:
        print(f" Eroare la citire: {e}")
        sys.exit(1)
    
    
    print("\n Rulează BACKTRACKING...")
    start = time.perf_counter()
    
    try:
        traseu, cost = rezolva_tsp_backtracking(n, matrice)
        durata = time.perf_counter() - start
        
       
        print(f"\nRezultat:")
        print(f"   Traseu: {' -> '.join(map(str, traseu))} -> {traseu[0]}")
        print(f"   Cost: {cost}")
        print(f"   Timp: {durata:.6f} secunde")
        
       
        if args.output:
            salveaza_rezultat(args.output, n, traseu, cost, durata, "backtracking")
            print(f" Rezultat salvat în: {args.output}")
            
    except Exception as e:
        print(f" Eroare la rulare: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print(" TSP - CERINȚA 1: Backtracking")
    print("=" * 60)
    main()
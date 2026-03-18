"""Utilități pentru citirea și scrierea fișierelor."""

import os
from typing import List, Tuple


def citeste_matrice(cale_fisier: str) -> Tuple[int, List[List[int]]]:
    """
    Citește matricea de distanțe dintr-un fișier text.
    
    Format fișier:
        Linia 1: N (numărul de orașe)
        Următoarele N linii: câte N numere (matricea)
    
    Args:
        cale_fisier: Calea către fișier
        
    Returns:
        (n, matrice) - numărul de orașe și matricea N x N
        
    Raises:
        FileNotFoundError: Dacă fișierul nu există
        ValueError: Dacă formatul e invalid
    """
    if not os.path.exists(cale_fisier):
        raise FileNotFoundError(f"Fișierul {cale_fisier} nu există")
    
    with open(cale_fisier, 'r') as f:
        linii = [linie.strip() for linie in f if linie.strip()]
    
    if not linii:
        raise ValueError("Fișierul este gol")
    
    try:
        n = int(linii[0])
        matrice = []
        
        for i in range(n):
            linie = list(map(int, linii[i + 1].split()))
            if len(linie) != n:
                raise ValueError(f"Linia {i+1} trebuie să aibă {n} numere")
            matrice.append(linie)
        
      
        for i in range(n):
            if matrice[i][i] != 0:
                raise ValueError(f"Matrice[{i}][{i}] trebuie să fie 0")
        
        return n, matrice
        
    except ValueError as e:
        raise ValueError(f"Eroare la citire: {e}")


def salveaza_rezultat(cale_fisier: str, n: int, traseu: List[int], 
                      cost: int, timp: float, algoritm: str = "backtracking") -> None:
    """
    Salvează rezultatul într-un fișier.
    
    Args:
        cale_fisier: Calea fișierului de ieșire
        n: Numărul de orașe
        traseu: Lista cu ordinea orașelor
        cost: Costul total
        timp: Timpul de execuție
        algoritm: Numele algoritmului
    """
    with open(cale_fisier, 'w') as f:
        f.write(f"Algoritm: {algoritm}\n")
        f.write(f"Număr orașe: {n}\n")
        f.write(f"Traseu: {' -> '.join(map(str, traseu))} -> {traseu[0]}\n")
        f.write(f"Cost: {cost}\n")
        f.write(f"Timp: {timp:.6f} secunde\n")
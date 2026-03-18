"""Implementarea algoritmului Backtracking pentru TSP."""

import sys
from typing import List, Tuple


def _backtracking(matrice: List[List[int]], n: int, oras_curent: int,
                  vizitat: List[bool], traseu: List[int], cost_curent: int,
                  cost_minim: List[int], traseu_optim: List[List[int]]) -> None:
    """
    Funcție recursivă internă pentru backtracking.
    
    Args:
        matrice: Matricea de distanțe
        n: Numărul de orașe
        oras_curent: Orașul curent
        vizitat: Listă cu orașele vizitate
        traseu: Traseul curent
        cost_curent: Costul parțial
        cost_minim: Listă cu un element - costul minim (referință)
        traseu_optim: Listă cu un element - traseul optim (referință)
    """
   
    if len(traseu) == n:
        
        cost_total = cost_curent + matrice[oras_curent][traseu[0]]
        if cost_total < cost_minim[0]:
            cost_minim[0] = cost_total
            traseu_optim[0] = traseu.copy()
        return
    
    
    for urmator in range(n):
        if vizitat[urmator]:
            continue
            
        cost_nou = cost_curent + matrice[oras_curent][urmator]
        
       
        if cost_nou >= cost_minim[0]:
            continue
        
        vizitat[urmator] = True
        traseu.append(urmator)
        
        _backtracking(matrice, n, urmator, vizitat, traseu, cost_nou,
                      cost_minim, traseu_optim)
        
        # Backtrack
        traseu.pop()
        vizitat[urmator] = False


def rezolva_tsp_backtracking(n: int, matrice: List[List[int]]) -> Tuple[List[int], int]:
    """
    Rezolvă TSP folosind backtracking cu branch-and-bound.
    
    Args:
        n: Numărul de orașe
        matrice: Matricea de distanțe N x N
        
    Returns:
        (traseu_optim, cost_minim) - traseul optim și costul său
        
    Raises:
        ValueError: Dacă datele sunt invalide
    """
    if n <= 0:
        raise ValueError("Numărul de orașe trebuie să fie pozitiv")
    
    
    vizitat = [False] * n
    vizitat[0] = True  
    
    cost_minim = [sys.maxsize]
    traseu_optim = [[]]
    
  
    _backtracking(matrice, n, 0, vizitat, [0], 0, cost_minim, traseu_optim)
    
    if not traseu_optim[0]:
        raise RuntimeError("Nu s-a găsit niciun traseu")
    
    return traseu_optim[0], cost_minim[0]
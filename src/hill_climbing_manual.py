"""
Hill Climbing MANUAL pentru problema TSP.
Implementare completa fara biblioteci externe (doar Python standard).
"""

import random
import time
from typing import List, Tuple, Optional


def calculeaza_cost(tur: List[int], matrice: List[List[int]]) -> int:
    """
    Calculeaza costul total al unui tur TSP.
    
    Args:
        tur: Lista cu ordinea oraselor (ex: [0, 2, 1, 3])
        matrice: Matricea de distante N x N
        
    Returns:
        Costul total al turului (include si intoarcerea la start)
    """
    n = len(tur)
    cost = 0
    
    # Calculeaza distanta dintre orase consecutive
    for i in range(n - 1):
        cost += matrice[tur[i]][tur[i + 1]]
    
    # Adauga distanta de intoarcere la primul oras
    cost += matrice[tur[-1]][tur[0]]
    return cost


def genereaza_vecini_2opt(tur: List[int]) -> List[List[int]]:
    """
    Genereaza toti vecinii folosind operatia 2-opt.
    Operatia 2-opt: alege doua pozitii i < j si inverseaza segmentul dintre ele.
    De exemplu, pentru turul [0,1,2,3,4] si i=1, j=3:
        segmentul [1,2,3] devine [3,2,1]
        rezultat: [0,3,2,1,4]
    Args: tur: Turul curent 
    Returns: Lista de tururi vecine (toate combinatiile 2-opt posibile)
    """
    n = len(tur)
    vecini = []
    
    # Generam toate perechile (i, j) cu i < j si diferenta > 1
    for i in range(n - 2):
        for j in range(i + 2, n):
            # Creeaza un nou tur inversand segmentul dintre i si j
            vecin = tur[:i] + tur[i:j+1][::-1] + tur[j+1:]
            vecini.append(vecin)
    
    return vecini


def gaseste_cel_mai_bun_vecin(tur_curent: List[int], 
                               matrice: List[List[int]]) -> Tuple[List[int], int]:
    """
    Args:
        tur_curent: Turul curent
        matrice: Matricea de distante
        
    Returns:
        (cel_mai_bun_vecin, costul_sau)
    """
    vecini = genereaza_vecini_2opt(tur_curent)
    cost_curent = calculeaza_cost(tur_curent, matrice)
    
    cel_mai_bun_vecin = None
    cel_mai_bun_cost = cost_curent
    
    for vecin in vecini:
        cost_vecin = calculeaza_cost(vecin, matrice)
        if cost_vecin < cel_mai_bun_cost:
            cel_mai_bun_cost = cost_vecin
            cel_mai_bun_vecin = vecin
    
    return cel_mai_bun_vecin, cel_mai_bun_cost


def hill_climbing_steepest_ascent(tur_initial: List[int], 
                                   matrice: List[List[int]],
                                   iteratii_max: int = 1000) -> Tuple[List[int], int, int]:
    """
    Ruleaza algoritmul Hill Climbing cu cea mai abrupta panta (steepest ascent).
    
    Args:
        tur_initial: Turul de start
        matrice: Matricea de distante
        iteratii_max: Numarul maxim de iteratii
        
    Returns:
        (tur_final, cost_final, numar_iteratii)
    """
    tur_curent = tur_initial.copy()
    cost_curent = calculeaza_cost(tur_curent, matrice)
    
    for iteratie in range(iteratii_max):
        # Gaseste cel mai bun vecin
        cel_mai_bun_vecin, cost_vecin = gaseste_cel_mai_bun_vecin(tur_curent, matrice)
        
        # Daca nu exista vecin mai bun, ne oprim (optim local)
        if cel_mai_bun_vecin is None or cost_vecin >= cost_curent:
            return tur_curent, cost_curent, iteratie + 1
        
        # Altfel, ne mutam la vecinul mai bun
        tur_curent = cel_mai_bun_vecin
        cost_curent = cost_vecin
    
    return tur_curent, cost_curent, iteratii_max


def genereaza_tur_aleator(n: int) -> List[int]:
    """
    Genereaza un tur aleator pentru n orase.
    Args:
        n: Numarul de orase
    Returns:
        O permutare aleatoare a oraselor 0..n-1
    """
    tur = list(range(n))
    random.shuffle(tur)
    return tur


def hill_climbing_cu_reporniri(n: int,
                               matrice: List[List[int]],
                               numar_reporniri: int = 10,
                               iteratii_max: int = 1000,
                               afiseaza_progres: bool = False) -> Tuple[List[int], int]:
    """
    Ruleaza Hill Climbing cu reporniri aleatorii.
    Args:
        n: Numarul de orase
        matrice: Matricea de distante
        numar_reporniri: Cate reporniri sa facem
        iteratii_max: Iteratii maxime per repornire
        afiseaza_progres: Afiseaza progresul in consola  
    Returns:
        (cel_mai_bun_tur, cel_mai_bun_cost)
    """
    cel_mai_bun_tur = None
    cel_mai_bun_cost = float('inf')
    
    for rep in range(numar_reporniri):
        # Genereaza tur initial aleator
        tur_initial = genereaza_tur_aleator(n)
        
        if afiseaza_progres:
            print(f"  Repornire {rep + 1}/{numar_reporniri}... ", end="")
        
        # Ruleaza hill climbing
        tur_final, cost_final, iteratii = hill_climbing_steepest_ascent(
            tur_initial, matrice, iteratii_max
        )
        
        if afiseaza_progres:
            print(f"cost={cost_final}, {iteratii} iteratii")
        
        # Actualizeaza cea mai buna solutie
        if cost_final < cel_mai_bun_cost:
            cel_mai_bun_tur = tur_final
            cel_mai_bun_cost = cost_final
            if afiseaza_progres:
                print(f"     Nou record global: {cel_mai_bun_cost}")
    
    return cel_mai_bun_tur, cel_mai_bun_cost


# ==================== FUNCTIA PRINCIPALA PENTRU EXPORT 

def hill_climbing_manual(n: int, 
                         matrice: List[List[int]], 
                         restarturi: int = 10,
                         iteratii_max: int = 1000,
                         verbose: bool = False) -> Tuple[List[int], int]:
    """
    Functia principala pentru Hill Climbing MANUAL.
    Aceasta este functia care trebuie apelata din alte module.
    Args:
        n: Numarul de orase
        matrice: Matricea de distante
        restarturi: Numarul de reporniri aleatorii
        iteratii_max: Iteratii maxime per repornire
        verbose: Afiseaza progresul
        
    Returns:
        (cel_mai_bun_tur, cel_mai_bun_cost)
    """
    return hill_climbing_cu_reporniri(
        n, matrice, 
        numar_reporniri=restarturi,
        iteratii_max=iteratii_max,
        afiseaza_progres=verbose
    )


# ==================== VERSIUNE SIMPLIFICATA 

def hill_climbing_manual_simplu(n: int, 
                                matrice: List[List[int]], 
                                restarturi: int = 10) -> Tuple[List[int], int]:
    """
    Versiune simplificata pentru apel rapid (fara parametri optionali).
    
    Args:
        n: Numarul de orase
        matrice: Matricea de distante
        restarturi: Numarul de reporniri
        
    Returns:
        (cel_mai_bun_tur, cel_mai_bun_cost)
    """
    return hill_climbing_manual(n, matrice, restarturi, verbose=False)


# ==================== TEST 

if __name__ == "__main__":
    
    print("=" * 60)
    print(" HILL CLIMBING MANUAL - TEST")
    print("=" * 60)
    
    # Matricea de test 
    matrice_test = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    n = 4
    
    print(f"\n Problema cu {n} orase")
    print("Matricea de distante:")
    for i, rand in enumerate(matrice_test):
        print(f"  {i}: {rand}")
    
    # Test 1: O singura rulare
    print("\n" + "-" * 40)
    print("TEST 1: O singura rulare")
    print("-" * 40)
    
    tur_aleator = genereaza_tur_aleator(n)
    print(f"Tur initial aleator: {tur_aleator}")
    print(f"Cost initial: {calculeaza_cost(tur_aleator, matrice_test)}")
    
    start = time.time()
    tur_final, cost_final, iteratii = hill_climbing_steepest_ascent(
        tur_aleator, matrice_test
    )
    durata = time.time() - start
    
    print(f"Tur final: {tur_final}")
    print(f"Cost final: {cost_final}")
    print(f"Iteratii: {iteratii}")
    print(f"Timp: {durata:.6f} secunde")
    
    # Test 2: Cu reporniri
    print("\n" + "-" * 40)
    print("TEST 2: Cu 10 reporniri")
    print("-" * 40)
    
    start = time.time()
    tur_optim, cost_optim = hill_climbing_manual(
        n, matrice_test, 
        restarturi=10, 
        iteratii_max=1000,
        verbose=True
    )
    durata = time.time() - start
    
    print(f"\n REZULTAT FINAL:")
    print(f"  Traseu: {' -> '.join(map(str, tur_optim))} -> {tur_optim[0]}")
    print(f"  Cost: {cost_optim}")
    print(f"  Timp total: {durata:.4f} secunde")
    
    # Verifica daca a gasit optimul (80)
    if cost_optim == 80:
        print("   Solutie optima gasita!")
    else:
        print(f"   Solutie suboptimala (optimul este 80)")
    
    # Test 3: Generare matrice aleatorie mai mare
    print("\n" + "-" * 40)
    print("TEST 3: Problema cu 10 orase aleatorii")
    print("-" * 40)
    
    # Genereaza matrice aleatorie pentru 10 orase
    random.seed(42)  
    n2 = 10
    matrice_random = [[0] * n2 for _ in range(n2)]
    for i in range(n2):
        for j in range(i + 1, n2):
            dist = random.randint(10, 100)
            matrice_random[i][j] = dist
            matrice_random[j][i] = dist
    
    print(f"Problema cu {n2} orase, distante intre 10 si 100")
    
    start = time.time()
    tur, cost = hill_climbing_manual(
        n2, matrice_random,
        restarturi=15,
        verbose=False
    )
    durata = time.time() - start
    
    print(f"  Cel mai bun cost gasit: {cost}")
    print(f"  Timp: {durata:.4f} secunde")
    
    print("\n" + "=" * 60)
    print("TEST COMPLET")
    print("=" * 60)
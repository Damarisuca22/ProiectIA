"""Hill Climbing pentru TSP."""

import random
from typing import List, Tuple, Optional
from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing_random_restarts


class TSPHillClimbing(SearchProblem):
    """
    Problema TSP pentru Hill Climbing.
    Starea este un tuplu cu ordinea orașelor (ex: (0, 2, 1, 3)).
    """
    
    def __init__(self, n: int, matrice: List[List[int]]):
        """
        Args:
            n: Numarul de orașe
            matrice: Matricea de distante
        """
        super().__init__(initial_state=None)
        self.n = n
        self.matrice = matrice
        self._cache_cost = {}  # Cache pentru costuri
        
    def generate_random_state(self) -> Tuple[int, ...]:
        """Genereaza o stare initiala aleatoare."""
        orase = list(range(self.n))
        random.shuffle(orase)
        return tuple(orase)
    
    def actions(self, state: Tuple[int, ...]) -> List[Tuple[int, int]]:
        """
        Genereaza actiuni posibile (operatii 2-opt).
        2-opt: alege i < j si inverseaza subsecventa dintre ele.
        Returns: Lista de tupluri (i, j)
        """
        actiuni = []
        for i in range(self.n - 2):
            for j in range(i + 2, self.n):
                actiuni.append((i, j))
        return actiuni
    
    def result(self, state: Tuple[int, ...], action: Tuple[int, int]) -> Tuple[int, ...]:
        """Aplica operatia 2-opt."""
        i, j = action
        # Converteste in lista-inverseaza segmentul-revino la tuplu
        lista = list(state)
        lista[i:j+1] = reversed(lista[i:j+1])
        return tuple(lista)
    
    def value(self, state: Tuple[int, ...]) -> float:
        """
        Calculeaza valoarea euristica (negativul costului).
        simpleai MAXIMIZEAZA, deci retrun -cost.
        """
        if state not in self._cache_cost:
            cost = 0
            for k in range(self.n - 1):
                cost += self.matrice[state[k]][state[k + 1]]
            cost += self.matrice[state[-1]][state[0]]  
            self._cache_cost[state] = cost
        
        return -self._cache_cost[state]
    
    def calculeaza_cost(self, state: Tuple[int, ...]) -> int:
        """Calculeaza costul (folosit extern)."""
        if state not in self._cache_cost:
            self.value(state)  
        return self._cache_cost[state]


def rezolva_tsp_hill_climbing(n: int, matrice: List[List[int]],
                              restarturi: int = 10,
                              iteratii: Optional[int] = 5000) -> Tuple[List[int], int]:
    """
    Rezolva TSP folosind Hill Climbing cu reporniri aleatorii.
    Args:
        n: Numarul de orase
        matrice: Matricea de distante
        restarturi: Numarul de reporniri
        iteratii: Iteratii maxime per repornire (None = nelimitat)
    Returns: (traseu, cost) - cel mai bun traseu gasit și costul sau
    """
    problema = TSPHillClimbing(n, matrice)
    
    # Ruleaza hill climbing cu reporniri
    rezultat = hill_climbing_random_restarts(
        problema,
        restarts_limit=restarturi,
        iterations_limit=iteratii
    )
    
    cost = problema.calculeaza_cost(rezultat.state)
    
    return list(rezultat.state), cost
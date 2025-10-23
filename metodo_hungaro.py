from collections import deque
from typing import Set, List, Optional, Dict
from generar_grafo import hacer_grafo, grafo_apareado

class ApareamientoBipartito:
    def __init__(self, X: Set, Y: Set, edges: Dict):
        self.X = X
        self.Y = Y
        self.adj = edges
    
    # Vecinos de S
    def N(self, S: Set) -> Set:
        neighbors = set()
        for x in S:
            neighbors.update(self.adj.get(x, set()))
        return neighbors
    
    # Encontrar M-(u,y)-camino aumentante
    def camino_aumentante(self, u: any, y: any, M: Dict) -> Optional[List]:
        parent = {}
        queue = deque([u])
        visited = set([u])
        target_found = False
        
        while queue and not target_found:
            current = queue.popleft()
            # Si current está en X
            if current in self.X:
                # Explorar todos los vecinos en Y
                for neighbor in self.adj.get(current, set()):
                    if neighbor not in visited:
                        # La arista no está en M, usarla (aumentante)
                        if M.get(current) != neighbor:
                            parent[neighbor] = current
                            visited.add(neighbor)
                            if neighbor == y:
                                target_found = True
                                break
                            queue.append(neighbor)
            # current está en Y
            else:
                if current in M:
                    x_match = M[current]
                    if x_match not in visited:
                        parent[x_match] = current
                        visited.add(x_match)
                        queue.append(x_match)
        
        # Reconstruir camino si llegamos a y
        if y in visited:
            path = []
            current = y
            while current != u:
                path.append(current)
                current = parent[current]
            path.append(u)
            return path[::-1]  # invertir camino
        
        return None
    
    def metodo_hungaro(self):
        M = {} # Elegir un apareamiento M
        
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteración {iteration} ---")
            print(f"M actual: {M}")
            
            # 1. Si M satura X entonces parar
            x_no_saturado = {x for x in X if x not in M}
            if not x_no_saturado:
                print("M completo")
                return M
            
            #   Si no u <- vértice no saturado de X
            #       S <- {u}; T <- conjunto vacio
            u = x_no_saturado.pop()
            print(f"u = {u}")
            S = {u}
            T = set()
            
            inner_iteration = 0
            while True:
                inner_iteration += 1
                print(f"\nSub-iteración {inner_iteration}:")
                print(f"S = {S}, T = {T}")
                
                # 2. Si N(S) = T entonces |N(S)| < |S| Parar
                N_S = self.N(S)
                print(f"N(S) = {N_S}")
                if N_S == T:
                    print(f"{len(N_S)} = |N(S)| < |S| = {len(S)}")
                    print("M no perfecto")
                    return M
                
                #   Si no hacer y <- un vértice de N(S)\T
                aux = N_S - T
                y = aux.pop()
                print(f"{y} ∈ N(S)\\T")
                
                # 3. Si y es M-saturado entonces
                #       1. Sea yz pertenece a M;
                #       2. S <- S union {z};
                #       3. T <- T union {y};   Ir a 2
                if y in M:
                    z = M[y]
                    print(f"z = {z}")
                    S = S | {z}
                    T = T | {y}
                    print(f"S = S union {{{z}}} = {S}")
                    print(f"T = T union {{{y}}} = {T}")
                #   Si no  P: un M-(u,y)-camino aumentante
                #       1. M <- M exclusion P;    Ir a 1
                else:
                    P = self.camino_aumentante(u, y, M)
                    if P:
                        print(f"Camino aumentante: {P}")
                        for i in range(0, len(P)-1, 2):
                            x = P[i]
                            y = P[i+1]
                            M[x] = y
                            M[y] = x
                        print(f"Nuevo M después de aumentar: {M}")
                    else:
                        print("ERROR: No se encontró camino aumentante")
                    break

if __name__ == "__main__":
    # Prueba 1
    '''
    X = {"x1", "x2", "x3"} # conjunto X
    Y = {"y1", "y2", "y3"} # conjunto Y
    edges = {
        "x1": ["y1", "y2"],
        "x2": ["y1", "y2", "y3"],
        "x3": ["y1", "y3"]
    } # N(X)
    '''

    # Prueba 2
    '''
    X = {f'x{i}' for i in range(1, 11)} # conjunto X
    Y = {f'y{i}' for i in range(1, 11)} # conjunto Y
    edges = {
        'x1': ['y1', 'y2', 'y3', 'y4'],
        'x2': ['y1', 'y4', 'y5', 'y7'],
        'x3': ['y2', 'y5', 'y6', 'y8'],
        'x4': ['y1', 'y3', 'y6', 'y9'],
        'x5': ['y3', 'y4', 'y7', 'y10'],
        'x6': ['y2', 'y5', 'y8', 'y9'],
        'x7': ['y4', 'y6', 'y7', 'y10'],
        'x8': ['y5', 'y8', 'y9', 'y10'],
        'x9': ['y1', 'y2', 'y6', 'y8'],
        'x10': ['y3', 'y5', 'y7', 'y9']
    } # N(X)
    '''

    # Prueba 3
    '''
    X = {'A', 'B', 'C', 'D', 'E', 'F', 'G'} # conjunto X
    Y = {'1', '2', '3', '4', '5', '6', '7'} # conjunto Y
    edges = {
        'A': {'1', '2', '3'},
        'B': {'2', '4'},
        'C': {'1', '4', '5'},
        'D': {'3', '5', '6'},
        'E': {'4', '6', '7'},
        'F': {'5', '7'},
        'G': {'1', '7'}
    } # N(X)
    '''
    
    # Prueba 4
    '''
    X = {"x1", "x2", "x3", "x4", "x5"} # conjunto X
    Y = {"y1", "y2", "y3", "y4", "y5"} # conjunto Y
    edges = {
        "x1": ["y2", "y3"],
        "x2": ["y1", "y2", "y4", "y5"],
        "x3": ["y2", "y3"],
        "x4": ["y2", "y3"],
        "x5": ["y4", "y5"]
    } # N(X)
    '''

    X = {f'x{i}' for i in range(1, 11)} # conjunto X
    Y = {f'y{i}' for i in range(1, 11)} # conjunto Y
    edges = {
        'x1': ['y1', 'y2', 'y3', 'y4'],
        'x2': ['y1', 'y4', 'y5', 'y7'],
        'x3': ['y2', 'y5', 'y6', 'y8'],
        'x4': ['y1', 'y3', 'y6', 'y9'],
        'x5': ['y3', 'y4', 'y7', 'y10'],
        'x6': ['y2', 'y5', 'y8', 'y9'],
        'x7': ['y4', 'y6', 'y7', 'y10'],
        'x8': ['y5', 'y8', 'y9', 'y10'],
        'x9': ['y1', 'y2', 'y6', 'y8'],
        'x10': ['y3', 'y5', 'y7', 'y9']
    } # N(X)

    hacer_grafo(X, Y, edges, "grafo_inicial")
    print("\n=== Metodo Hungaro ===")
    print(f"Conjunto X: {X}")
    print(f"Conjunto Y: {Y}")
    print("Aristas:")
    for x in sorted(X):
        print(f"{x}: {edges[x]}")
    
    bipartito = ApareamientoBipartito(X, Y, edges)
    M = bipartito.metodo_hungaro()
    
    grafo_apareado(X, Y, edges, M, "grafo_apareado")
    
    print("\n" + "="*50)
    print("Resultado:")
    parejas = []
    for x in sorted(X):
        if x in M:
            parejas.append(f"{x} -- {M[x]}")
        else:
            parejas.append(f"{x} -- No emparejado")
    
    for pareja in parejas:
        print(f"{pareja}")
    
    matched_count = len([x for x in X if x in M])
    print("Apareamiento perfecto" if matched_count == len(X) else "Apareamiento no perfecto")
from typing import Dict, List
from metodo_hungaro import ApareamientoBipartito
from generar_grafo import hacer_grafo, grafo_apareado

def xname(i: int) -> str:
    return f"x{i+1}"
def yname(j: int) -> str:
    return f"y{j+1}"

class Kuhn_Munkres:
    def __init__(self, W: List[List[int]]):
        self.W = [[int(v) for v in row] for row in W]
        # N en K_(n,n)
        self.n = len(self.W)
        # Etiquetas l(x)
        self.Lx = [max(row) if len(row) > 0 else 0 for row in self.W]
        # Etiquetas l(y)
        self.Ly = [0 for _ in range(self.n)]
        # Apareamiento
        self.M: Dict[str, str] = {}

    def peso_total_apareamiento(self) -> int:
        total = 0
        for x in self.M:
            if x.startswith('x'):
                y = self.M[x]
                i = int(x[1:]) - 1
                j = int(y[1:]) - 1
                total += self.W[i][j]
        return total
    
    def determinar_Gl(self) -> List[List[int]]:
        Gl = [[0]*self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if self.W[i][j] > 0 and (self.Lx[i] + self.Ly[j] == self.W[i][j]):
                    Gl[i][j] = self.W[i][j]
                else:
                    Gl[i][j] = 0
        return Gl
    
    def x_no_saturados(self):
        saturados = {int(k[1:]) - 1 for k in self.M.keys() if k.startswith('x')}
        return {i for i in range(self.n) if i not in saturados}

    # Encontrar M-(u,y)-camino aumentante en Gl
    def camino_aumentante(self, Gl: List[List[int]], u: int, y: int):
        inicio = ('x', u)
        objetivo = ('y', y)
        queue = [inicio]
        visited = set([inicio])
        parent = {}

        while queue:
            node = queue.pop(0)
            tipo, idx = node

            if tipo == 'x':
                # para toda arista (x_i,y_j) en Gl y NO está en M
                for j in range(self.n):
                    if Gl[idx][j] == 0:
                        continue
                    neighbor = ('y', j)
                    if neighbor in visited:
                        continue
                    # si (x_i,y_j) esta en M continuar a otra arista
                    if self.M.get(xname(idx)) == yname(j):
                        continue

                    parent[neighbor] = node
                    visited.add(neighbor)

                    # si y_j = y, reconstruir el camino
                    if neighbor == objetivo:
                        path = []
                        cur = neighbor
                        while cur != inicio:
                            path.append(cur)
                            cur = parent[cur]
                        path.append(inicio)
                        path.reverse()
                        return path

                    # si y_j está saturado, continuar hacia z para (z,y_j) en M'
                    if yname(j) in self.M:
                        z_name = self.M[yname(j)]
                        z_idx = int(z_name[1:]) - 1
                        z = ('x', z_idx)
                        if z not in visited:
                            parent[z] = neighbor
                            visited.add(z)
                            queue.append(z)
        # Si no se encontró un (u,y)-camino aumentante
        return None

    def calcular_alpha(self, S: set, T: set) -> int:
        # alpha = min_{x en S, y no en T} (l(x) + L(y) - W(xy))
        alpha = None
        for x in S:
            for y in range(self.n):
                if y in T:
                    continue
                # No hay arista
                if self.W[x][y] == 0:
                    continue
                val = (self.Lx[x] + self.Ly[y] - self.W[x][y])
                if alpha is None or val < alpha:
                    alpha = val
        if alpha is None:
            # no hay aristas entre S y Y\T
            return None
        return int(alpha)

    # Para fines de debug se imprime el estado de todas las variables del codigo
    def imprimir_estado(self, etapa: str, S=None, T=None, alpha=None):
        print("\n---", etapa, "---")
        print("Lx:", self.Lx)
        print("Ly:", self.Ly)
        if S is not None:
            print("S:", sorted([s+1 for s in S]))
        if T is not None:
            print("T:", sorted([t+1 for t in T]))
        if alpha is not None:
            print("alpha:", alpha)
        Gl = self.determinar_Gl()
        print("G_l:")
        for i in range(self.n):
            row = [1 if Gl[i][j] != 0 else 0 for j in range(self.n)]
            print(f"    x{i+1}: {row}")
        print("M actual:", self.M)
        print("\n")

    def metodo_optimo(self, verbose_hungaro=True, verbose= True):
        # Inicio: Etiq arb l; 
        # determinar Gl;
        Gl = self.determinar_Gl()
        if verbose:
            self.imprimir_estado("Inicio")
        # elegir un apar arb en Gl
        M0 = ApareamientoBipartito(Gl).metodo_hungaro(verbose_hungaro)
        self.M = dict(M0)
        if verbose:
            print("\nApareamiento arbitrario sobre G_l:", self.M)
            
        # 1) Si X es M-saturado, M es perfecto: Parar
        x_no_saturado = self.x_no_saturados()
        while x_no_saturado:
            #    Si no, sea u que pertenece a X no saturado de M; 
            #       S <- {u}; T <- {}
            u = x_no_saturado.pop()
            if verbose:
                print(f"\n  u = x{u+1} no saturado")
            S = {u}
            T = set()

            while True:
                Gl = self.determinar_Gl()
                # Obtener N_Gl(S)
                N_S = set()
                for x in S:
                    for j in range(self.n):
                        if Gl[x][j] != 0:
                            N_S.add(j)
                if verbose:
                    self.imprimir_estado("Estado antes de elegir y", S=S, T=T)

                # N_Gl(S)\T
                n_t = [y for y in sorted(list(N_S)) if y not in T]
                # 2) N_Gl(S)\T =/ vacio ?
                if n_t:
                    # 3) Elegir y que pertenece a N_Gl(S);
                    y = n_t[0]
                    if verbose:
                        print(f"Elegido y = y{y+1} ∈ N_Gl(S)\\T")
                    # Si y es M-saturado con yz que pertenece a M
                    if yname(y) in self.M:
                        z_name = self.M[yname(y)]
                        z = int(z_name[1:]) - 1
                        if verbose:
                            print(f"y{y+1} está M-saturado con {z_name}. S union {z_name} y T union y{y+1}")
                        # entonces S <- S union {z};
                        S.add(z)
                        # T <- T union {y};
                        T.add(y)
                        # ir a 2)
                        continue
                    # sino, Sea P un (u,y)-camino M-aumentante en Gl,
                    else:
                        if verbose:
                            print(f"Buscar camino aumentante desde x{u+1} hasta y{y+1} no saturado.")
                        P = self.camino_aumentante(Gl, u, y)
                        if P is None:
                            if verbose:
                                print("No se encontró camino aumentante.")
                            return self.M
                        # aplicar camino aumentante
                        if verbose:
                            p_str = " - ".join(f"{p[0]}{p[1]+1}" for p in P)
                            print("Camino aumentante:", p_str)
                        #  M <- M^ = M xor E(P);
                        for k in range(0, len(P)-1, 2):
                            xi = P[k][1]
                            yj = P[k+1][1]
                            xn = xname(xi)
                            yn = yname(yj)
                            self.M[xn] = yn
                            self.M[yn] = xn
                        if verbose:
                            print("Nuevo apareamiento M maximo:", self.M)
                        # Ir a 1)
                        break
                # Si no T = N_Gl(S)
                else:
                    # calcular alpha
                    alpha = self.calcular_alpha(S, T)
                    if alpha is None:
                        if verbose:
                            print("No hay aristas entre S y Y\\T")
                        return self.M
                    # actualizar etiquetado factible dado por
                    #        { l(v) - alpha si v pertenece a S
                    # l(v) = { l(v) + alpha si v pertenece a T
                    #        { l(v) de lo contrario
                    if verbose:
                        print(f"T == N_Gl(S). alpha = {alpha} y etiquetado factible (Lx -= alpha para S; Ly += alpha para T)")
                    for v in S:
                        self.Lx[v] -= alpha
                    for v in T:
                        self.Ly[v] += alpha

        if verbose:
            print("\n========== Emparejamiento final ==========")
            print(self.M)
        return self.M

if __name__ == "__main__":
    '''
    matriz = [
        [3, 5, 5, 4, 1],
        [2, 2, 0, 2, 2],
        [2, 4, 4, 1, 0],
        [0, 1, 1, 0, 0],
        [1, 2, 1, 3, 3]
    ]
    '''
    '''
    matriz = [
        [3, 5, 5, 0, 0, 0, 0],
        [0, 5, 0, 3, 0, 0, 0],
        [1, 0, 0, 5, 4, 0, 0],
        [0, 0, 5, 0, 3, 0, 4],
        [0, 0, 0, 5, 0, 1, 2],
        [0, 0, 0, 0, 3, 0, 2],
        [2, 0, 0, 0, 0, 0, 3]
    ]
    '''
    '''
    matriz = [
        [8,  6, 10,  9,  7,  2,  3,  5,  1,  4],
        [9,  8,  7,  6, 10,  3,  5,  4,  2,  1],
        [4, 10,  9,  8,  5,  6,  7,  2,  3,  1],
        [6,  9,  8, 10,  7,  4,  5,  2,  3,  1],
        [5,  7,  6,  9, 10,  8,  3,  4,  2,  1],
        [7,  8,  9, 10,  6,  5,  4,  3,  2,  1],
        [9, 10,  8,  7,  6,  5,  4,  3,  2,  1],
        [3,  2,  1,  4,  5,  6,  7,  8,  9, 10],
        [10, 9,  8,  7,  6,  5,  4,  3,  2,  1],
        [5,  6,  7,  8,  9, 10,  4,  3,  2,  1],
    ]

    '''

    matriz = [
        [8,  6, 10,  9,  7,  2,  3,  5,  1,  4],
        [9,  8,  7,  6, 10,  3,  5,  4,  2,  1],
        [4, 10,  9,  8,  5,  6,  7,  2,  3,  1],
        [6,  9,  8, 10,  7,  4,  5,  2,  3,  1],
        [5,  7,  6,  9, 10,  8,  3,  4,  2,  1],
        [7,  8,  9, 10,  6,  5,  4,  3,  2,  1],
        [9, 10,  8,  7,  6,  5,  4,  3,  2,  1],
        [3,  2,  1,  4,  5,  6,  7,  8,  9, 10],
        [10, 9,  8,  7,  6,  5,  4,  3,  2,  1],
        [5,  6,  7,  8,  9, 10,  4,  3,  2,  1],
    ]

    km = Kuhn_Munkres(matriz)
    M = km.metodo_optimo(False, False)

    for x, y in M.items():
        if x.startswith('x'):
            print(f"{x} → {y}")
    
    peso = km.peso_total_apareamiento()
    print(f"\nPeso total de M*: {peso}\n")

    hacer_grafo(matriz, len(matriz), "grafo_inicial")
    grafo_apareado(matriz, len(matriz), M, "grafo_apareado")

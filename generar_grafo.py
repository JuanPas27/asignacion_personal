import graphviz
import os

def hacer_grafo(matriz, n_node, file_name, output="grafos_generados"):
    if not os.path.exists(output):
        os.makedirs(output)
    
    dot = graphviz.Graph('asignación_personal', comment='Grafo bipartita', engine='neato')
    dot.attr(overlap='false', splines='curved', decorate='true')
    dot.attr(size=f'{n_node},{n_node}!', ratio='fill', 
             label='Grafo bipartita personal-tareas', fontsize='20')
    dot.attr('node', shape='circle', width='0.4', fixedsize='true')

    X = [f"x{i+1}" for i in range(len(matriz))]
    Y = [f"y{j+1}" for j in range(len(matriz[0]))]

    # Agregar nodos al grafo
    for i, x in enumerate(X):
        dot.node(x, x, pos=f"0,{i*1.0}!")
    for j, y in enumerate(Y):
        dot.node(y, y, pos=f"8,{j*1.0}!")

    # Agregar aristas entre los nodos
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            peso = matriz[i][j]
            if peso != 0:
                dot.edge(X[i], Y[j], label=str(peso), fontsize='10', len='1.5')

    file_path = os.path.join(output, file_name)
    dot.render(file_path, format='png', view=True, cleanup=True)
    print(f"¡Grafo guardado en '{file_path}.png'!")

def grafo_apareado(matriz, n_node, M, file_name, output="grafos_generados"):
    if not os.path.exists(output):
        os.makedirs(output)
    
    dot = graphviz.Graph('asignación_personal', 
                         comment='Apareamiento maximo en grafo bipartita', engine='neato')
    dot.attr(overlap='false', splines='curved', decorate='true')
    dot.attr(size=f'{n_node},{n_node}!', ratio='fill', 
             label='Apareamiento maximo en grafo bipartita', fontsize='20')
    dot.attr('node', shape='circle', width='0.4', fixedsize='true')

    # Agregar nodos al grafo
    X = [f"x{i+1}" for i in range(len(matriz))]
    Y = [f"y{j+1}" for j in range(len(matriz[0]))]

    for i, x in enumerate(X):
        dot.node(x, x, pos=f"0,{i*1.0}!")
    for j, y in enumerate(Y):
        dot.node(y, y, pos=f"8,{j*1.0}!")

    # Agregar aristas entre los nodos
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            peso = matriz[i][j]
            if peso != 0:
                if M.get(X[i]) == Y[j] or M.get(Y[j]) == X[i]:
                    dot.edge(X[i], Y[j], color='red', penwidth='3', 
                             label=str(peso), fontsize='10', len='1.5')
                else:
                    dot.edge(X[i], Y[j], label='')

    file_path = os.path.join(output, file_name)
    dot.render(file_path, format='png', view=True, cleanup=True)
    print(f"¡Grafo guardado en '{file_path}.png'!")

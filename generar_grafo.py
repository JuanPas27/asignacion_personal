import graphviz
import os

def hacer_grafo(X, Y, edges, file_name, output="grafos_generados"):
    if not os.path.exists(output):
        os.makedirs(output)
    
    # Definir grafo
    dot = graphviz.Graph('asignación_personal', comment='Grafo bipartita')
    dot.attr(rankdir='LR', label='Grafo bipartita personal-tareas', fontsize='20')
    dot.attr('node', shape='circle')

    # Agrega nodos al grafo
    for x in X:
        dot.node(x, x)
    for y in Y:
        dot.node(y, y)

    # Agrega aristas (conexiones) entre los nodos
    for x, x_A in edges.items():
        for y in x_A:
            dot.edge(x, y, label='')

    # 4. Genera y guarda el grafo
    file_path = os.path.join(output, file_name)
    dot.render(file_path, format='png', view=True, cleanup=True)

    print(f"¡Grafo guardado en '{file_path}.png'!")

def grafo_apareado(X, Y, edges, M, file_name, output="grafos_generados"):
    if not os.path.exists(output):
        os.makedirs(output)
    
    # Definir grafo
    dot = graphviz.Graph('asignación_personal', comment='Apareamiento maximo en grafo bipartita')
    dot.attr(rankdir='LR', label='Asignación de personal-tareas', fontsize='20')
    dot.attr('node', shape='circle')

    # Agrega nodos al grafo
    for x in X:
        dot.node(x, x)
    for y in Y:
        dot.node(y, y)

    # Agrega aristas (conexiones) entre los nodos
    for x, x_A in edges.items():
        for y in x_A:
            if M.get(x) == y or M.get(y) == x:
                dot.edge(x, y, color='red', penwidth='3', label='')
            else:
                dot.edge(x, y, label='')

    # 4. Genera y guarda el grafo
    file_path = os.path.join(output, file_name)
    dot.render(file_path, format='png', view=True, cleanup=True)

    print(f"¡Grafo guardado en '{file_path}.png'!")
from numpy import save
from algorithms import *
import random
from graph import *


# g = gridGraph(6)
# g = erdosRenyiGraph(100, 4500)
# g = dorogovtsevMendesGraph(30)
# g = gilbertGraph(500, p=0.3)
# tree = DFS_R(g, 5)
# saveGraph(tree, g.typee)
# tree = DFS_I(g, 5)
# tree.typee = 8
# saveGraph(tree, g.typee)

# saveGraph(tree, g.typee)

# g = barasiAlbertGraph(30, 4)
g = dorogovtsevMendesGraph(300)
# g = erdosRenyiGraph(30, 330)
print(f"Número de aristas: {len(g.edges)}")
# m = g.createAdjMat()
# print(f"Matriz de adyacencia de dimensión: {m.shape}")
# print(m)
dg = g.Dijkstra(5)
saveGraph(dg, g.typee)

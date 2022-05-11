from graph import Graph
import random
import numpy as np


def gridGraph(m=2, n=0, dirigido=False):
    """
    Grid graph:
    m: number of rows - int
    n: number of columns - int
    dirigido: dirigido? - Boolean

    Create m*n edges and for each node ni,j add edges ni+1,j y ni,j+1
    for i<m and j<n 

    return: edges, nodes
    """
    if n == 0:
        n = m

    g = Graph()
    g.typee = 0
    for i in range(n):
        g.addNode(i)

    for i in range(m):
        for j in range(n):
            cn = i * n + j
            rn = cn + 1
            ln = (i + 1) * n + j
            if i < m-1:
                g.addEdge(cn, ln, f"{cn}->{ln}")
            if j < n-1:
                g.addEdge(cn, rn, f"{cn}->{rn}")

    print("Grid Graph created")
    return g


def erdosRenyiGraph(n, m, dirigido=False, auto=False):
    """
    n: númber of nodes - int
    m: number of edges - int
    dirigido: dirigido? - Boolean
    auto: allow auto cycles - Boolean
    Create an Erdos Renyi graph with different n nodes and m edges 

    return: edges, nodes
    """

    g = Graph()
    g.typee = 1
    for i in range(n):
        g.addNode(i)

    for i in range(m):
        s = random.randint(0, n-1)
        t = random.randint(0, n-1)
        if s != t:
            g.addEdge(s, t, f"{s}->{t}")

    print("Erdos Renyi Graph created")
    return g


def gilbertGraph(n, p=0.5, dirigido=False, auto=False):
    """
    n: number of nodes - int
    p: probability of create edge (0, 1) - float
    dirigido: gdirigido? - Boolean
    auto: allow auto cycles- Boolean
    Create a Gilbert graph with n nodes and edges with
    probability p

    return: edges, nodes
    """

    g = Graph()
    g.typee = 2
    for i in range(n):
        g.addNode(i)

    for i in range(n):
        for j in range(n):
            if i != j:
                if random.random() <= p:
                    g.addEdge(i, j, f"{i}->{j}")

    print("Gilbert Graph Created")
    return g


def geographicGraph(n, r=0.5, dirigido=False, auto=False):
    """
    n: number of nodes - int
    r: max distance allow to create edge (0, 1) - float
    dirigido: dirigido? - Boolean
    auto: allow auto cycles- Boolean
    Create a Geographic graph with n nodes and edges with
    probability p

    return: edges, nodes
    """
    g = Graph()
    g.typee = 3

    for i in range(n):
        g.addNode(i)

    for i in range(n):
        for j in range(n):
            if i != j:
                d = np.linalg.norm(
                    g.nodes[i].attr["N_POS"] - g.nodes[j].attr["N_POS"])
                # print(d)
                if d <= r:
                    g.addEdge(i, j, f"{i}->{j}")
                    # print(d)

    print("Geographic Graph Created")
    return g


def barasiAlbertGraph(n, d, dirigido=False, auto=False):
    """
    n: nunber of nodes (>0) int
    d: maximum node degreee allowed(>1) int
    dirigido: dirigido? boolean
    auto: allow auto cycles boolean

    Place n nodes one by one, asigning to ech one d edges
    to different nodes in order the probability of the new node be 
    connected to a existent node v is proportional to the amount of
    edges in the node v (degree of v) at the moment
    - firts d edges connect each others.
    """
    g = Graph()
    g.typee = 4

    for i in range(n):
        v = np.random.randint(0, i, (1, i))
        # print(v)
        g.addNode(i)
        for k in v[0]:
            # dg = g.nodes[k].attr['DEGREE']
            dg = len(g.nodes[k].attr["NEIGHBORS"])
            # print("grado de nodo:", dg)
            p = 1 - dg / d
            # print(p)
            prob = random.random()
            # print(prob)
            if prob <= p:
                # print("Si creó arista")
                g.addEdge(i, k, f"{i}->{k}")
            # print("################")

    print("Barasi-Albert Graph Created")
    return g


def dorogovtsevMendesGraph(n, dirigido=False):
    """
    n: number of nodes (>=3) int
    dirigido: dirigido? boolean

    Create 3 nodes y 3 edges forming a triangle. After that, 
    to ech aditional node, select an edges randomly
    and create edges between the new node and the ends of 
    the edge selected.
    """
    if n < 3:
        n = 3
    g = Graph()
    g.typee = 5

    for i in range(3):
        g.addNode(i)
    for i in range(3):
        if i < 2:
            g.addEdge(i, i+1, f"{i}->{i+1}")
        else:
            g.addEdge(i, i-2, f"{i}->{i-2}")
    if n != 3:
        for i in range(3, n):
            e = random.choice(g.getEdges())
            t1, t2 = e
            g.addNode(i)
            g.addEdge(i, t1, f"{i}->{t1}")
            g.addEdge(i, t2, f"{i}->{t2}")

    print("Dorogovtsev-Mendes Graph Created")
    return g


def saveGraph(g, t_g=None):
    g_types = ["Grid", "ErdosReyni", "Gilbert", "Geographic", "BarasiAlbert",
               "Dorogovtsev-Mendes", "BFS", "DFS_R", "DFS_I", "Dijkstra", "Manual"]

    if t_g == None:

        with open(f"files gv\{g_types[g.typee]}{len(g.nodes)}graph.gv", mode="w") as file:
            file.write("digraph my_graph {\n")
            file.writelines(
                [f"{int(e)} [label={int(e)}]\n" for e in list(g.nodes.keys())])
            file.writelines(
                [f"{e}\n" for e in g.edges.keys()])
            file.write("}")
            print("Graph saved...")
    else:
        if g.typee == 9:  # dijkstra
            with open(f"files gv\{g_types[g.typee]}{len(g.nodes)}{g_types[t_g]}graph.gv", mode="w") as file:
                file.write("digraph my_graph {\n")
                file.writelines(
                    [f"{int(e)} [label=nodo_{int(e)}({d})]\n" for e, d in zip(list(g.nodes.keys()), g.ds)])
                file.writelines(
                    [f"{e}\n" for e in g.edges.keys()])
                file.write("}")
                print("Graph saved...")
        else:  # bfs, dfs
            with open(f"files gv\{g_types[g.typee]}{len(g.nodes)}{g_types[t_g]}graph.gv", mode="w") as file:
                file.write("digraph my_graph {\n")
                file.writelines(
                    [f"{int(e)} [label={int(e)}]\n" for e in list(g.nodes.keys())])
                file.writelines(
                    [f"{e}\n" for e in g.edges.keys()])
                file.write("}")
                print("Graph saved...")

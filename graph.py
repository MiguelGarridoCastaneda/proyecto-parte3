from edge import Edge
from node import Node
import random
import numpy as np


class Graph:
    def __init__(self):
        self.nodes = {}  # Graph nodes
        self.edges = {}  # Graph edges
        self.typee = None  # Type of graph
        self.attr = {}
        self.ds = []   # Distancias minimas (dijkstra)

    def addNode(self, name):
        """
        Add node to graph.
        :param name: the name of the node
        """
        # First check if node already exists
        n = self.nodes.get(name)

        if n is None:
            n = Node(name)

            self.nodes[name] = n
            # print("se crea nodo", name)
        # else:
        #     print("el nodo ", name, "ya existia")

        return n

    def addEdge(self, s, t, label):
        """
        Add edge to graph.
        :param s: source node
        :param t: target node
        :param label: s->t
        """
        e = self.edges.get(label)

        if e is None:
            n1 = self.addNode(s)
            n2 = self.addNode(t)
            e = Edge(n1, n2, label)

            self.edges[label] = e
            n1.attr["NEIGHBORS"].append(n2)
            n1.attr['EDGES'].append(e)
            n2.attr["NEIGHBORS"].append(n1)
            n2.attr['EDGES'].append(e)

        return e

    def getNodes(self):
        """
        Return list of nodes
        """
        total_nodes = list(self.nodes.keys())
        return total_nodes

    def getEdges(self):
        """
        Return list of edges
        """
        total_edges = [[edge.s.id, edge.t.id] for edge in self.edges.values()]
        return total_edges

    def BFS(self, s):
        """
        Applies BFS algorithm to graph
        s: source node (int)

        return tree (Graph), List of tree layers, label graph (for saving)
        """
        # Se declara el grafo tree
        tree = Graph()
        visited = [False] * len(self.nodes.keys())
        visited[s] = True
        tree.addNode(s)
        tree.typee = 6
        # vectores de capas del árbol
        L = []
        Ls = []
        L.append(s)
        Ls.append([s])

        # Pasar por todos los nodos del grafo
        while L:
            # Se obtienen vecinos del nodo s y se crean aristas si el nodo vecino no ha sido visitado
            s = L.pop(0)
            vecinos = self.nodes[s].attr['NEIGHBORS']
            L_i = []
            for vecino in vecinos:
                if visited[vecino.id] == False:
                    L.append(vecino.id)
                    visited[vecino.id] = True
                    tree.addEdge(s, vecino.id, f"{s}->{vecino.id}")
                    L_i.append(vecino.id)
            # También se guardan las capas del árbol
            if len(L_i) > 0:
                Ls.append(L_i)

        return tree, Ls

    def DFS_UTILS(self, s, tree, visited):
        # Se obtienen vecinos del nodo s
        visited.add(s)
        vecinos = self.nodes[s].attr['NEIGHBORS']
        # random.shuffle(vecinos)
        for vecino in vecinos:
            # si el vecino no ha sido visitado se crea arista y se llama
            # recursivamente función con el vecino como nodo s
            if vecino.id not in visited:
                tree.addEdge(s, vecino.id, f'{s}->{vecino.id}')
                self.DFS_UTILS(vecino.id, tree, visited)
        return tree

    def DFS_R(self, s):
        """
        Applies recursive DFS algorithm to graph
        s: source node (int)

        return tree (Graph)

        """
        # Se declara grafo tree y se llama función dfs recursiva
        tree = Graph()
        visited = set()
        tree.typee = 7
        t = self.DFS_UTILS(s, tree, visited)
        return t

    def DFS_I(self, s):
        """
        Applies iterative DFS algorithm to graph
        s: source node (int)

        return tree (Graph)

        """
        # Se declara grafo tree
        tree = Graph()
        tree.typee = 8
        discovered = [s]
        u = s
        stack = []
        # mientras existan elementos en stack
        while True:
            # se obtienen vecinos de nodo u
            vecinos = self.nodes[u].attr['NEIGHBORS']
            for vecino in vecinos:
                # si el vecino no ha sido visitado se aagrega al stack
                if vecino.id not in discovered:
                    stack.append(vecino.id)

            if not stack:
                break

            # se extrae último elemento del stack
            p, c = u, stack.pop()
            # Si el nodo c no ha sido visitado se crea arista de p a c (p->c)
            # y se marca como visitado.
            if c not in discovered:
                tree.addEdge(p, c, f"{p}->{c}")
                discovered.append(c)
            # se actualiza u = c
            u = c

        return tree

    def addDistances(self, rangeL=2, rangeR=50):
        """
        rangeL: left limit (int). Default 2.
        rangeR: right limit (int). Default 50.
        return distances (list)

        Create a list of random integer numbers for each edge of random graph.
        """
        n_edges = len(self.edges)
        distances = [random.randint(rangeL, rangeR) for _ in range(n_edges)]
        return distances

    def createAdjMat(self):
        """
        return m (numpy 2D-array)
        Creates the adjacent matrix of random graph"""
        distances = self.addDistances()
        n_dis = len(distances)
        n_nodes = len(self.nodes)
        edges = self.edges
        m = np.ones((n_nodes, n_nodes))*np.inf
        c = 0
        for e in edges:
            i = int(e.split("->")[0])
            j = int(e.split("->")[1])
            m[i, j] = distances[c]
            m[j, i] = distances[c]
            c += 1

        for i in range(m.shape[0]):
            for j in range(m.shape[1]):
                if i == j:
                    m[i, j] = 0
        return m

    def Dijkstra(self, s):
        """
        s: source node (int)
        return: dg (Graph)
        Returns Dijkstra tree from random graph"""
        dg = Graph()  # Dijkstra graph
        dg.typee = 9  # id of graph
        mat = self.createAdjMat()  # adjacent matrix mat
        INF = np.inf  # varible with infinite value to represent nodes no neighbors
        distancias = [INF]*mat.shape[0]  # vector de distancias minimas
        visto = [False]*mat.shape[0]  # vector de nodos visitados
        padre = [-1]*mat.shape[0]  # nodos padres
        caminos = [()]*mat.shape[0]  # caminos

        distancias[s] = mat[s][s]  # distance of s to s is 0.

        while sum(visto) < len(visto):
            dismin = INF  # dismin
            v_min = 0  # nodo con distancia minima
            for i in range(len(visto)):
                # se obtiene el nodo de distancia minima
                if visto[i] == False and distancias[i] < dismin:
                    dismin = distancias[i]
                    v_min = i  # nodo de distancia minima

            visto[v_min] = True  # se marca como visto el nodo
            for i in range(len(visto)):  # si L(y) > L(x)+w(x,y)
                if not visto[i] and mat[v_min][i] != 0 and distancias[i] > distancias[v_min] + mat[v_min][i]:
                    # se actualiza nueva distancia mínima
                    distancias[i] = distancias[v_min] + mat[v_min][i]
                    padre[i] = v_min  # se obtiene el nodo padre del nodo i

        # Para obtener los caminos
        for i in range(len(padre)):
            nodo = i  # nodo final
            c = []
            while nodo != -1:  # hasta que se llegue al nodo inicio
                c.append(nodo)  # se guarda el nodo
                nodo = padre[nodo]  # y se mueve al nodo predecesor
            caminos[i] = c[::-1]

        # Agregar edges al grafo dg (Graph)
        for camino in caminos:
            if len(camino) > 1:
                p = 0
                while p < len(camino)-1:
                    dg.addEdge(camino[p], camino[p+1],
                               f"{camino[p]}->{camino[p+1]}")
                    p += 1

        # Se crea lista orden para pasar las distancias de cada nodo a s en gephi
        orden = []
        for camino in caminos:
            for r in camino:
                if r not in orden:
                    orden.append(r)

        # Se agregan las distancias a dg (Graph)
        for r in orden:
            dg.ds.append(distancias[r])

        return dg

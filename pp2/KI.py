import math
import heapq

class Node():
    def __init__(self, i):
        self.key = float('Inf')
        self.name = int(i)
        self.parrent = None




class KI(object):

    def __init__(self,n):
        self.n = n
        self.nnodes = n**2 +1
        self.nodes = [Node(i) for i in range(self.nnodes)]
        # Start Knoten
        self.root = 0
        self.nodes[self.root].key = 0
        #self.nodes[0].key = 0
        self.adj_list = self.__init_adj_list()
        #self.heap = MinHeap(self.nodes)
        self.heap = []
        for node in self.nodes:
            heapq.heappush(self.heap,node)
        bla = 1

    def calculateMove(self):

        tmp_adj = self.adj_list
        # fuer Knoten in Adjaliste
        for i in range(1,len(tmp_adj)):
            # fuer verbindung in Knoten liste
            for j in range(len(tmp_adj[i])) :
                tup = tmp_adj[i][j]
                tmp_adj[i][j] = (tmp_adj[i][j][0], 0)
                a = self.max_value(tmp_adj, -float("inf"), float("inf"), 2)
                tmp_adj[i][j] = tup
                # if a > maxi:
                #     maxi = a
                #     self.best_move = s
    def value(self,adj):
        self.shortest_path_potentials(adj)
        mini = 1000
        for i in range(self.n**2-self.n+1, self.n**2+1):
            mini = min(mini,self.nodes[i].key)
        return mini



    def max_value(self, tmp_adj , a, b, depth):

        if (depth == 0):
            return self.value(tmp_adj)
        # goes through all possible moves
        for i in range(1,len(tmp_adj)):
            # fuer verbindung in Knoten liste
            for j in range(len(tmp_adj[i])) :
                tup = tmp_adj[i][j]
                tmp_adj[i][j] = (tmp_adj[i][j][0], 0)
                a = max(a, self.min_value(tmp_adj,a,b,depth-1))
                tmp_adj[i][j] = tup

            # this ia a cutoff point
            if a >= b:
                return a

            return a

    def min_value(self, tmp_adj, a, b, depth):
        if (depth == 0):
            return self.value(my_moves,other_moves)

        for i in range(1,len(tmp_adj)):
            # fuer verbindung in Knoten liste
            for j in range(len(tmp_adj[i])) :
                tup = tmp_adj[i][j]
                tmp_adj[i][j] = (tmp_adj[i][j][0], 0)
                b = min(b, self.max_value(tmp_adj, a, b, depth - 1))
                tmp_adj[i][j] = tup

            # this is a cutoff point
            if b <= a:
                return b
            return b






    def __init_adj_list(self):
        adj_list = {}
        # Start Knoten
        for v in range(1,self.n +1):
            (adj_list.setdefault(0, [])).append((v, 0))
        # End Knoten
        for v in range(self.n**2 - self.n +1,self.n**2 +1):
            (adj_list.setdefault(self.n ** 2 + 1, [])).append((v, 0))

        # erste Reihe
        for v in range(1, self.n + 1):
            # linker Rand
            if not v % self.n == 0:
                (adj_list.setdefault(v, [])).append((v+1, 1))
            (adj_list.setdefault(v, [])).append((v + self.n, 1))

            # rechter Rand
            if not v % self.n == 1:
                (adj_list.setdefault(v, [])).append((v - 1, 1))
                (adj_list.setdefault(v, [])).append((v + self.n - 1, 1))
        # letzte Reihe
        for v in range(self.n**2-self.n + 1, self.n**2 + 1):
            # linker Rand
            if not v % self.n == 0:
                #(adj_list.setdefault(v, [])).append((v - self.n, 1))
                (adj_list.setdefault(v, [])).append((v + 1, 1))
                (adj_list.setdefault(v, [])).append((v - self.n+1, 1))
            # rechter Rand
            if not v % self.n == 1:
                (adj_list.setdefault(v, [])).append((v - 1, 1))
            (adj_list.setdefault(v, [])).append((v - self.n, 1))

        # zwischen Reihen
        for v in range(self.n+1 , self.n**2-self.n + 1 ):
            # Randknoten muessen anders behandelt werden
            # Wenn am rechten Rand, kein rechter Nachbar
            if not v % self.n == 0:
                (adj_list.setdefault(v, [])).append((v+1, 1))
                (adj_list.setdefault(v, [])).append((v - self.n + 1, 1))
            # Wenn am linkten Rand, kein linker nachbar und kein linker unterer Nachbar
            if not v % self.n == 1:
                (adj_list.setdefault(v, [])).append((v - 1, 1))
                (adj_list.setdefault(v, [])).append((v + self.n - 1, 1))

             # untere Nachbar
            #(adj_list.setdefault(v, [])).append((v + self.n, 1))
            (adj_list.setdefault(v, [])).append((v - self.n, 1))
            (adj_list.setdefault(v, [])).append((v + self.n, 1))
        return adj_list

    def shortest_path_potentials(self, adj_list):
        while not len(self.heap) == 0:
            u = heapq.heappop(self.heap).name

            for v, w in adj_list[u]:
                print(v,u)
                if self.nodes[v].key > self.nodes[u].key + w:
                    #self.heap.decreaseKey(self.nodes[v], self.nodes[u].key + w)
                    self.nodes[v].key = self.nodes[u].key + w
                    heapq.heapify(self.heap)
                    self.nodes[v].parent = self.nodes[u]
                    ass = ' '.join(str(n.key) for n in self.nodes)
        #return a

#    def __str__(self):
 #       self.shortest_path_potentials(self.adj_list)
  #      return ' '.join(str(n.key) for n in self.nodes)


K = KI(3)

K.calculateMove()
#print (K)
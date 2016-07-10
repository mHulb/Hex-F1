import math
import heapq

class Node():
    def __init__(self, i):
        self.key = float('Inf')
        self.name = int(i)
        self.parrent = None


class MinHeap():
    def __init__(self, nodes):
        self.knoten = nodes[:]
        # build-heap
        # print("Knoten Ursprung")
        # for k in nodes:
        #    print(k.name, k.key, end="  ")
        # print()
        # print("Heap aufbauen:")
        for i in reversed(range(0, int(len(self.knoten) / 2 + 1))):
            #    print("grad fuer", i)
            self.minHeapify(self.knoten, i)
            # print("HEAP FERTIG!")
            # for k in self.knoten:
            #    print(k.name, k.key, end="    ")
            # print()

    def minHeapify(self, array, i):
        # print("Heapify")
        left = 2 * i + 1
        right = 2 * i + 2
        n = len(array) - 1
        # print("vor aenderung:")
        # for k in array:
        #    print(k.name, k.key, end="    ")
        # print()
        # print("links:", left, "rechts:", right, "i:", i)
        if left <= n and array[left].key < array[i].key:
            # print("Bed 1")
            smallest = left
        else:
            # print("Bed 2")
            smallest = i
        if right <= n and array[right].key < array[smallest].key:
            # print("Bed 3")
            smallest = right
        if not (smallest == i):
            placeholder = array[i]
            array[i] = array[smallest]
            array[smallest] = placeholder
            self.minHeapify(array, smallest)

    def isEmpty(self):
        return (len(self.knoten) == 0)

    def extractMin(self):
        vorn = self.knoten[0]
        if len(self.knoten) > 1:
            self.knoten[0] = self.knoten[len(self.knoten) - 1]
        self.knoten.pop()
        self.minHeapify(self.knoten, 0)
        # print("Laenge:", len(self.knoten))
        return (vorn)

    def decreaseKey(self, knotenV, wert):
        knotenV.key = wert
        # self.minHeapify(self.knoten, 0)
        for i in reversed(range(0, int(knotenV.name / 2 + 1))):
            #    print("grad fuer", i)
            self.minHeapify(self.knoten, i)
        return (None)


class KI(object):

    def __init__(self,n):
        self.n = n
        self.nnodes = n**2 +2
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
        val = self.shortest_path_potentials(adj)

        return val



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
        return ' '.join(str(n.key) for n in self.nodes)


#    def __str__(self):
 #       self.shortest_path_potentials(self.adj_list)
  #      return ' '.join(str(n.key) for n in self.nodes)


K = KI(3)

K.calculateMove()
#print (K)
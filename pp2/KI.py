import math
class Node():
    def __init__(self, i):
        self.key = float('Inf')
        self.name = int(i)
        self.parrent = None

class MinHeap():
    def __init__(self, nodes_list):
        self.heaps = nodes_list[:]
        self.n = len(self.heaps) - 1
        self.build_max_heap()

    def build_max_heap(self):
        n = self.n

        for i in range(int(math.floor(n / 2) + 1), 0, -1):
            self.Min_Heapify(i)
            # self.Min_Heapify(0)

    def extractMin(self):
        # self.Min_Heapify(1)
        # print(' '.join(str(n)+' '+str(self.heaps[n].key) for n in range(len(self.heaps))))
        self.heaps[0], self.heaps[len(self.heaps) - 1] = self.heaps[len(self.heaps) - 1], self.heaps[0]
        back = self.heaps.pop()
        self.Min_Heapify(1)
        return back

    def isEmpty(self):
        if len(self.heaps) == 0:
            return True
        else:
            return False

    def decreaseKey(self, node_v, key):
        node_v.key = key
        self.build_max_heap()

    def Min_Heapify(self, i):
        l = i * 2 - 1
        r = i * 2
        i -= 1
        n = len(self.heaps)
        # wenn nur 1 Element vorhanden, muss man nicht Heapifyen
        # print(n,l,r,i)
        # print(self.heaps[l].key)
        # print(self.heaps[i].key)
        if not n == 1:
            if l < n and self.heaps[l].key < self.heaps[i].key:
                smallest = l
            else:
                smallest = i

            if r < n and self.heaps[r].key < self.heaps[smallest].key:
                smallest = r

            if not smallest == i:
                self.heaps[smallest], self.heaps[i] = self.heaps[i], self.heaps[smallest]
                self.Min_Heapify(smallest + 1)

                # print(' '.join(str(n)+' '+str(self.heaps[n].key) for n in range(len(self.heaps))))



class KI(object):

    def __init__(self,n):
        self.n = n
        self.nnodes = n**2 +2
        self.nodes = [Node(i) for i in range(self.nnodes)]
        # Start Knoten
        self.nodes[0].key = 0
        self.adj_list =  self.__init_adj_list()
        self.heap = MinHeap(self.nodes)

    def __init_adj_list(self):
        adj_list = {}
        # Start Knoten
        for v in range(1,self.n +1):
            (adj_list.setdefault(0, [])).append((v, 0))
        # End Knoten
        for v in range(self.n**2 - self.n ,self.n**2 +1):
            (adj_list.setdefault(self.n ** 2 + 1, [])).append((v, 0))

        for v in range(1,self.n**2 +1 ):
            # Randknoten muessen anders behandelt werden
            # Wenn am rechten Rand, kein rechter Nachbar
            if not v % self.n == 0:
                (adj_list.setdefault(v, [])).append((v+1, 1))
            # Vll nicht noetig den linken Nachbarn nochmal durch zu gehen
            (adj_list.setdefault(v, [])).append((v + self.n, 1))

            # Wenn am linkten Rand, kein linker nachbar und kein linker unterer Nachbar
            if not v % self.n == 1:
                (adj_list.setdefault(v, [])).append((v + self.n - 1, 1))
                (adj_list.setdefault(v, [])).append((v - 1, 1))
            # erste Reihe hat keine oberen Nachbarn
            if v > self.n:
                (adj_list.setdefault(v, [])).append((v - self.n +1, 1))
                (adj_list.setdefault(v, [])).append((v - self.n, 1))
        return adj_list

    def shortest_path_potentials(self):
        while not self.heap.isEmpty():
            u = self.heap.extractMin().name
            print(u)
            for v, w in self.adj_list[u]:
                if self.nodes[v].key > self.nodes[u].key + w:
                    self.heap.decreaseKey(self.nodes[v], self.nodes[u].key + w)
                    self.nodes[v].parent = self.nodes[u]


    def __str__(self):
        self.shortest_path_potentials()
        return ' '.join(str(n.key) for n in self.nodes)


K = KI(4)
print (K)
from helpers import AINode, Edge, Dijkstra
import random


class HexKI:
    """
    HexKI: Implements an AI opponent.
    """

    def __init__(self, m, n):
        """
        """
        self.m = m  # number of rows
        self.n = n  # number of columns
        self.depth = 2
        self.first_move = 1
        self.nodes = [[AINode(i, j) for j in range(m)] for i in range(n)]
        # boundary nodes have no indices, but a predefined colour (1 or 2)
        self.boundaries = {1: [AINode(None, None, 1), AINode(None, None, 1)],
                           2: [AINode(None, None, 2), AINode(None, None, 2)]}
        for _, nodes in self.boundaries.items():
            for node in nodes:
                node.update_resistances()

        self.__initialize_nodes(m, n)
        self.edges = self.__make_edges()
        self.best_move = None
        self.player_colour = None
        self.opponent_colour = None

    def __make_edges(self):
        edges = [] # logisch gesehen waere ein set wohl sinnvoller
        for row in self.nodes:
            for node in row:
                for neighbour in node.neighbours:
                    # resistance default value is 2 for both sides
                    new_edge = Edge(node, neighbour)
                    if not new_edge in edges:
                        edges.append(new_edge)

                        # add edge to both nodes
                        node.adjacent_edges.append(new_edge)
                        neighbour.adjacent_edges.append(new_edge)

        for edge in edges:
            edge.update_resistances()
        return edges


    def __initialize_nodes(self, m, n):
        # initializing the basic board nodes
        for i, row in enumerate(self.nodes):
            for j, node in enumerate(row):
                if i > 0:
                    node.neighbours.append(self.nodes[i - 1][j])
                if j > 0:
                    node.neighbours.append(self.nodes[i][j - 1])
                if i < n - 1:
                    node.neighbours.append(self.nodes[i + 1][j])
                if j < m - 1:
                    node.neighbours.append(self.nodes[i][j + 1])
                if i < n - 1 and j > 0:
                    node.neighbours.append(self.nodes[i + 1][j - 1])
                if i > 0 and j < m - 1:
                    node.neighbours.append(self.nodes[i - 1][j + 1])

        # initializing the boundary nodes
        upper_bound = self.boundaries[1][0]
        lower_bound = self.boundaries[1][1]
        for node in self.nodes[0]: # upper side
            node.neighbours.append(upper_bound)
            upper_bound.neighbours.append(node)
        for node in self.nodes[n - 1]: # lower side
            node.neighbours.append(lower_bound)
            lower_bound.neighbours.append(node)

        left_bound = self.boundaries[2][0]
        right_bound = self.boundaries[2][1]
        for row in self.nodes:
            # leftmost side
            row[0].neighbours.append(left_bound)
            left_bound.neighbours.append(row[0])
            # rightmost side
            row[self.m - 1].neighbours.append(right_bound)
            right_bound.neighbours.append(row[self.m - 1])

    def chooseOrder(self, firstmove):
        """
        """
        pass

    def calculateMove(self):
        """
        """
        
        # Kann spaeter geloescht werden, ist nur zum print da
        show_board = [["#" for i in range(self.n)] for j in range(self.m)]
        # Minimum fuer a intialisieren
        self.mini = 1000
        mo = {}
        nodes = self.nodes


        # Nachfolgende ist zum Speichern der besten moves gedacht
        # Wenn man mit besseren moves anfängt, spart man sich angeblich zeit

        # Beim ersten Zug werden nur das mitlere quadrat durchsucht
        # muss noch angepasst werden mit swap später
        if self.first_move == 1:
            self.moves = {}
            # noch in list comprehension
            for i in range(1, self.n - 1):
                for j in range(1,self.m-1):
                    (self.moves.setdefault(1, [])).append((i, j))

            self.first_move += 1

        # Beim zweiten move werden alle fehlenden moves hinzugefuegt
        elif self.first_move == 2:
            for i in range(self.n):
                for j in range(self.m):
                    if i not in range(1, self.n-1) or not j in range(1,self.m-1):
                        (self.moves.setdefault(1, [])).append((i, j))
            self.first_move += 1

        # Sortiere Moves nach a wert, so das er mit dem kleinsten a
        # beginnt(kleines a -> guter move)
        for val in sorted(self.moves):
            if val == 0 and len(self.moves[val]) > 1:
                moves = [self.moves[val]]
            else:
                moves = self.moves

            for move in moves[val]:
                if nodes[move[0]][move[1]].colour == 0:
                    # Zum probieren des jeweiligen moves muss die Farbe geändert werden
                    # Daher tmporere nodes
                    nodes[move[0]][move[1]].change_colour(self.player_colour)
                    # theoretisch muesste hier min_value aufgerufen werden
                    a = self.min_value(nodes, -float("inf"), float("inf"), self.depth)
                    # wieder zurueck setzten, damit es beim naechsten move nicht
                    # stoert
                    nodes[move[0]][move[1]].change_colour(0)
                    nodes[move[0]][move[1]].pot = 1

                    # Moves für die naechste Runde abspeichern
                    (mo.setdefault(a, [])).append((move[0], move[1]))

                    show_board[move[0]][move[1]] = round(a,3)
                    if a < self.mini:
                        self.mini = a
                        self.best_move = move
        self.moves = mo
        # Ausgabe der a Werte in Matrixform
        print(' \n'.join('       '.join(str(a) for a in row) for row in show_board))

        return True

    def evaluate(self, nodes=None):
        """
        Evaluates a board
        """
        if not nodes:
            nodes = self.nodes
        #if not edges:
        #    edges = self.edges
        start_node = self.boundaries[self.player_colour][0]
        end_node = self.boundaries[self.player_colour][1]
        # Evaluate board with Dijkstra's algorithm.
        board_eval_1 = Dijkstra(nodes, start_node, end_node)
        value_1 = board_eval_1.value

        start_node = self.boundaries[self.opponent_colour][0]
        end_node = self.boundaries[self.opponent_colour][1]
        board_eval_2 = Dijkstra(nodes, start_node, end_node)
        value_2 = board_eval_2.value
        if value_1 == 0:
            self.depth = 1
            return 0
        elif value_2 == 0:
            return float("inf")
        return value_1 / value_2

    def nextMove(self):
        """
        """
        self.nodes[self.best_move[0]][self.best_move[1]].change_colour(self.player_colour)

        for row in self.nodes:
            print(' '.join(str(node) for node in row)),


        return self.best_move

    def receiveMove(self, move):
        """
        """
        self.nodes[move[0]][move[1]].change_colour(self.opponent_colour)


    def readBoard(self, board, current=True):
        """
        """
        for i, row in enumerate(board):
            for j, player_num in enumerate(row):
                self.board[i][j].colour = player_num

    def random_move(self):
        while True:
            i = random.randint(0, self.m-1)
            j = random.randint(0, self.n-1)

            if self.nodes[i][j].colour == 0:
                return (i, j)

    def max_value(self, nodes, a, b, depth):

        if (depth == 0):
            return self.evaluate(nodes)
        #moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        #for move in moves:
        for val in sorted(self.moves):
            for move in self.moves[val]:
                if nodes[move[0]][move[1]].colour == 0:
                    nodes[move[0]][move[1]].change_colour(self.player_colour)


                    a = max(a, self.min_value(nodes, a, b, depth - 1))

                    nodes[move[0]][move[1]].change_colour(0)
                    nodes[move[0]][move[1]].pot = 1


        # this ia a cutoff point
        #if a <= b:
        #     return a
        return a

    def min_value(self, nodes, a, b, depth):
        if (depth == 0):
            return self.evaluate(nodes)
        #moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        #for move in moves:
        for val in sorted(self.moves):
            for move in self.moves[val]:
                if nodes[move[0]][move[1]].colour == 0:
                    nodes[move[0]][move[1]].change_colour(self.opponent_colour)

                    b = min(b, self.max_value(nodes, a, b, depth - 1))
                    nodes[move[0]][move[1]].change_colour(0)
                    nodes[move[0]][move[1]].pot = 1


        # this is a cutoff point
        #if b <= a:
        #    return b
        return b


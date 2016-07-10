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
        nodes = self.nodes
        edges = self.edges
        moves = [(i,j) for i in range(self.n) for j in range(self.m)]
        maxi = -1
        for move in moves:
            if nodes[move[0]][move[1]].colour == 0:
                nodes[move[0]][move[1]].change_colour(self.player_colour)
                a = self.max_value(nodes,edges,-float("inf"),float("inf"),3)
                nodes[move[0]][move[1]].change_colour(0)
                nodes[move[0]][move[1]].pot = 1

                if a > maxi:
                    maxi = a
                    self.best_move = move


        #self.best_move = self.__random_move()
        return True

    def evaluate(self, nodes=None, edges=None):
        """
        Evaluates a board
        """
        if not nodes:
            nodes = self.nodes
        if not edges:
            edges = self.edges

        start_node = self.boundaries[self.player_colour][0]
        end_node = self.boundaries[self.player_colour][1]
        # erstmal mit dijkstra versuchen
        shortest_length = Dijkstra(nodes, edges, start_node, end_node)
        return shortest_length.value

    def nextMove(self):
        """
        """
        self.nodes[self.best_move[0]][self.best_move[1]].colour = self.player_colour
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

    def __random_move(self):
        while True:
            i = random.randint(0, self.m)
            j = random.randint(0, self.n)

            if self.board[i][j].colour == 0:
                return (i, j)

    def max_value(self, nodes, edges , a, b, depth):

        if (depth == 0):
            return self.evaluate(nodes,edges)
        moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        for move in moves:
            if nodes[move[0]][move[1]].colour == 0:
                nodes[move[0]][move[1]].change_colour(self.player_colour)
                a = max(a, self.min_value(nodes, edges, a, b, depth - 1))
                nodes[move[0]][move[1]].change_colour(0)
                nodes[move[0]][move[1]].pot = 1

        # this ia a cutoff point
        if a >= b:
             return a
        return a

    def min_value(self, nodes, edges , a, b, depth):
        if (depth == 0):
            return self.evaluate(nodes,edges)
        moves = [(i, j) for i in range(self.n) for j in range(self.m)]
        for move in moves:
            if nodes[move[0]][move[1]].colour == 0:
                nodes[move[0]][move[1]].change_colour(self.player_colour)
                b = min(b, self.max_value(nodes, edges, a, b, depth - 1))
                nodes[move[0]][move[1]].change_colour(0)
                nodes[move[0]][move[1]].pot = 1

        # this is a cutoff point
        if b <= a:
            return b
        return b
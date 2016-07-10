from helpers import AINode, Edge
import random


class HexKI:
    """
    HexKI: Implements an AI opponent.
    """

    def __init__(self, m, n):
        """
        """
        self.nodes = [[AINode(i, j) for j in range(m)] for i in range(n)]
        self.__initialize_nodes(m, n)
        self.edges = self.__make_edges(self.nodes)
        self.m = m  # number of rows
        self.n = n  # number of columns
        self.best_move = None
        self.player_colour = None
        self.opponent_colour = None

    def __make_edges(self, nodes):
        edges = [] # logisch gesehen wäre ein set wohl sinnvoller
        for row in nodes:
            for node in row:
                for neighbour in node.neighbours:
                    # resistance default 2 for both sides
                    new_edge = Edge(node, neighbour)
                    if not new_edge in edges:
                        edges.append(new_edge)

                        # das hier evtl unnötig, später gucken
                        node.adjacent_edges.append(new_edge)
                        neighbour.adjacent_edges.append(new_edge)
        return edges

    def __initialize_nodes(self, m, n):
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

    def chooseOrder(self, firstmove):
        """
        """
        pass

    def calculateMove(self):
        """
        """
        self.best_move = self.__random_move()
        return True

    def evaluate(self, nodes=None, edges=None):
        """
        Evaluates a board
        """
        if not nodes:
            nodes = self.nodes
        if not edges:
            edges = self.edges

        """
        !!! Hier eigentlich später nur nach jedem neuen zug das neueste updaten
        anstatt alle edges neu zu berechnen.
        """
        for edge in edges:
            edge.update_resistances()
        

    def nextMove(self):
        """
        """

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
            i = random.randint(0, self.size[0])
            j = random.randint(0, self.size[1])

            if self.board[i][j].colour == 0:
                return (i, j)

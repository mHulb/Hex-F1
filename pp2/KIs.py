
class KI(object):
    '''
    small_fields KI: This KI looks for the winning Strategie for small fields
    '''
    def __init__(self,n):
        self.my_moves = []
        self.other_moves = []
        self.n = n
        self.best_move = None
        # save all posible moves, so we dont have to calculate them every move
        self.all_moves = set([(i,j) for i in range(n) for j in range(n) ])
        print(self.all_moves)

    def chooseOrder(self, firstmove):
        """
        """
        pass

    def calculateMove(self):
        """
        """

        return True


    def nextMove(self):
        """
        returns the best move which was calculated by calculateMove
        """
        self.my_moves.append(self.best_move)
        self.all_moves.difference(set([self.best_move]))
        return self.best_move


    def receiveMove(self, move):
        """
        """
        self.other_moves.append(move)
        self.all_moves.difference(set([move]))


    def readBoard(self, board, current=True):
        """
        Reads a given board. Updates the own moves, other_moves
        and all possible moves
        """
        self.my_moves = []
        self.other_moves = []
        for i in range(board):
            for j in range(board[0]):
                if board[i][j] == 1:
                    self.my_moves.append((i,j))
                elif board[i][j] == 2:
                    self.other_moves.append((i,j))
        self.all_moves.difference(set(self.my_moves))
        self.all_moves.difference(set(self.other_moves))



    def __random_move(self):
        while True:
            i = random.randint(0,self.size[0])
            j = random.randint(0,self.size[1])

            if self.board[i][j].colour == 0:
                return (i , j)

    def max_value(self, my_moves,other_moves, a, b, depth):

        if (depth == 0):
            return self.value(my_moves,other_moves)
        all_moves = self.all_moves.copy()
        all_moves = all_moves.difference(set(my_moves))
        all_moves = all_moves.difference(set(other_moves))
        # gos through all possible moves
        for s in all_moves:
            tmp_state = my_moves[:]
            tmp_state.append(s)
            a = max(a, self.min_value(tmp_state, other_moves, a, b, depth - 1))
        # this ia a cutoff point
        if a >= b:
            return a

        return a

    def min_value(self, my_moves,other_moves, a, b, depth):
        if (depth == 0):
            return self.value(other_moves,my_moves)
        all_moves = self.all_moves.copy()
        all_moves = all_moves.difference(set(my_moves))
        all_moves = all_moves.difference(set(other_moves))
        # gos through all possible move
        for s in all_moves:
            tmp_state = other_moves[:]
            tmp_state.append(s)
            b = min(b, self.max_value(my_moves,tmp_state, a, b, depth - 1))
        # this is a cutoff point
        if b <= a:
            return b
        return b

    def value(self, my, othter):
        return 1



test = KI(3)
test.max_value(test.my_moves,test.other_moves,float("-inf"),float("inf"),4)
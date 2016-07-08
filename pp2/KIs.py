
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
        self.all_moves = set([(i,j) for i in range(n) for j in range(n)])


    def chooseOrder(self, firstmove):
        """
        """
        pass

    def calculateMove(self):
        """
        """
        maxi = 0

        for s in self.all_moves:
            tmp_state = self.my_moves[:]
            tmp_state.append(s)
            a = self.max_value(tmp_state,self.other_moves,-float("inf"),float("inf"),3)
            if a > maxi:
                maxi = a
                self.best_move = s
        return True


    def nextMove(self):
        """
        returns the best move which was calculated by calculateMove
        """
        self.my_moves.append(self.best_move)
        self.all_moves = self.all_moves.difference(set(self.my_moves))
        return self.best_move


    def receiveMove(self, move):
        """
        Bekommt move und packt ihn direkt in ZHK
        """
        self.other_moves.append(move)

    def is_nachbar(self,move,ZHK):
        # ZHK [(1,1),(2,1),(1,3)]
        for el in ZHK:
            if move[0] in range(el[0]-1,el[0]+2) and move[1] in range(el[1]-1,el[1]+2):
                return True
        return False

    def is_bridg(self, mo, brid,other):
        """
        :param mo: move (x,y)
        :param brid: is a list withe tuples
        :param other: is from type [] with tuples in the second list
        :return: True/False
        Prueft ob move punkt eine Bruecke bildet
        """

        # ist in richtiger Reihenfolge
        bridges = [(mo[0]-2,mo[1]+1),(mo[0]-1,mo[1]+2),(mo[0]+1,mo[1]+1),(mo[0]+2,mo[1]-1),(mo[0]+1,mo[1]-2),(mo[0]-1,mo[1]-1)]

        # ist in richtiger Reihenfolge
        blockers = [(mo[0] - 1, mo[1]),(mo[0] - 1, mo[1] + 1),(mo[0], mo[1] + 1),(mo[0] + 1, mo[1]),(mo[0] + 1, mo[1] - 1),(mo[0], mo[1] - 1),(mo[0] - 1, mo[1])]

        for i,el in enumerate(bridges):
            # wenn bridg punkt in sub-graph schau ob geblockt
            if el in brid:
                # gehe subraphen von others durch
                if not blockers[i] in other or blockers[i+1] in other:
                    return True
        return False

    def max_value(self, my_moves,other_moves, a, b, depth):

        if (depth == 0):
            return self.value(my_moves,other_moves)
        # da wir nichts ande den self.variablen aender wollen, Suche nur in tmp variablen
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

    def value(self,my,ot):
        # laengste zusammenhangs komponente
        # kann man was blocken
        # ist es bruecke
        # liegt es nahe an mittellinie
        # lets try what happens
        l = self.ZHK(my)
        b = self.bridge_count(my,ot)
        w1,w2 = 4,1
        val = w1*l + w2*b
        return val

    def ZHK(self,tupls):
        zhk = []
        indis = []
        l = range(len(tupls))
        while len(tupls)>0:
            t = [tupls.pop()]
            for i in t:
                for ko in tupls:
                    if self.is_nachbar(ko,t):
                        s = tupls.pop()
                        t.append(s)
            zhk.append(t)
        l = 0

        for el in zhk:
            l = max(l,len(el))
        return l

    def bridge_count(self,my,ot):
        l = len(my)
        count = 0
        for i in range(l):
            t = my.pop()
            if self.is_bridg(t,my,ot) == True:
                count +=1
        return count


a = KI(5)

a.receiveMove((3,3))
a.best_move = (2,2)
a.nextMove()
a.receiveMove((4,3))
a.calculateMove()
a.nextMove()
a.receiveMove((5,1))
a.calculateMove()
a.nextMove()
a.receiveMove((3,1))
a.calculateMove()
a.nextMove()
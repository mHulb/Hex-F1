import time
import random


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
        maxi = -1
        # bei all moves kann man vll noch etwas aussieben. Gerade die Spitzen
        # other_moves durch gehen und schauen ob eins der toten muster drin ist
        # wenn ja dann loesche die freien felder, dann werden sie nie mit durchsucht!
        n = self.n
        if len(self.my_moves) == 0:
            all_moves = set([(i,j) for i in range(1,n-1) for j in range(1,n-1)])
        else:
            all_moves = self.all_moves

        for s in all_moves:
            tmp_state = self.my_moves[:]
            tmp_state.append(s)
            a = self.max_value(tmp_state,self.other_moves,-float("inf"),float("inf"),4)
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
        o = self.on_the_line(my)
        #print (l,b,o)
        w1,w2,w3 = 10,1,7
        val = w1*l + w2*b + w3*o
        return val

    def on_the_line(self,my):
        """
        how close is it to se midle line
        :param my: list with own moves
        :return: int value
        """
        all = []
        mean = 0
        for elm in my:
            su = elm[0] + elm[1]
            all.append(abs(self.n-1 - su))
        if len(all)>0:
            mean = sum(all)/len(all)
            return 10 - mean
        else:
            return 1
        #     all.append(su)
        # if len(all) > 0:
        #     mean = sum(all)/len(my)*1.
        # if mean == self.n:
        #     return 1
        # else:
        #     return ((abs(self.n-1 - mean)+1))


    def ZHK(self,my):
        tupls = my[:]
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
        wining = 0
        for el in zhk:
            for tup in el:
                if tup[1] == 0:
                    wining += 1
                if tup[1] == self.n-1:
                    wining += 1
            if wining == 2:
                return 100

        for el in zhk:
            l = max(l,len(el))
        return l

    def bridge_count(self,my_in,ot_in):
        my = my_in[:]
        ot = ot_in[:]
        l = len(my)
        count = 0
        for i in range(l):
            t = my.pop()
            if self.is_bridg(t,my,ot) == True:
                count +=1
        return count

    def random_move(self):
        while True:
            i = random.randint(0,self.n)
            j = random.randint(0,self.n)

            if (i,j) in self.all_moves:
                return (i,j)



def prin(my,ot,n):
    board = [[0 for i in range(n)] for j in range(n)]
    for el in my:
        board[el[0]][el[1]] = 1
    for el in ot:
        board[el[0]][el[1]] = 2
    output = ""
    for i, row in enumerate(board):
        output += i * " " + " ".join(str(el) for el in row) + "\n"
    print (output)


a = KI(4)
a.best_move = (2,1)
a.nextMove()
for k in range(7):
    a.receiveMove(a.random_move())
    t0 = time.clock()
    a.calculateMove()
    print(time.clock() -t0)
    a.nextMove()
    prin(a.my_moves,a.other_moves,4)
prin(a.my_moves,a.other_moves,4)

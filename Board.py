from copy import deepcopy

class Board:

    def __init__(self,mode,other=None):
        self.player = 'X'
        self.opponent = 'O'
        self.empty = ' '
        self.size = 3
        self.fields = {}
        self.mode = mode
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x,y] = self.empty

        #if (AI == True):        #finish this up

        # copy constructor
        if (other):
            self.__dict__ = deepcopy(other.__dict__)

    def move(self,x,y):
        board = Board(self.mode,self)
        board.fields[x,y] = board.player
        (board.player,board.opponent) = (board.opponent,board.player)
        return board

    def minimax(self, player):
        if (self.won()):
            if (player):
                return(-1,None)
            else:
                return (+1,None)
        elif (self.tied()):
            return (0,None)
        elif player:
            best = (-2,None)
            for x,y in self.fields:
                if self.fields[x,y] == self.empty:
                    value = self.move(x,y).minimax(not player)[0]
                    if (value > best[0]):
                        best = (value,(x,y))
            return best
        else:
            best = (+2,None)
            for x,y in self.fields:
                if (self.fields[x,y] == self.empty):
                    value = self.move(x,y).minimax(not player)[0]
                    if (value < best[0]):
                        best = (value,(x,y))
            return best

    def bestMove(self):
        return self.minimax(True)[1]

    def tied(self):
        for (x,y) in self.fields:
            if self.fields[x,y]==self.empty:
                return False
        return True

    def won(self):
        #horiz
        for y in xrange(self.size):
            winning = []
            for x in xrange(self.size):
                if self.fields[x,y] == self.opponent:
                    winning.append((x,y))
            if (len(winning) == self.size):
                return winning

        #verticle
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.fields[x,y] == self.opponent:
                    winning.append((x,y))
            if len(winning) == self.size:
                return winning

        # diagonal
        winning = []
        for y in range(self.size):
            x = y
            if self.fields[x,y] == self.opponent:
                winning.append((x,y))
        if len(winning) == self.size:
            return winning

        # other diagonal
        winning = []
        for y in range(self.size):
            x = self.size-1-y
            if self.fields[x,y] == self.opponent:
                winning.append((x,y))
        if len(winning) == self.size:
            return winning

        # default
        return None


    def __str__(self):
        string = ''
        for y in range(self.size):
            for x in range(self.size):
                string+=self.fields[x,y]
            string+="\n"
        return string



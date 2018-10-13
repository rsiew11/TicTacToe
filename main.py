from Tkinter import Tk, Button
from tkFont import Font
from Board import Board

class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=100)
        self.board = Board("ai")
        self.buttons = {}
        self.backBtn = None

        #menu stuff
        self.mode=""
        self.aiBtn=None
        self.hostBtn=None
        self.joinBtn=None
        #self.board_img = self.app.PhotoImage("./TicTacToe.gif")
        #self.menu_img = tk.PhotoImage("./")

        self.menuScreen()
        #self.createGrid()

    def menuScreen(self):
        w = 50
        p = 50
        self.mode = 'menu'
        #buttons here_----------------------------------------------------------
        self.aiBtn = Button(self.app, width=w, pady=p,
                       text='Play Against AI!', command=self.playAI)
        self.hostBtn = Button(self.app, width=w, pady=p,
                       text='Host a game!', command=self.hostGame)
        self.joinBtn = Button(self.app, width=w, pady=p,
                       text='Join a game!', command=self.joinGame)

        self.aiBtn.grid(row=0, column=0, sticky="WE")
        self.hostBtn.grid(row=1, column=0, sticky="WE")
        self.joinBtn.grid(row=2, column=0, sticky="WE")

    def playAI(self):
        self.mode="ai"
        self.destroyMenu()
        self.createGrid()

    def hostGame(self):
        self.mode="host"
        self.destroyMenu()

    def joinGame(self):
        self.mode="join"
        self.destroyMenu()

    def destroyMenu(self):
        self.aiBtn.destroy()
        self.hostBtn.destroy()
        self.joinBtn.destroy()

    def createGrid(self):
        if (self.mode == 'ai'):
            self.board = Board('ai')
        elif (self.mode == 'host'):
            self.board = Board('host')
        elif(self.mode == 'join'):
            self.board = Board('join')

        for col,row in self.board.fields:
            handler = lambda x=col,y=row: self.move(x,y)
            button = Button(self.app, command=handler, font=self.font,
                            disabledforeground='black', state='normal',
                            width=4, height=2, pady=0)
            button.grid(row=row, column=col)
            self.buttons[col,row] = button

        self.backBtn = Button(self.app, text='Back to Menu',
                         command=self.backButton)
        self.backBtn.grid(row=self.board.size, column=1,
                     columnspan=self.board.size/2, sticky="WE")

        self.update()

    def backButton(self):
        #destroy the current windows based on what mode we are on rn
        #                   ie human vs AI mode
        #self.board = Board("AI")
        #self.update()

        for col,row in self.board.fields:
            self.buttons[col,row].destroy()

        self.backBtn.destroy()
        self.menuScreen()


    #def resetAI(self):
     #   self.board = Board("AI")
     #   self.update()

    def move(self,x,y):
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x,y)
        self.update()
        # AI moves here
        # call to minimax here... need to display on screen to wait for move
        move = self.board.bestMove()
        print(move)
        if (move):
            self.board = self.board.move(*move)
            self.update()
        self.app.config(cursor="")

    def update(self):
        for (x,y) in self.board.fields:
            gridVal = self.board.fields[x,y]
            self.buttons[x,y]['text'] = gridVal

            if (gridVal != self.board.empty):
                self.buttons[x,y]['state'] = 'disabled'

        for (x,y) in self.board.fields:
            self.buttons[x,y].update()
        winning = self.board.won() # the winning coords
        if (winning != None):
            for x,y in self.buttons:
                self.buttons[x,y]['state'] = 'disabled'
            for x,y in winning:
                self.buttons[x,y]['disabledforeground'] = 'red'

    def mainloop(self):
        self.app.mainloop()

if __name__ == '__main__':
    GUI().mainloop()

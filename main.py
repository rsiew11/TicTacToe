from Tkinter import Tk, Button, Label
from tkFont import Font
from Board import Board
import socket

class GUI:
    def __init__(self):
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=False, height=False)
        self.font = Font(family="Helvetica", size=100)
        self.board = Board("ai")
        self.buttons = {}
        self.backBtn = None
        self.gameOverLabel = None

        #menu buttons
        self.mode=""
        self.aiBtn=None
        self.hostBtn=None
        self.joinBtn=None

        #networking constructs
        self.conn = None
        self.addr = None
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 5007
        self.BUFFER_SIZE = 128
        self.s = None

        # begin the menu
        self.menuScreen()

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
        self.app.title('HOST')
        self.mode="host"
        self.destroyMenu()
        waiting = Label(self.app, text = "waiting for player 2!")
        waiting.grid(row=0,column=0,sticky="WE",pady=150,padx=150)

        ### connection!!
        self.sh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sh.bind((self.TCP_IP, self.TCP_PORT))
        self.sh.listen(1)
        self.conn, self.addr = self.sh.accept()
        data = self.conn.recv(self.BUFFER_SIZE)
        print(data)
        self.conn.send("ur gonna join")

        #setting up the menu stuff
        waiting.destroy()
        self.createGrid()
        # CLosing connection for now
        #self.conn.close()

    def joinGame(self):
        self.app.title('JOIN')
        self.mode="join"
        self.destroyMenu()
        waiting = Label(self.app, text = "waiting for player 1!")
        waiting.grid(row=0,column=0,sticky="WE",pady=150,padx=150)
        ### connection!!
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP,self.TCP_PORT))
        self.s.send("ur the host!!")
        data = self.s.recv(self.BUFFER_SIZE)
        print(data)

        #setting up the menu stuff
        waiting.destroy()
        self.createGrid()

        #make the player wait!!
        self.waitForMove()

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
        for col,row in self.board.fields:
            self.buttons[col,row].destroy()

        if (self.mode == 'host'):
            self.conn.close()
        elif (self.mode == 'join'):
            self.s.close()

        if (self.gameOverLabel != None):
            self.gameOverLabel.destroy()

        self.backBtn.destroy()
        self.menuScreen()

    def waitForMove(self):
        if (self.mode == 'host'):
            ## disable the buttons
            self.disableButtons()
            ## make a label to show that it's other turn
            while(1):
                #wait for player 2's move
                print("waiting for joiner")
                data = self.conn.recv(self.BUFFER_SIZE)
                x = int(data[0])
                y = int(data[2])
                if (len(data)==3): break


        elif (self.mode == 'join'):
            ## disable the buttons
            ## make a label to show that it's other turn
            while (1):
                #wait for player 1's move
                print("waiting for host")
                data = self.s.recv(self.BUFFER_SIZE)
                x = int(data[0])
                y = int(data[2])
                if (len(data)==3): break

        print(x)
        print(y)
        self.board = self.board.move(x,y)
        self.update()

    def move(self,x,y): # the x and y are coords of button pushed
        if (self.mode == 'ai'): # player vs AI
            self.app.config(cursor="watch")
            self.app.update()
            self.board = self.board.move(x,y)
            self.update()
            # find the AI move via minimax
            move = self.board.bestMove()
            print(move)
            if (move):
                self.board = self.board.move(*move)
                self.update()
            self.app.config(cursor="")

        elif (self.mode == 'host'): # player 1
            self.app.config(cursor="watch")
            self.app.update()
            self.board = self.board.move(x,y)
            self.update()
            #send move to player 2
            #data = self.conn.recv(self.BUFFER_SIZE)
            #print(data)
            self.conn.send(str(x)+','+str(y))
            self.waitForMove()
            self.conn.close()

        elif (self.mode == 'join'): # player 2
            # wait for player 1 move
            #self.s.send("im cnectin")
            #data = self.s.recv(self.BUFFER_SIZE)
            #print(data)
            self.app.config(cursor="watch")
            self.app.update()
            self.board = self.board.move(x,y)
            self.update()

            self.s.send(str(x)+','+str(y))
            self.waitForMove()
            #self.s.close()

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

            for col,row in self.board.fields:
                self.buttons[col,row].destroy()


            self.gameOverLabel = Label(self.app, text = "GAME OVER!")
            self.gameOverLabel.grid(row=0,column=0,sticky="WE",pady=250,padx=250)


    def disableButtons(self):
        for x,y in self.buttons:
            self.buttons[x,y]['state'] = 'disabled'

    def enableButtons(self):
        for x,y in self.buttons:
            self.buttons[x,y]['state'] = 'normal'

    def mainloop(self):
        self.app.mainloop()

if __name__ == '__main__':
    GUI().mainloop()

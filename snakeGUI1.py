from tkinter import *
from snakeLogic import SnakeLogic 
import random

class SnakeGUI(object):
    def __init__(self):
        self.boardSize = 10
        self.board = []
        self.root = Tk()
        self.root.title("Game con rắn nhom 6")
        self.canvas = Canvas(self.root, width=(self.boardSize * 31), height=(self.boardSize * 31))
        self.canvas.pack()
        self.direction = ""
        self.gameOver = False
        self.root.canvas = self.canvas.canvas = self.canvas

        self.boardSizeEntry = Entry(self.root)
        self.boardSizeEntry.pack()
        self.boardSizeEntry.insert(0, "10")  # Default value

        self.newGameButton = Button(self.root, command=self.init, text='New Game').pack()
        self.CPUGameButton = Button(self.root, command=self.initA_Star, text='A* run').pack()
        self.root.bind("<Key>", self.keyPressed)  # binds keyEvent to the function keyPressed()
        self.gameStarted = False
        self.isA_StarGameClicked = False
        self.isNewGameClicked = False
        self.printInstructions()
        self.computerPlay = False

    def init(self):
        try:
            size = int(self.boardSizeEntry.get())
            if 10 <= size <= 50:
                self.boardSize = size
                self.canvas.config(width=(self.boardSize * 31), height=(self.boardSize * 31))
                self.isNewGameClicked = True
                self.newGame()
            else:
                print("Please enter a value between 10 and 50.")
        except ValueError:
            print("Invalid input. Please enter a number between 10 and 50.")

    def initA_Star(self):
        self.isA_StarGameClicked = True

    def newGame(self):
        self.gameOver = False
        self.gameStarted = False
        self.computerPlay = False
        self.printInstructions()
        self.score = 0
        self.board = [[0] * self.boardSize for _ in range(self.boardSize)]  #Tạo 1 bảng với kích thước mới

        #Đặt các CNV
        self.board[3][3] = -3
        self.board[4][4] = -3


        self.redrawAll()

        

    def updateBoard(self, board):
        self.canvas.delete(ALL)
        self.board = board
        self.drawSnakeBoard()

    def gameOverScreen(self, score):
        """Outputs the Game Over screen in the GUI"""
        canvas_id = self.canvas.create_text(100, 50, anchor="nw")
        endText = "Game Over!\nYour score is:" + str(score)
        self.canvas.itemconfig(canvas_id, text=endText, fill='red')

    def timerFired(self, logic):
        """Delays the game by the tick time amount"""
        delay = 80 
        if self.isNewGameClicked:
            self.isNewGameClicked = False
            self.computerPlay = False
            logic.gameOver = False
            logic.loadSnakeBoard(self.boardSize)
            self.updateBoard(logic.getBoard())
            self.gameStarted = False
            logic.score = 0

        if self.isA_StarGameClicked:
            self.isA_StarGameClicked = False
            logic.gameOver = False
            logic.loadSnakeBoard(self.boardSize)
            self.gameStarted = False
            self.updateBoard(logic.getBoard())
            self.computerPlay = True
            logic.score = 0

        if self.gameStarted and not logic.gameOver:
            if self.computerPlay:
                logic.calculateAstar()
                logic.setDirection()
                self.updateBoard(logic.getBoard())
                self.redrawAll()
            else:
                logic.makeMove(self.direction)
                self.updateBoard(logic.getBoard())
                self.redrawAll()
        elif logic.gameOver:
            self.gameOver = True
            self.gameOverScreen(logic.getScore())
        else:
            self.redrawAll()

        self.canvas.after(delay, self.timerFired, logic)

    def drawSnakeBoard(self):
        """Take the 2D list board, and visualizes it into the GUI"""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.drawSnakeCell(row, col)

    def drawSnakeCell(self, row, col):
        """Helper function for drawSnakeBoard
           Draws the cell, which is represented as a rectangle, in the GUI
           if cell is where the snake is at, it has blue oval
           if cell is where the food is at, it has yellow oval"""
        margin = 5
        cellSize = 30
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        board = self.board
        self.canvas.create_rectangle(left, top, right, bottom, fill="lightblue")
        
        if board[row][col] > 0:
            # draw part of the snake body
            self.canvas.create_oval(left, top, right, bottom, fill="green")
        elif board[row][col] == -1:
            self.canvas.create_oval(left, top, right, bottom, fill="yellow")
        elif board[row][col] == -3:
            self.canvas.create_oval(left, top, right, bottom, fill="black")
            
    
    
    def makeObstacle(self):
        width = self.boardSize
        row = random.choice(range(width-1))
        col = random.choice(range(width-1))
        # if we are at a location where snake already exists, keep looking for random blank space
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width-1))
            col = random.choice(range(width-1))

        self.snakeBoard[row][col] = -3
        
        


    def redrawAll(self):
        """Deletes the current snakeBoard, and redraws a new snakeBoard with changed values"""
        self.canvas.delete(ALL)
        self.drawSnakeBoard()

    def keyPressed(self, event):
        """Input: Keyboard event
        1) Sets the direction data member given corresponding arrow-key event
        2) game starts from the moment key is pressed also"""
        self.direction = event.keysym
        self.gameStarted = True

    def getDirection(self):
        return self.direction

    def printInstructions(self):
        """Print the instructions of the game in the Console"""
        print("Welcome to Snake Game!")
        print("Use the Arrow keys to move!")
        print("Press New Game to Restart your game!")
        print("Press A* Game and then press any arrow key to watch the A* Algorithm Snake Player!")
#ashikag
#tetris_bonus
##############################
#import the following to be used in the programs
import random
import copy

from Tkinter import *
import tkMessageBox
import sys


def mousePressed(event):
    redrawAll()
    #calls the redrawAll method each time 

def keyPressed(event):
    #controller
    if (event.char == "r"):
    #restart
        init()
    elif (event.char == "p"):
    #pause
        pauseScreen()
    elif (event.char == "h"):
        init()

    if (canvas.data.isSplashScreen==True):
        if (event.char == "s"):
        #start game
            splashScreen()
            pauseScreen()
            #at start screen the game is paused
    if canvas.data.isGameOver==False:
        if event.keysym=="Left":
            #each key moves it accordingly based on grid coordinates 
            moveFallingPiece(canvas,0,-1)
        elif event.keysym=="Right":
            moveFallingPiece(canvas,0,1)
        elif event.keysym=="Down":
            moveFallingPiece(canvas,1,0)
        elif event.keysym=="Up":
            #rotates piece counterclockwise
            rotateFallingPiece()
        elif event.char=="d":
        #drops the piece to bottom most position
            while moveFallingPiece(canvas,1,0):
            #loop continues until the move is False
                pass
    redrawAll()

def timerFired():
    if canvas.data.isGameOver==False and (canvas.data.isPauseScreen==False):
        #runs until the game is over or is paused
        if moveFallingPiece(canvas,1,0)==False:
            #if a piece can no longer move, place it on tetrisBoard
            placeFallingPiece()
            removeFullRows()
            #will remove multiple rows via the function
            newFallingPiece()
            if fallingPieceIsLegal()==False:
            #will put one  piece over the top before the game ends
                canvas.data.isGameOver=True
    redrawAll()
    delay = 300 # milliseconds
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    #view
    canvas.delete(ALL)
    if (canvas.data.isSplashScreen==True):
        #start screen with intructions
        drawSplashScreen()
    else:
        drawGame()
        drawScore()
        canvasWidth=canvas.data.canvasWidth
        canvasHeight=canvas.data.canvasHeight
    if canvas.data.isGameOver==True:
        #Text over finished game image
        canvas.create_text(canvasWidth/2,canvasHeight/2, text="     GAME OVER\n" + "       PRESS R  \n" +\
            "     TO RESTART" + "\n  FINAL SCORE: " + str(canvas.data.score), font=("Helvetica", 40, "bold"))

    elif (canvas.data.isPauseScreen==True and
          canvas.data.isSplashScreen==False):
        #text over paused game
        drawPauseScreen()

def splashScreen():#Turns splash screen off
    canvas.data.isSplashScreen=False

def drawSplashScreen():
    sx = canvas.data.canvasWidth/2
    sy = canvas.data.canvasHeight/2
    #instructions
    canvas.create_text(sx, sy,
                       text="                   GAME OF TETRIS\n"+ "\n                  BY:ASHIKA GANESH \n" +\
                       "\n 'Up' key rotates block\n" + "\nLeft, Right, and Down keys move blocks \n" +\
                        "\n'S' starts\n"+"\n'R' restarts & 'P' pauses\n" + "\n'H' will return you to the help screen\n" +\
                         "\n'D' sends piece to bottom \n" + "\n *Clear rows to get bonus points!!!\n",\
                         font=("Helvetica", 13, "bold"))
    #creates wat will be printed out onto the screen as a preview before the start of teh game

def drawPauseScreen():
    #pause screen is white with the word Pause
    px = canvas.data.canvasWidth/2
    py = canvas.data.canvasHeight/2
    canvas.create_text(px, py, text="PAUSE", font=("Helvetica", 100, "bold"))
    #if paused, will print on the screen "PAUSE"

def pauseScreen():#can turn on and off with p
    if (canvas.data.isPauseScreen==True):
        canvas.data.isPauseScreen=False
    elif (canvas.data.isPauseScreen==False):
        canvas.data.isPauseScreen=True
        #set the pause screen to opposite variables to toggle

def drawScore():
    #located at bottom left corner
    canvas.create_text(canvas.data.margin+20,479,text="SCORE="+ str(canvas.data.score))
    #writes the score values

def removeFullRows():
    score = 0
    def isFullRow(tetrisBoard, oldRow):
        fullRow = len(tetrisBoard[0])
        count = 0
        for i in xrange(len(tetrisBoard[oldRow])):
            if tetrisBoard[oldRow][i]!="blue":
                count+=1
                if count == fullRow:
                    return True
    tetrisBoard = canvas.data.tetrisBoard
    rows = len(tetrisBoard)
    cols = len(tetrisBoard[0])
    newTetrisBoard=[]
    for row in range(rows):
            newTetrisBoard += [[canvas.data.emptyColor] * cols]
    fullRows = 0
    newRow = len(tetrisBoard)-1
    for oldRow in xrange(rows-1, -1, -1):
            if not isFullRow(tetrisBoard, oldRow):
                for i in xrange(len(tetrisBoard[oldRow])):
                    newTetrisBoard[newRow][i] = tetrisBoard[oldRow][i]
                newRow -=1
            else:
                fullRows +=1
		score +=1
    canvas.data.tetrisBoard = newTetrisBoard
    canvas.data.score+=score**2


def placeFallingPiece():
    #loads falling piece onto tetrisBoard
    fallingPieceColor=canvas.data.fallingPieceColor
    tetrisBoard=canvas.data.tetrisBoard
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    fallingPiece=canvas.data.fallingPiece
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    for row in range(fallingPieceRows):
        for col in range(fallingPieceCols):
            if fallingPiece[row][col]==True:
                (tetrisBoard[fallingPieceRow+row]
                [fallingPieceCol+col])=fallingPieceColor

def moveFallingPiece(canvas, drow, dcol):
    # moves the block by key functions 
    canvas.data.fallingPieceCol+=dcol
    canvas.data.fallingPieceRow+=drow
    if fallingPieceIsLegal()==False:
        canvas.data.fallingPieceCol-=dcol
        canvas.data.fallingPieceRow-=drow
        return False
    return True
        
def rotateFallingPiece():
    oldFallingPiece=canvas.data.fallingPiece
    oldFallingPieceRow=canvas.data.fallingPieceRow
    oldFallingPieceCol=canvas.data.fallingPieceCol
    canvas.data.fallingPieceRows=len(oldFallingPiece)
    canvas.data.fallingPieceCols=len(oldFallingPiece[0])
    (oldCenterRow,oldCenterCol)=fallingPieceCenter()
    #finds old center which is off a bit for pieces that have even rows or cols
    canvas.data.fallingPieceRows=len(oldFallingPiece[0])
    canvas.data.fallingPieceCols=len(oldFallingPiece)
    #switches the direction of the peice
    (newCenterRow,newCenterCol)=fallingPieceCenter()
    #finds a new center
    canvas.data.fallingPieceRow+=(oldCenterRow-newCenterRow)
    canvas.data.fallingPieceCol+=(oldCenterCol-newCenterCol)
    #adjusts location according to center of fallingPiece
    rotatedFallingPiece=[]
    for row in range(canvas.data.fallingPieceRows):
        rotatedFallingPiece += [[False]*canvas.data.fallingPieceCols]
        #new 2d list of False's for rotated piece
    for row in range(canvas.data.fallingPieceCols):
        for col in range(canvas.data.fallingPieceRows):
            (rotatedFallingPiece
            [canvas.data.fallingPieceRows-1-col]
            [row])=(oldFallingPiece[row][col])
            #stores rotated piece values to old piece values
    canvas.data.fallingPiece=rotatedFallingPiece
    #sets the rotated piece to falling piece
    if fallingPieceIsLegal()==False:
    #if that piece is not legal, switch back to the old piece
        canvas.data.fallingPiece=oldFallingPiece
        canvas.data.fallingPieceRow=oldFallingPieceRow
        canvas.data.fallingPieceCol=oldFallingPieceCol
    
def fallingPieceCenter():
    #finds the current fallingPiece center
    row=(canvas.data.fallingPieceRows-1)/2
    col=(canvas.data.fallingPieceCols-1)/2
    return (row,col)
        
def fallingPieceIsLegal():
    #tests if the piece is in a legal spot
    emptyColor=canvas.data.emptyColor
    tetrisBoard=canvas.data.tetrisBoard
    fallingPiece=canvas.data.fallingPiece
    fallingPieceCol=canvas.data.fallingPieceCol
    fallingPieceRow=canvas.data.fallingPieceRow
    rows= canvas.data.rows
    cols= canvas.data.cols
    #find values of rows and cols based on canvas
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    for row in range(fallingPieceRows):
        for col in range(fallingPieceCols):
            if fallingPiece[row][col]==True:
                if (fallingPieceRow+row>=rows or fallingPieceRow<0 or fallingPieceCol+col>=cols or fallingPieceCol<0):
                    return False
                elif (tetrisBoard[fallingPieceRow+row]
                      [fallingPieceCol+col])!=emptyColor:
                    return False
    return True
    
def newFallingPiece():
    #create new falling piece at top of tetrisBoard
    canvas.data.fallingPieceRow=0
    cols=canvas.data.cols
    tetrisPieces=canvas.data.tetrisPieces
    tetrisPieceColors=canvas.data.tetrisPieceColors
    i=random.randint(0, len(tetrisPieces)-1)
    x=random.randint(0, len(tetrisPieces)-1)
    canvas.data.fallingPiece=tetrisPieces[i]
    canvas.data.fallingPieceColor=tetrisPieceColors[x]
    canvas.data.fallingPieceCol=(canvas.data.cols/2- len(canvas.data.fallingPiece[0])/2)
    #places the new peice in the center
    
def drawFallingPiece():
    #draw falling piece over tetrisBoard
    fallingPiece=canvas.data.fallingPiece
    fallingPieceColor=canvas.data.fallingPieceColor
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    for row in range(fallingPieceRows):
        for col in range(fallingPieceCols):
            if fallingPiece[row][col]==True:
                drawTetrisCell(canvas,fallingPieceRow+row,
                         fallingPieceCol+col,fallingPieceColor)
    
def loadTetrisBoard():
    #loads whole setup for tetrisBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    emptyColor=canvas.data.emptyColor
    tetrisBoard = [ ]
    #tetrisBoard is a grid
    for row in range(rows): tetrisBoard += [[emptyColor] * cols]
    canvas.data.tetrisBoard = tetrisBoard

def drawTetrisBoard():
    tetrisBoard=canvas.data.tetrisBoard
    rows = len(tetrisBoard)
    cols = len(tetrisBoard[0])
    for row in range(rows):
        for col in range(cols):
            color=tetrisBoard[row][col]
            drawTetrisCell(canvas, row, col, color)# nothing drawn here but cells
            
def drawTetrisCell(canvas, row, col, color):
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize 
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill=color)
    #color changes drawn here
    
def drawGame():
    canvasWidth=canvas.data.canvasWidth
    canvasHeight=canvas.data.canvasHeight
    #canvas.data.scoreText=str(canvas.data.scoreCounter)
    wx=canvasWidth/2
    #canvas.create_text(wx, 15, text=canvas.data.scoreText)
    canvas.create_rectangle(0, 0,
                            canvasWidth+10, canvasHeight+10, fill="orange")
    drawTetrisBoard()
    drawFallingPiece()

def init():
    canvas.data.score=0
    canvas.data.isSplashScreen=True
    #start with start screen
    canvas.data.isPauseScreen=True
    #game begins paused
    canvas.data.emptyColor="blue"
    canvas.data.isGameOver=False
    #creates each of the tetris game board peices
    iPiece=[[True,True,True,True]]
    jPiece=[[True,False,False],
           [True,True,True]]
    lPiece=[[False,False,True],
           [True,True,True]]
    oPiece=[[True,True],
           [True,True]]
    sPiece=[[False,True,True],
           [True,True,False]]
    tPiece=[[False,True,False],
           [True,True,True]]
    zPiece=[[True,True,False],
           [False,True,True]]
    tetrisPieces=[iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors=[ "red", "yellow", "magenta","pink", "cyan", "green", "orange" ]
    #possible colors 
    canvas.data.tetrisPieces=tetrisPieces
    canvas.data.tetrisPieceColors=tetrisPieceColors
    newFallingPiece()
    canvas.data.fallingPieceRow=0
    canvas.data.fallingPieceCol=(canvas.data.cols/2-len(canvas.data.fallingPiece[0])/2)
    loadTetrisBoard()
    redrawAll()

def run(rows,cols):
    # create the root and the canvas
    global canvas
    root = Tk()
    margin = 20
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    #root.resizable(width=0, height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    #canvas.data.scoreList= []#scorelist of scores from every game
    init()
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  

run(15,10) #runs a 15 by 10 board for tetris

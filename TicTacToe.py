
import pygame
import copy
from GameAlgos import Game
from MonteCarloNode import MCTSNode
from MonteCarloSearch import MonteCarloTreeSearch
def draw_lines(grid):
    no= grid - 1
    for n in range(1,no+1):
        #horizontal
        pygame.draw.line(screen,(255,255,255),(0,(n*screenSize)//(no+1)),(screenSize,(n*screenSize)//(no+1)))
        #vertical
        pygame.draw.line(screen,(255,255,255),((n*screenSize)//(no+1),0),((n*screenSize)//(no+1),screenSize))
        
def mouse_to_board(x,y,grid1):
    no = grid1-1
    row= 0 
    col = 0
    for n in range(1,no+2):
        if x in range(((n-1)*screenSize)//(no+1),((n)*screenSize)//(no+1)):
            col = n
        if y in range(((n-1)*screenSize)//(no+1),((n)*screenSize)//(no+1)):
            row = n
    return (row,col)
            
def is_valid(board,x,y):
    if board[x][y] is None:
        return 1
    else:
        return 0
    
def is_full(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] is None:
                return 0
    return 1
def wincheck(arr,wk):
    tempx=0
    tempy=0

    for i in range(len(arr)-wk+1):
        x=arr[i]                                       
        for j in range(i,i+wk):
            if arr[j] == x:                        
                if arr[j] == 'X':
                    tempx=tempx+1
                    if tempx == wk:
                        return 'X',i,j
                elif arr[j] == 'O':
                    tempy=tempy+1
                    if tempy == wk:
                        return 'O',i,j
            else:
                tempx = 0
                tempy = 0
    return 0,0,0
            
def get_winner(board,wk):
    for i in range(len(board)):
        temp,s,e = wincheck(board[i],wk)
        if temp!=0:
            return (temp,s+1,e+1,i+1,1)
    leftdiag=[]
    rightdiag=[]    
    for i in range(len(board)):
        col = []
        for j in range(len(board)):
            col.append(board[j][i])
            if i == j:
                leftdiag.append(board[i][j])
                rightdiag.append(board[i][len(board)-j-1])
        temp,s,e = wincheck(col,wk)
        if temp!=0:
            return (temp,i+1,s+1,e+1,2)
    temp,s,e = wincheck(leftdiag,wk)
    if temp!=0:
        return(temp,s+1,e+1,0,3)
    temp,x,y = wincheck(rightdiag,wk)
    if temp!=0:
        return(temp,s+1,e+1,1,3)
    winK = wk
    while winK<len(board):    
        l1=[]
        l2=[]
        l3=[]
        l4=[]
        count = 0
        for i in range(len(board)-winK):
            for j in range(winK):
                count +=1
        count = count - winK
        for i in range(len(board)-winK):
            for j in range(winK):
                if count != 0:
                    count-=1
                    continue
                l1.append(board[i+j+1][j])
                l2.append(board[j][i+j+1])
                l3.append(board[len(board)-i-j-2][j])
                l4.append(board[i+j+1][len(board)-j-1])
        temp,s,e = wincheck(l1,wk)
        if temp !=0:
            return (temp,0,0,0,3)
        temp,s,e = wincheck(l2,wk)
        if temp !=0:
            return (temp,0,0,0,3)
        temp,s,e = wincheck(l3,wk)
        if temp !=0:
            return (temp,s+1,e+1,1,3)
        temp,s,e = wincheck(l4,wk)
        if temp !=0:
            return (temp,len(board)-s,len(board)-e,1,3)

        winK=winK+1
        
    return None

def show_algos():
    screen1 = pygame.display.set_mode((600,400))
    screen1.fill(backgroundColor)
    text3= myFont1.render('Press 1 for MinMax', True, (255,255,255))
    screen1.blit(text3 , (80,100))
    text3= myFont1.render('Press 2 for AlphaBeta pruning', True, (255,255,255))
    screen1.blit(text3 , (80,120))
    text3= myFont1.render('Press 3 for depth limited Minmax', True, (255,255,255))
    screen1.blit(text3 , (80,140))
    text3= myFont1.render('Press 4 for Combo of 2 and 3', True, (255,255,255))
    screen1.blit(text3 , (80,160))
    text3= myFont1.render('Press 5 for Monte Carlo Tree Search', True, (255,255,255))
    screen1.blit(text3 , (80,180))
def get_algo():
    show_algos()
    while True:
        pygame.display.update()
        algo = 0
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    x=pygame.key.name(event.key)
                    valid = ["1","2","3","4","5"]
                    if x not in valid:
                        print("wrong Number")
                        screen1 = pygame.display.set_mode((600,400))
                        text3= myFont1.render('Press valid Number', True, (255,255,255))
                        screen1.blit(text3 , (80,160))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        show_algos()
                    else:
                        algo = int(x)
                        string = 'You have pressed ' + str(x)+"."
                        screen1 = pygame.display.set_mode((600,400))
                        text3= myFont1.render(string, True, (255,255,255))
                        screen1.blit(text3 , (80,160))
                        pygame.display.update()
                        pygame.time.delay(400)
                        return (algo,1)
def get_winK(grid):
    screen1 = pygame.display.set_mode((600,400))
    text3= myFont1.render('Give number of connecting pieces to win...', True, (255,255,255))
    screen1.blit(text3 , (80,160))
    while True:
        pygame.display.update()
        winK=3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    x=pygame.key.name(event.key)
                    if not x.isdigit():
                        print("wrong Number")
                        screen1 = pygame.display.set_mode((600,400))
                        text3= myFont1.render('Press valid Number', True, (255,255,255))
                        screen1.blit(text3 , (80,160))
                        pygame.display.update()
                        pygame.time.delay(1000)
                        screen1 = pygame.display.set_mode((600,400))
                        text3= myFont1.render('Give number of connecting pieces to win...', True, (255,255,255))
                        screen1.blit(text3 , (80,160))
                    else:
                        x=int(x)
                        if x>1 and x<=grid:
                            winK = int(x)
                            string = 'You have pressed ' + str(x)+"."
                            screen1 = pygame.display.set_mode((600,400))
                            text3= myFont1.render(string, True, (255,255,255))
                            screen1.blit(text3 , (80,160))
                            pygame.display.update()
                            pygame.time.delay(400)
                            return winK
                        else:
                            pygame.time.delay(500)
                            screen1 = pygame.display.set_mode((600,400))
                            string = 'Press valid Number between 1 and ' + str(grid)+"."
                            text3= myFont1.render(string, True, (255,255,255))
                            screen1.blit(text3 , (80,160))
                            pygame.display.update()
                            pygame.time.delay(1000)
                            screen1 = pygame.display.set_mode((600,400))
                            text3= myFont1.render('Give number of connecting pieces to win...', True, (255,255,255))
                            screen1.blit(text3 , (80,160))

                            

                
def get_grid():
    screen1 = pygame.display.set_mode((600,400))
    screen1.fill(backgroundColor)
    text3= myFont1.render('Press a number for nXn grid.', True, (255,255,255))
    screen1.blit(text3 , (80,100))
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                else:
                    x=pygame.key.name(event.key)
                    if x.isdigit():
                        grid = int(x)
                        algo = int(x)
                        string = 'Creating ' + str(x)+"x" + str(x)+' grid.'
                        screen1 = pygame.display.set_mode((600,400))
                        text3= myFont1.render(string, True, (255,255,255))
                        screen1.blit(text3 , (80,160))
                        pygame.display.update()
                        pygame.time.delay(400)
                        return grid
                        


board = [[None, None, None], [None, None, None], [None, None, None]]

screenSize=400
pygame.init()
pygame.display.init()  

screen1 = pygame.display.set_mode((600,400))
backgroundColor=(0,0,0)
screen1.fill(backgroundColor)
pygame.display.set_caption('Game')
myFont = pygame.font.SysFont('comicsansms', 45)
myFont1 = pygame.font.SysFont('comicsansms', 20)
text = myFont.render('Welcome player', True, (255,255,255))
text1= myFont1.render('Press 1 to play tic tac toe', True, (255,255,255))
screen1.blit(text,(60,30))
screen1.blit(text1 , (80,120))
text1= myFont1.render('Press 2 to play Open field tic tac toe', True, (255,255,255))
screen1.blit(text1 , (80,140))
currentPlayer = 'X'
game = Game()
algo = 0
canPlay = 0
gameNo = 0
grid = 3
winK = 3
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            if canPlay:
                pos = pygame.mouse.get_pos()
                k=grid
                x,y=mouse_to_board(pos[0],pos[1],grid)
                if is_valid(board,x-1,y-1):
                    if currentPlayer == 'X':
                        board[x-1][y-1] = currentPlayer
                        text2 = myFont.render('X', True, (255,255,255))
                        if grid == 2:
                            screen.blit(text2,((((2*y-1)*screenSize)//(k*2))-screenSize//(k*12),(((2*x-1)*screenSize)//(k*2))-screenSize//(k*6))) 
                        else:
                            screen.blit(text2,((((2*y-1)*screenSize)//(k*2))-screenSize//(k*8),(((2*x-1)*screenSize)//(k*2))-screenSize//(k*4)))
                            
                        winner = get_winner(board,winK)
                        if not winner:
                            if algo == 1:
                                print("MinMax")
                                t,temp = game.MinMax(copy.deepcopy(board),1,winK)
                            elif algo == 2:
                                print("Alpha Beta")
                                t,temp = game.AlphaBetaPruning(copy.deepcopy(board),1,-10000,10000,winK)
                            elif algo == 3:
                                print("Depth limit")
                                t,temp = game.MinMax_depth(copy.deepcopy(board),1,6,winK)
                            elif algo == 4:
                                print("Combo ")
                                t,temp = game.MinMax_DepthplusAlphaBeta(copy.deepcopy(board),1,-10000,10000,6,winK)
                            elif algo == 5:
                                print("Monte Carlo")
                                node = MCTSNode(copy.deepcopy(board),'X',winK)
                                tree = MonteCarloTreeSearch(node)
                                monte_next_state = tree.best_action(1000).state 
                                montex = 0
                                montey = 0
                                for i in range(len(board)):
                                    for j in range(len(board)):
                                        if board[i][j]!=monte_next_state[i][j]:
                                            montex=i
                                            montey=j
                                temp=(1,montex,montey)
                                t='Monte move'
                            currentPlayer = 'O'
                            print(t,' - ',temp[1],temp[2])
                            if temp[1] is not None and is_valid(board,temp[1],temp[2]):
                                board[temp[1]][temp[2]] = currentPlayer
                                text2 = myFont.render('O', True, (255,255,255))
                                x=temp[1]+1
                                y=temp[2]+1
                                if grid == 2:
                                    screen.blit(text2,((((2*y-1)*screenSize)//(k*2))-screenSize//(k*12),(((2*x-1)*screenSize)//(k*2))-screenSize//(k*6)))
                               
                                else:
                                    screen.blit(text2,((((2*y-1)*screenSize)//(k*2))-screenSize//(k*8),(((2*x-1)*screenSize)//(k*2))-screenSize//(k*4)))
                            currentPlayer='X'
                        winner = get_winner(board,winK)

                        if winner:
                            if winner[0] == 'X':
                                print(winner[3])
                                print('X is Won')
                                if winner[4] == 1:
                                    pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),4)
                                elif winner[4] == 2:
                                    pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),4)
                                else:
                                    if winner[3] == 0:
                                        pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[1]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),4)
                                    elif winner[3] == 1:
                                        pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[1]-1)*screenSize)//(k*2)),4)
                                
                                pygame.display.flip()   
                                pygame.time.delay(300)
                                
                                pygame.display.update
                                pygame.time.delay(400)
                                screen1 = pygame.display.set_mode((600,400))
                                screen1.fill(backgroundColor)
                                text3= myFont.render('X won', True, (255,255,255))
                                screen1.blit(text3 , (60,30))
                                text3= myFont1.render('1. Press r to Reset', True, (255,255,255))
                                screen1.blit(text3 , (80,120))
                                text3= myFont1.render('2. Press esc to Quit', True, (255,255,255))
                                screen1.blit(text3 , (80,140))

                            elif winner[0] == 'O':
                                print('O is Won')
                                if winner[4] == 1:
                                    pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),4)
                                elif winner[4] == 2:
                                    pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[3]-1)*screenSize)//(k*2)),4)
                                else:
                                    if winner[3] == 0:
                                        pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[1]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),4)
                                    elif winner[3] == 1:
                                        pygame.draw.line(screen,(255,0,255),(((2*winner[1]-1)*screenSize)//(k*2),((2*winner[2]-1)*screenSize)//(k*2)),(((2*winner[2]-1)*screenSize)//(k*2),((2*winner[1]-1)*screenSize)//(k*2)),4)
                                
                                pygame.display.flip()   
                                pygame.time.delay(300)
                                pygame.display.update
                                pygame.time.delay(400)
                                screen1 = pygame.display.set_mode((600,400))
                                screen1.fill(backgroundColor)
                                text3= myFont.render('O won', True, (255,255,255))
                                screen1.blit(text3 , (60,30))
                                text3= myFont1.render('1. Press r to Reset', True, (255,255,255))
                                screen1.blit(text3 , (80,120))
                                text3= myFont1.render('2. Press esc to Quit', True, (255,255,255))
                                screen1.blit(text3 , (80,140))


                        else:
                            if is_full(board):
                                
                                screen1 = pygame.display.set_mode((600,400))
                                screen1.fill(backgroundColor)
                                text3= myFont.render("It's a tie", True, (255,255,255))
                                screen1.blit(text3 , (60,30))
                                text3= myFont1.render('1. Press r to Reset', True, (255,255,255))
                                screen1.blit(text3 , (80,120))
                                text3= myFont1.render('2. Press esc to Quit', True, (255,255,255))
                                screen1.blit(text3 , (80,140))

                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                algo = 0
                canPlay = 0
                gameNo = 0
                grid = 3
                board = [[None for i in range(grid)] for j in range(grid)]
                screen1 = pygame.display.set_mode((600,400))
                screen1.fill(backgroundColor)
                text3= myFont1.render('Press 1 for Tic Tac Toe', True, (255,255,255))
                screen1.blit(text3 , (80,100))
                text3= myFont1.render('Press 2 for Open field tic tac toe', True, (255,255,255))
                screen1.blit(text3 , (80,120))
            if event.key == pygame.K_0:
                screen.fill(backgroundColor)
                screen.blit(text1 , (80,80))
            if event.key == pygame.K_1:
                if gameNo == 0:
                    gameNo = 1
                if algo == 0 and canPlay == 0:
                    algo,canPlay=get_algo()
                    winK=3
                    pygame.display.update()
                if canPlay == 1 and gameNo == 1:
                    screen = pygame.display.set_mode((screenSize,screenSize))
                    board = [[None, None, None], [None, None, None], [None, None, None]]
                    currentPlayer = 'X'
                    screen.fill(backgroundColor)
                    draw_lines(grid)
            if event.key == pygame.K_2:
                if gameNo == 0:
                    gameNo=2
                    grid = get_grid()
                    winK = get_winK(grid)
                if algo == 0 and canPlay == 0:
                    algo,canPlay=get_algo()
                    pygame.display.update()
                if canPlay == 1 and gameNo == 2:
                    screen = pygame.display.set_mode((screenSize,screenSize))
                    board = [[None for i in range(grid)] for j in range(grid)]
                    currentPlayer = 'X'
                    screen.fill(backgroundColor)
                    draw_lines(grid)
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
    pygame.display.update()  
    
        

        
        


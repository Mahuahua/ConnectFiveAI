
from graphics import *

def main():
    aWindow=GraphWin("Connect 5",250,300)
    p1=Point(120,120)
    r1=Rectangle(Point(p1.getX()-40,p1.getY()-10),Point(p1.getX()+40,p1.getY()+10))
    r1.draw(aWindow)
    t1=Text(p1,"One Player")
    t1.draw(aWindow)
    p2=Point(120,150)
    t2=Text(p2,"Two Player")
    t2.draw(aWindow)
    r2=Rectangle(Point(p2.getX()-40,p2.getY()-10),Point(p2.getX()+40,p2.getY()+10))
    r2.draw(aWindow)

    mouse=aWindow.getMouse()
    while(not checkClick(p1,mouse) and not checkClick(p2,mouse)):
        mouse=aWindow.getMouse()
    if(checkClick(p1,mouse)):
        AI=1
    if(checkClick(p2,mouse)):
        AI=0
    aWindow.close()

    board=GraphWin("Connect 5 board",600,600) #opening a new form and drawing the board
    board.setCoords(0,0,15,15)
    for i in range(0,15):
        hLine=Line(Point(0,i),Point(15,i))
        hLine.draw(board)
        vLine=Line(Point(i,0),Point(i,15))
        vLine.draw(board)
    grid=[]
    for i in range(0,15):   #creating 2D array
        grid.append([])
        for j in range(0,15):
            grid[i].append(0)

    turn=1
    mouse=board.getMouse() #get mouse input
    mouse=Point(14-int(mouse.getX()),int(mouse.getY()))
    px=int(mouse.getX())
    py=int(mouse.getY())
    #wait(0.1)
    while(1):#getting mouse input,drawing to screen
        if(turn):   
            turn=0
        else:
            turn=1
        if(CheckValid(grid,px,py)):
            if(turn):
                SketchCircle(px,py,board)
            else:
                SketchX(mouse.getX(),mouse.getY(),board)
            UpdateArray(grid,px,py,turn+1)
        else:
            if(turn):   
                turn=0
            else:
                turn=1
        if(CheckWin(grid,px,py)):
            break
        if(checkTie(grid)):
            break
        if(AI and turn==0):
            move=getplay(grid)
            px=move/15
            py=move%15
        else:
            mouse=board.getMouse()
            mouse=Point(14-int(mouse.getX()),int(mouse.getY())) 
            px=int(mouse.getX())
            py=int(mouse.getY())
        #wait(0.1)
    #board.close()
    if(checkTie(grid)):
        win="Tie"
    elif(grid[px][py]==1):
        win="Player 1 wins"
    else:
        win="Player 2 wins"
    WINdow=GraphWin(win,250,300)

    p1=Point(120,120)
    r1=Rectangle(Point(p1.getX()-40,p1.getY()-10),Point(p1.getX()+40,p1.getY()+10))
    r1.draw(WINdow)
    t1=Text(p1,"Again")
    t1.draw(WINdow)
    p2=Point(120,150)
    t2=Text(p2,"Quit")
    t2.draw(WINdow)
    r2=Rectangle(Point(p2.getX()-40,p2.getY()-10),Point(p2.getX()+40,p2.getY()+10))
    r2.draw(WINdow)

    mouse=WINdow.getMouse()
    while(not checkClick(p1,mouse) and not checkClick(p2,mouse)):
        mouse=WINdow.getMouse()

    
    board.close();
    WINdow.close()
    
    if(checkClick(p1,mouse)):
        print win
        main()
    if(checkClick(p2,mouse)):
        print win
        
    

def checkClick(p,x):
    if(x.getX()<p.getX()-40 or x.getX()>p.getX()+40):
        return 0
    if(x.getY()<p.getY()-10 or x.getY()>p.getY()+10):
        return 0
    return 1    

def SketchX(x,y,board):
    x=14-x
    l1=Line(Point(x,y),Point(x+1,y+1))
    l1.draw(board)
    l2=Line(Point(x,y+1),Point(x+1,y))
    l2.draw(board)

def SketchCircle(x,y,board):
    x=14-x+0.5
    y+=0.5
    c1=Circle(Point(x,y),0.5)
    c1.draw(board)

def CheckValid(array,x,y):#player should be 1 or 2. 0 in the array means no piece. 
    if (x<0 or x>14 or y<0 or y>14 or array[x][y]!=0):
        return 0
    else:
        return 1

def UpdateArray(array,x,y, player):#checks for valid mod. if valid, update that piece
    if (CheckValid(array,x,y)==1):
        array[x][y]=player
        return 1
    else:
        return 0

def CheckWin(array,x,y):#return 1 for win and 0 for lose
    horizontal=0
    hLeft=0
    hRight=0

    vertical=0
    vTop=0
    vBottom=0

    diag1=0
    d1Left=0
    d1Right=0
    
    diag2=0
    d2Left=0
    d2Right=0

    player=array[x][y]
    for i in range (0,5):
        ##horizontal
        if (x-i>=0 and hLeft==0):
            if (array[x-i][y]==player):
                horizontal=horizontal+1
            else:
                hLeft==1
        if (x+i<15 and hRight==0):
            if (array[x+i][y]==player):
                horizontal=horizontal+1
            else:
                hRight==1
        ##vertical
        if (y-i>=0 and vTop==0):
            if (array[x][y-i]==player):
                vertical=vertical+1
            else:
                vTop==1
        if (y+i<15 and vBottom==0):
            if (array[x][y+i]==player):
                vertical=vertical+1
            else:
                vBottom==1
        ##diagonal \
        if (x-i>=0 and y-i>=0 and d1Left==0):
            if (array[x-i][y-i]==player):
                diag1=diag1+1
            else:
                d1Left==1
        if (x+i<15 and y+i<15 and d1Right==0):
            if (array[x+i][y+i]==player):
                diag1=diag1+1
            else:
                d1Right==1
        ##diagonal inverse /
        if (x-i>=0 and y+i<15 and d2Right==0):
            if (array[x-i][y+i]==player):
                diag2=diag2+1
            else:
                d2Right==1
        if (x+i<15 and y-i>=0 and d2Left==0):
            if (array[x+i][y-i]==player):
                diag2=diag2+1
            else:
                d2Left==1
    if (horizontal>5 or vertical>5 or diag1>5 or diag2>5):
        return 1
    else:
        return 0
    
def resetArray (array):
    for x in range (0,15):
        for y in range (0,15):
            array[x][y]=0
            
# of course i am lazy so if the board is filled it is a tie!
def checkTie (array):
    x=1
    for z in range (0,15):
        for y in range (0,15):
            if(array[z][y]==0):
                x=0
    return x

def calscore(array,c,maxscore):
    ans=0;
    for i in range (0,15):
      for j in range (0,15):
        if (array[i][j]==c):
        #free2 10
            #-
            if (i-1>=0 and i+2<15):
              if (array[i-1][j]==0 and array[i+1][j]==c and array[i+2][j]==0):
                  ans=ans+10;
            #|
            if (j-1>=0 and j+2<15):
              if (array[i][j-1]==0 and array[i][j+1]==c and array[i][j+2]==0):
                  ans=ans+10;
            #\
            if (j-1>=0 and j+2<15 and i-1>=0 and i+2<15):
              if (array[i-1][j-1]==0 and array[i+1][j+1]==c and array[i+2][j+2]==0):
                  ans=ans+10;
            #/
            if (j-1>=0 and j+2<15 and i+1<15 and i-2>=0):
              if (array[i+1][j-1]==0 and array[i-1][j+1]==c and array[i-2][j+2]==0):
                  ans=ans+10;
        #free3 30
            #-
            if (i-1>=0 and i+3<15):
              if (array[i-1][j]==0 and array[i+1][j]==c and array[i+2][j]==c and array[i+3][j]==0):
                  ans=ans+30;
            #|
            if (j-1>=0 and j+3<15):
              if (array[i][j-1]==0 and array[i][j+1]==c and array[i][j+2]==c and array[i][j+3]==0):
                  ans=ans+30;
            #\
            if (j-1>=0 and j+3<15 and i-1>=0 and i+3<15):
              if (array[i-1][j-1]==0 and array[i+1][j+1]==c and array[i+2][j+2]==c and array[i+3][j+3]==0):
                  ans=ans+30;
            #/
            if (j-1>=0 and j+3<15 and i+1<15 and i-3>=0):
              if (array[i+1][j-1]==0 and array[i-1][j+1]==c and array[i-2][j+2]==c and array[i-3][j+3]==0):
                  ans=ans+30;
        #free4 99
            #-
            if (i-1>=0 and i+4<15):
              if (array[i-1][j]==0 and array[i+1][j]==c and array[i+2][j]==c and array[i+3][j]==c and array[i+4][j]==0):
                  ans=ans+99;
            #|
            if (j-1>=0 and j+4<15):
              if (array[i][j-1]==0 and array[i][j+1]==c and array[i][j+2]==c and array[i][j+3]==c and array[i][j+4]==0):
                  ans=ans+99;
            #\
            if (j-1>=0 and j+4<15 and i-1>=0 and i+4<15):
              if (array[i-1][j-1]==0 and array[i+1][j+1]==c and array[i+2][j+2]==c and array[i+3][j+3]==c and array[i+4][j+4]==0):
                  ans=ans+99;
            #/
            if (j-1>=0 and j+4<15 and i+1<15 and i-4>=0):
              if (array[i+1][j-1]==0 and array[i-1][j+1]==c and array[i-2][j+2]==c and array[i-3][j+3]==c and array[i-4][j+4]==0):
                  ans=ans+99;
        #free5 9999
            #-
            if (i+4<15):
              if (array[i+1][j]==c and array[i+2][j]==c and array[i+3][j]==c and array[i+4][j]==c):
                  ans=ans+9999;
            #|
            if (j+4<15):
              if (array[i][j+1]==c and array[i][j+2]==c and array[i][j+3]==c and array[i][j+4]==c):
                  ans=ans+9999;
            #\
            if (j+4<15 and i+4<15):
              if (array[i+1][j+1]==c and array[i+2][j+2]==c and array[i+3][j+3]==c and array[i+4][j+4]==c):
                  ans=ans+9999;
            #/
            if (j+4<15 and i+1<15):
              if (array[i-1][j+1]==c and array[i-2][j+2]==c and array[i-3][j+3]==c and array[i-4][j+4]==c):
                  ans=ans+9999;
    if (c==2):#minus avreage moves by the user after the move
         if (ans<maxscore):
              return maxscore-1
         maxs=0
         score=0
         for i in range (0,15):
           for j in range (0,15):
             if (array[i][j]==0):
               array[i][j]=1
               score=calscore(array,1,maxscore)
               array[i][j]=0
               if (maxs<score):
                 maxs=score
         return ans-maxs*0.85
    return ans
def alone(array,x,y):
    for i in range (x-2,x+2):
        for j in range (y-2,y+2):
            if (i!=j and i>=0 and i<15 and j>=0 and j<15):
               if (array[i][j]!=0):
                   return 1
    return 0
def getplay(array):
    maxscore=-9999999
    score=0;
    ans=0;
    for i in range (0,15):
      for j in range (0,15):
        score=score+array[i][j];
    if (score==1):
       for i in range (0,15):
         for j in range (0,15):
            if (array[i][j]==1):
               if (i-1>0):
                   return (i-1)*15+j
               return (i+1)*15+j
    for i in range (0,15):
      for j in range (0,15):
         if (array[i][j]==0):
          if (alone(array,i,j)==1):
            array[i][j]=2
            score=calscore(array,2,maxscore)
            array[i][j]=0
            if (maxscore<score):
                  maxscore=score
                  ans=i*15+j
    return ans

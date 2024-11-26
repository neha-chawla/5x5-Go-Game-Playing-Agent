from copy import deepcopy
import numpy as np
import random
import ast
import time

class GamePlayer:
    def __init__(self):
        self.started = False
        self.tr = {}
        self.maxv = -1
        self.minv = 1
        self.templist = []
        self.xmove = None
        self.ymove = None
        self.oppxmove = None
        self.oppymove = None
        self.mt = {}
        self.rt = [[]]
        
    # i referenced the provided host.py when i made this function
    def findallies(self, temp, i, j, player):
        allies = [(i,j)] # visited
        queue = [(i,j)]
        while queue:
            piece = queue.pop(0)
            x, y = piece[0], piece[1]
            if x-1 >= 0:
                if temp[x-1][y] == player and (x-1,y) not in allies:
                    queue.append((x-1,y))
                    allies.append((x-1,y))
            if y-1 >= 0:
                if temp[x][y-1] == player and (x,y-1) not in allies:
                    queue.append((x,y-1))
                    allies.append((x,y-1))
            if x+1 <= 4:
                if temp[x+1][y] == player and (x+1,y) not in allies:
                    queue.append((x+1,y))
                    allies.append((x+1,y))
            if y+1 <= 4:
                if temp[x][y+1] == player and (x,y+1) not in allies:
                    queue.append((x,y+1))
                    allies.append((x,y+1))
        return allies
    
    # i referenced the provided host.py when i made this function
    def liberty(self, temp, allies):
        for piece in allies:
            x, y = piece[0], piece[1]
            neighbors = 0
            if x-1 >= 0:
                if temp[x-1][y] == 0:
                    neighbors +=1
            if y-1 >= 0:
                if temp[x][y-1] == 0:
                    neighbors +=1
            if x+1 <= 4:
                if temp[x+1][y] == 0:
                    neighbors +=1
            if y+1 <= 4:
                if temp[x][y+1] == 0:
                    neighbors +=1
            if neighbors > 0:
                return True
        return False

    def valid(self, i, j, previous_board, board, player):
        temp = []
        temp = deepcopy(board)
        # invalidate positions that already have pieces
        if temp[i][j] == 1 or temp[i][j] == 2:
            return False

        temp[i][j] = player
        # remove pieces that would be eliminated by the piece being played
        removelist = []
        for a in range(5):
            for b in range(5):
                if temp[a][b] != 0 and self.liberty(temp, self.findallies(temp, a, b, temp[a][b])) == False and temp[a][b] != player:
                    removelist.append((a,b))
        for toremove in removelist:
            x = toremove[0]
            y = toremove[1]
            temp[x][y] = 0
        # enforce ko rule
        if temp == previous_board:
            return False

        # find piece's allies
        allies = self.findallies(temp, i, j, player)
        # find if the piece would still have liberties after being placed            
        if self.liberty(temp, allies):
            return True
        return False

    def findpossibilities(self, board, previous_board, player):
        possibilities = []
        for i in range(5):
            for j in range(5):
                if(self.valid(i, j, previous_board, board, player)):
                    possibilities.append((i,j))
        return possibilities

    def getplayedmoves(self):
        movefile = open("moves.txt", "r")
        movelines = len(movefile.readlines())
        movefile.close()
        return movelines

    def game_end(self, board, prevboard, turn, moves):
        movelines = self.getplayedmoves()
        if movelines + moves >= 24:
            return True
        if self.findpossibilities(board, prevboard, 1) == [] and self.findpossibilities(board, prevboard, 2) == []:
            return True
        return False

    def judge_winner(self, board, player):
        # player 2, player 1
        cnt = [2.5, 0]
        for i in range(5):
            for j in range(5):
                if board[i][j] == 1:
                    cnt[1] += 1
                if board[i][j] == 2:
                    cnt[0] += 1
        if cnt[1] > cnt[0]: return 1, cnt[2-player], cnt[player-1]
        elif cnt[1] < cnt[0]: return 2, cnt[2-player], cnt[player-1]
        else: return 0, cnt[2-player], cnt[player-1]
    
    def findbestwall(self, board, player, length, possibilities):
        numpieces = 0
        for i in range(5):
            for j in range(5):
                if board[i][j] != 0:
                    numpieces +=1
        if (numpieces == 0 or numpieces == 1):
            if (2,2) in possibilities:
                wallfile = open("wallfile.txt", "w")
                wallfile.write("(2,2)\n(2,2)")
                wallfile.close()
                return 2, 2
            elif (2,1) in possibilities:
                wallfile = open("wallfile.txt", "w")
                wallfile.write("(2,1)\n(2,1)")
                wallfile.close()
                return 2, 1
        else: 
            wallfile = open("wallfile.txt", "r")
            findedges = wallfile.readlines()
            leftedge = ast.literal_eval(findedges[0])
            rightedge = ast.literal_eval(findedges[1])
            wallfile.close()
            leftx = leftedge[0]
            lefty = leftedge[1]
            rightx = rightedge[0]
            righty = rightedge[1]
            leftallies = self.numlibs(board, leftx, lefty)
            rightallies = self.numlibs(board, rightx, righty)
            if leftx == 0 and rightx == 4:
                return None, None
            if leftx != 0 and (abs(leftx-2) <= abs(rightx-2)):
                if (leftx-1, lefty) in possibilities:
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx-1, lefty)) + "\n" + str((rightx, righty)))
                    wallfile.close()
                    return leftx-1, lefty
                elif (leftx-1, lefty-1) in possibilities and ((self.numlibs(board, leftx-1, lefty-1) <= self.numlibs(board, leftx-1, lefty+1)) or ((leftx-1, lefty+1) not in possibilities)):
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx-1, lefty-1)) + "\n" + str((rightx, righty)))
                    wallfile.close()
                    return leftx-1, lefty-1
                elif (leftx-1, lefty+1) in possibilities:
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx-1, lefty+1)) + "\n" + str((rightx, righty)))
                    wallfile.close()
                    return leftx-1, lefty+1
            else: 
                if (rightx+1, righty) in possibilities:
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx, lefty)) + "\n" + str((rightx+1, righty)))
                    wallfile.close()
                    return rightx+1, righty
                elif (rightx+1, righty+1) in possibilities and ((self.numlibs(board, rightx+1, righty+1) <= self.numlibs(board, rightx+1, righty-1)) or ((rightx+1, righty-1) not in possibilities)):
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx, lefty)) + "\n" + str((rightx+1, righty+1)))
                    wallfile.close()
                    return rightx+1, righty+1
                elif (rightx+1, righty-1) in possibilities:
                    wallfile = open("wallfile.txt", "w")
                    wallfile.write(str((leftx, lefty)) + "\n" + str((rightx+1, righty-1)))
                    wallfile.close()
                    return rightx+1, righty-1
                return None, None
    
    def numlibs(self, board, x, y):
        neighbors = 0
        if x-1 >= 0:
            if board[x-1][y] == 0:
                neighbors +=1
        if y-1 >= 0:
            if board[x][y-1] == 0:
                neighbors +=1
        if x+1 <= 4:
            if board[x+1][y] == 0:
                neighbors +=1
        if y+1 <= 4:
            if board[x][y+1] == 0:
                neighbors +=1
        return neighbors
    
    def max(self, board, prevboard, player, moves, minscore, maxscore, minoppscore, maxoppscore, depth, tr, posslen, start, length):
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        result = self.game_end(board, prevboard, player, moves)
        possibilities = self.findpossibilities(board, prevboard, player)

        stopping = (25-posslen)/4
        if result or possibilities == [] or (depth >= stopping and stopping >= (1+player)) or (depth >= (1+player) and stopping <= (1+player)):
            winner, score, oppscore = self.judge_winner(board, player)
            if winner == opponent:
                return (-1, score, oppscore, None, None, [])
            elif winner == player:
                return (1, score, oppscore, None, None, [])
            elif winner == 0:
                return (0, score, oppscore, None, None, [])
            print("not classified")

        px = None
        py = None
        _maxv = -1
        _maxscore = 0
        _minoppscore = 14.5
        
        if depth == 0 and length < 10:
            i, j = self.findbestwall(board, player, length, possibilities)
            if i != None and j != None:
                return (None, None, None, i, j, None)
        
        for p in possibilities:
            temp = deepcopy(board)
            i = p[0]
            j = p[1]
            if temp[i][j] == 0:
                # remove dead pieces
                temp[i][j] = player
                removelist = []
                for a in range(5):
                    for b in range(5):
                        if self.liberty(temp, self.findallies(temp, a, b, temp[a][b])) == False and temp[a][b] == opponent:
                            removelist.append((a,b))
                for toremove in removelist:
                    x = toremove[0]
                    y = toremove[1]
                    temp[x][y] = 0
                (m, score, oppscore, min_i, min_j, path) = self.min(temp, board, player, moves+1, minscore, maxscore, minoppscore, maxoppscore, depth+1, tr, posslen, start, length)
                if px == None:
                    _maxv = m
                    px = i
                    py = j
                    temppath = deepcopy(path)
                    temppath.append((i, j, deepcopy(temp)))
                if (m >= _maxv and score >= _maxscore and oppscore < _minoppscore) or (m >= _maxv and score > _maxscore and oppscore <= _minoppscore):
                    _minoppscore = oppscore
                    _maxscore = score
                    _maxv = m
                    px = i
                    py = j
                    temppath = deepcopy(path)
                    temppath.append((i, j, deepcopy(temp)))
                if (_maxscore > minscore or _minoppscore < maxoppscore) or (_maxscore == minscore and _minoppscore == maxoppscore) or time.time() - start >= 9.8: 
                    return (_maxv, _maxscore, _minoppscore, px, py, temppath)
                if (_maxscore >= maxscore and _minoppscore < minoppscore) or (_maxscore > maxscore and _minoppscore <= minoppscore):
                    maxscore = _maxscore
                    minoppscore = _minoppscore
        return (_maxv, _maxscore, _minoppscore, px, py, temppath)

    
    def min(self, board, prevboard, player, moves, minscore, maxscore, minoppscore, maxoppscore, depth, tr, posslen, start, length):
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1

        result = self.game_end(board, prevboard, opponent, moves)
        possibilities = self.findpossibilities(board, prevboard, opponent)

        stopping = (25-posslen)/4
        if result or possibilities == [] or (depth >= stopping and stopping >= (1+player)) or (depth >= (1+player) and stopping <= (1+player)):
            winner, score, oppscore = self.judge_winner(board, player)
            if winner == opponent:
                return (-1, score, oppscore, None, None, [])
            elif winner == player:
                return (1, score, oppscore, None, None, [])
            elif winner == 0:
                return (0, score, oppscore, None, None, [])

        _minv = 1
        qx = None
        qy = None
        _minscore = 14.5
        _maxoppscore = 0
        
        for p in possibilities:
            temp = deepcopy(board)
            i = p[0]
            j = p[1]
            if temp[i][j] == 0:
                temp[i][j] = opponent
                removelist = []
                for a in range(5):
                    for b in range(5):
                        if self.liberty(temp, self.findallies(temp, a, b, temp[a][b])) == False and temp[a][b] == player:
                            removelist.append((a, b))
                for toremove in removelist:
                    x = toremove[0]
                    y = toremove[1]
                    temp[x][y] = 0
                (m, score, oppscore, max_i, max_j, path) = self.max(temp, board, player, moves+1, minscore, maxscore, minoppscore, maxoppscore, depth+1, tr, posslen, start, length)
                if qx == None:
                    qx = i
                    qy = j
                    temppath = deepcopy(path)
                    temppath.append((i, j, deepcopy(temp)))
                if (m <= _minv and score <= _minscore and oppscore > _maxoppscore) or (m <= _minv and score < _minscore and oppscore >= _maxoppscore):
                    _maxoppscore = oppscore
                    _minscore = score
                    _minv = m
                    qx = i
                    qy = j
                    temppath = deepcopy(path)
                    temppath.append((i,j,deepcopy(temp)))
                if (_minscore < maxscore or _maxoppscore > minoppscore) or (_minscore == maxscore and _maxoppscore == minoppscore) or time.time() - start >= 9.8:   
                    return (_minv, _minscore, _maxoppscore, qx, qy, temppath)
                if (minscore > _minscore and maxoppscore <= _maxoppscore) or (minscore >= _minscore and maxoppscore < _maxoppscore):
                    minscore = _minscore
                    maxoppscore = _maxoppscore
        return (_minv, _minscore, _maxoppscore, qx, qy, temppath)

# main function
def main():
    infile = open("input.txt", "r")
    inputlines = infile.readlines()
    player = int(inputlines[0].strip())
    previous_board = [[int(i) for i in line.rstrip('\n')] for line in inputlines[1:6]]
    board = [[int(x) for x in line.rstrip('\n')] for line in inputlines[6:11]]
    gameplayer = GamePlayer()
    tr = {}
    infile.close()
    movefile = open("moves.txt", "a")
    if np.sum(board) == 0 or np.sum(board) == 1:
        movefile.truncate(0)
    movefile.close()
    movefile = open("moves.txt", "r")
    length = len(movefile.readlines())
    movefile.close()
    with open("moves.txt", "a") as movefile:
        if length > 0:
            movefile.write("\nmove")
        if length == 0 and player == 2:
            length = length+1
            movefile.write("move")
    movefile.close()
    possibilities = gameplayer.findpossibilities(board, previous_board, player)
    
    # if there are no possible positions, pass
    outfile = open("output.txt", "w") 
    if not possibilities:
        outfile.write("PASS")
        outfile.close() 
        return
    
    # else return the best possible position
    curr_max = -2
    row, col = -1, -1
    
    moves = 0
    start = time.time()
    (m, score, oppscore, px, py, path) = gameplayer.max(board, previous_board, player, moves, 14.5, 0, 14.5, 0, 0, tr, len(possibilities), start, length)
    row = px
    col = py

    moves = 0
    selectedmove = (row, col)
    
    with open("moves.txt", "a") as movefile:
        if length > 0:
            movefile.write("\n")
        movefile.write("move")
        movefile.close()
        if row != None:
            prev = deepcopy(board)
            board[row][col] = player
        if gameplayer.game_end(board, prev, player, 0):
            print("true")

    outfile = open("output.txt", "w") 
    if selectedmove == (None, None):
        outfile.write("PASS")
    else:
        outfile.write(str(selectedmove[0]) + "," + str(selectedmove[1]))
    outfile.close() 
    return

# call main function    
if __name__ == "__main__":
    main()   

import numpy as np
import time, random, copy

f = open("input.txt", "r")
read = f.read().splitlines()
f.close()
board = [] 
boardN = int(read[0]) #height of the square boardN (0 < n <= 26)
fruitN = int(read[1]) # number of fruit types (0 <= p <= 9)
timeS = float(read[2]) #remaining time in seconds (+floating point #)
for i in range(3,int(boardN+3)): #0 to p-1 or *
    board.append(list(read[i]))
startTime = time.time()

def gravity():
    indices = []
    for i in range(1, boardN):
        for j in range(boardN):
            if board[i][j] == "*":
                indices.append((i, j))
    for r,c in indices:
        for i in range(r, 0, -1):
            board[i][c] = board[i-1][c]
        board[0][c] = '*'
    return board

def checkFruits(board, point, fruitVal):
    check = []
    if point[0] == boardN-1 and point[1] == boardN-1: #ex. (3,3)
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
    elif point[0] == 0 and point[1] == 0: #ex. (0,0)
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1]) 
    elif point[0] == 0 and point[1] == boardN-1: #ex. (0,3)
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
    elif point[0] == boardN-1 and point[1] == 0: #ex. (3,0)
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1])
    elif point[0] == boardN-1: #ex. (3,2)
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
    elif point[1] == boardN-1: #ex(1, 3)
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
    elif point[0] == 0: #ex. (0,1)
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1])
    elif point[1] == 0: #ex(1,0)
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1])
    else:
        if board[point[0]-1][point[1]] == fruitVal:
            check.append([point[0]-1,point[1]])
        if board[point[0]+1][point[1]] == fruitVal:
            check.append([point[0]+1,point[1]])
        if board[point[0]][point[1]-1] == fruitVal:
            check.append([point[0],point[1]-1])
        if board[point[0]][point[1]+1] == fruitVal:
            check.append([point[0],point[1]+1])
    return check

def pickupFruits(fruitList): 
    cboard = copy.deepcopy(board)
    score = 0 
    for fruit in fruitList:
        fruit_ = [fruit]
        for i in fruit_:
            for j in range(len(i)):
                point = i[j]
                fruitVal = cboard[point[0]][point[1]]
                cboard[point[0]][point[1]] = '*'
        for r,c in fruit:
            for i in range(r, 0, -1):
                cboard[i][c] = cboard[i-1][c]
            cboard[0][c] = '*'
    return cboard

def fruitPositions(board):
    fruit = []
    tempList = []
    for i in range(boardN-1, -1,-1):
        for j in range(boardN-1, -1,-1):
            if board[i][j] != '*':
                tempList.append([i,j])
    while tempList:
        point = tempList.pop()
        fruitVal = board[point[0]][point[1]]
        check = checkFruits(board, point, fruitVal)
        temp = []
        if check:
            temp.append(point)
            while check:
                point = check.pop()
                if point not in temp:
                    temp.append(point)
                    check += checkFruits(board, point, fruitVal)
            for i in temp:
                if i in tempList:
                    tempList.remove(i)
            fruit.append(temp)
        else:
            fruit.append([point])
    for i in fruit:
        i.append(len(i))
    fruit = sorted(fruit, key=lambda i: i[-1], reverse=True)
    for i in range(len(fruit)):
        fruit[i].remove(fruit[i][-1])
    return fruit

def depthValue(fruitLength):
    if fruitN == 1:
        depthVal = ((boardN*2)*(timeS))/((fruitLength)*(boardN/2))
    else:
        if boardN <= 10:
            depthVal = ((boardN*2)*(timeS*0.6))/((fruitLength)*(boardN/2))
        elif boardN > 10 and boardN <= 15:
            depthVal = ((boardN*2)*(timeS*0.5))/((fruitLength)*(boardN/2))
        else:
            depthVal = ((boardN*2)*(timeS*0.4))/((fruitLength)*(boardN/2))
    remaining = depthVal - int(depthVal)
    if remaining >= 0.7:
        depthVal = int(depthVal) + 1
    else:
        depthVal = int(depthVal)
    if depthVal <= 1:
        depthVal = 2
    return depthVal

def play():
    playTime = time.time()
    if boardN == 1:
        fruit = [[[0,0]]]
    else:
        fruit = minimax()
    fruit[0].sort()
    endTime = time.time()-playTime
    writeFile(fruit)
    return

def minimax():
    miniTime = time.time()
    board = gravity()
    fruitList = fruitPositions(board) 
    fruitLength = len(fruitList)
    bestFruit = [[fruitList[0][0]]]
    bestScore = float('-inf')
    beta = float('inf')
    depthVal = depthValue(fruitLength)
    for fruit in fruitList:
        if time.time() > (timeS*0.4) + startTime:
            return bestFruit
        countList = []
        fruitChoice = copy.deepcopy(fruit)
        depth = depthVal
        count = len(fruit)
        countList.append(count)
        score = min_play([fruit], bestScore, beta, depth-1, countList)
        if score > bestScore:
            bestFruit = [fruitChoice]
            bestScore = score
    return bestFruit

def min_play(parent, alpha, beta, depth, countListP):
    parent[0].sort()
    tempBoard = pickupFruits(parent)
    fruitList = fruitPositions(tempBoard)
    if len(fruitList) == 0 or depth == 0:
        point = 0
        for i in range(len(countListP)):
            if i%2 == 0:
                point += countListP[i]**2
            else:
                point -= countListP[i]**2
        return point
    score = float('inf')
    for fruit in fruitList:
        countList = []
        countList += countListP
        parent.append(fruit)
        count = len(fruit)
        countList.append(count)
        score = min(score, max_play(parent, alpha, beta, depth-1, countList))
        if score <= alpha:
            return score
        beta = min(beta, score)
    return score

def max_play(parent, alpha, beta, depth, countListP):
    parent[0].sort()
    tempBoard = pickupFruits(parent)
    fruitList = fruitPositions(tempBoard)
    if len(fruitList) == 0 or depth == 0:
        point = 0
        for i in range(len(countListP)):
            if i%2 == 0:
                point += countListP[i]**2
            else:
                point -= countListP[i]**2
        return point
    score = float('-inf')
    for fruit in fruitList:
        countList = []
        countList += countListP
        parent.append(fruit)
        count = len(fruit)
        countList.append(count)
        score = max(score, min_play(parent, alpha, beta, depth-1, countList))   
        if score >= beta:
            return score
        alpha = max(alpha, score)
    return score

def letterNumber(fruit):
    res = []
    choices = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K',
                 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U',
                 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'
                }
    for r,c in fruit:
        c = choices.get(c, 0)
        res.append(c)
        r += 1
        r = str(r)
        res.append(r)
        res = ''.join(res)
    return res

def writeFile(fruit):
    choice = letterNumber([fruit[0][0]])
    for i in fruit:
        for j in range(len(i)):
            point = i[j]
            board[point[0]][point[1]] = '*'
    for r,c in fruit[0]:
        for i in range(r, 0, -1):
            board[i][c] = board[i-1][c]
        board[0][c] = '*'
    data = np.array(board)
    f = open("output.txt", "w")
    f.write(choice + "\n")
    for i in range(boardN):
        for j in range(boardN):
            f.write(board[i][j])
        f.write("\n")
    f.close()
    exit()
    return

if __name__ == '__main__':
        play()
    
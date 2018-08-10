import numpy as np
from operator import itemgetter
from collections import deque
import time, random, math

def bfs(size,liz,tree):
    solution, queue = [] , deque([])
    queue = push(queue, tree, size, liz)

    timeout = time.time() + 270
    while queue:
        if time.time() > timeout: 
            break 
        nursery = queue.popleft()
        row = len(nursery)
        if row == liz:
            solution.append(nursery)
            return solution
        queue = before_checking_dfs_bfs(nursery, solution, liz, size, tree, queue)
    return solution

def dfs(size,liz,tree):
    solution, stack = [] , []
    stack = push(stack, tree, size, liz)
                
    timeout = time.time() + 270
    while stack:
        if time.time() > timeout: 
            break 
        nursery = stack.pop()
        row = len(nursery)
        if row == liz:
            solution.append(nursery)
            return solution
        stack = before_checking_dfs_bfs(nursery, solution, liz, size, tree, stack)
    return solution

def sa(size,liz,tree):
    solution, nursery = [], []
    initial_timeout = time.time() + 10
    timeout = time.time() + 270
    costPrev = liz
    temperature = 1.0
    temperatureMin = 0.00001
    alpha = 0.9999
    i = 0
    if not tree and size < liz:
        return solution
    while i < liz:
        if time.time() > initial_timeout:
            return solution 
            break 
        row,col = random.randint(0, size-1), random.randint(0, size-1)
        if not tree.count([row,col]):
            if not nursery.count([row,col]):
                nursery.append([row,col])
                i += 1
    countTrue = []
    while temperature > temperatureMin:
        if time.time() > timeout: 
            return solution
            break 
        if costPrev == 0:
            break

        temp= []
        i=0
        if len(countTrue) > 0:
            for i in countTrue:
                temp.append(i)
            i = len(countTrue)
            while i < liz -1:
                randN = random.randint(0,len(nursery)-1)
                if not temp.count(nursery[randN]):
                    temp.append(nursery[randN])
                    i += 1
            while i < liz:
                row, col = random.randint(0, size-1), random.randint(0, size-1)
                if not tree.count([row,col]):
                    if not temp.count([row,col]):
                        temp.append([row,col])
                        i +=1
        else:
            while i < liz:
                row,col = random.randint(0, size-1), random.randint(0, size-1)
                if not tree.count([row,col]):
                    if not temp.count([row,col]):
                        temp.append([row,col])
                        i += 1
        countTrue = trueCount(temp, tree, liz)
        costNew = cost(temp, tree) 
        if costNew < costPrev:
            ap = 1.0
        else:
            ap = math.exp(-abs(costNew-costPrev)/temperature)

        if ap > random.random():
            nursery = temp 
            costPrev = costNew

        temperature *= alpha
    if costPrev == 0:
        solution.append(nursery)
        return solution
    else:
        solution = []
        return solution

def push(data, tree, size, liz):
    if not tree and size < liz:
        return solution
    for i in range(size):
        for j in range(size):
            if not tree.count([i, j]):
                data.append([[i,j]])     
    return data

def before_checking_dfs_bfs(nursery, solution, liz, size, tree, data):
    row = len(nursery)
    for col in range(size):
        for row in range(row+1):
            if row == size:
                break
            temp = []
            if not tree.count([row, col]):
                temp = checking(nursery, tree, row, col)
                if all(temp):
                    data.append(nursery+[[row, col]])
    return data

def checking(nursery, tree, row, col):
    temp = []
    for r, c in nursery:
        if (row != r and col != c and abs(row-r) != abs(col-c)):
            temp.append(True)              
        else :
            treetemp = [False]
            for tr, tc in tree:
                if row==tr==r and (col<tc<c or col>tc>c):
                    treetemp.append(col != c and abs(row-r) != abs(col-c))
                    break
                elif col==tc==c and (row<tr<r or row>tr>r):
                    treetemp.append(row != r and abs(row-r) != abs(col-c))
                    break
                elif abs(row-r) == abs(col-c) and (((row<tr<r and col>tc>c) or (row>tr>r and col<tc<c)) 
                                                or ((row<tr<r and col<tc<c) or (row>tr>r and col>tc>c))):
                    if (tr-row)/(tc-col) == (tr-r)/(tc-c):
                        treetemp.append(True)
                        break
                else:
                    treetemp.append(False)
            if any(treetemp):
                temp.append(True)
            else:
                temp.append(False) 
    return temp

def trueCount(nursery, tree, liz):
    count = []
    i = 0
    for row, col in nursery:
        temp = checking(nursery, tree, row, col)
        i += 1
        if temp.count(True) == liz-1:
            count.append(nursery[i-1])
    return count

def cost(nursery, tree):
    count = 0  
    for row, col in nursery:
        temp = checking(nursery, tree, row, col)
        if temp.count(False) > 1:    
            count += 1
    return count

def writeFile(nursery, size, liz, tree):     
    f = open("output.txt", "w")
    if len(nursery) is 0:
        f.write("FAIL")
        return 0
    else:
        f.write("OK\n")
        sort_nursery = sorted(sorted(nursery[0], key=itemgetter(1)), key=itemgetter(0))
        image = np.zeros((size, size))

        for r,c in sort_nursery:
            image[r,c] = 1
        for r,c in tree:
            image[r,c] = 2
        for i in range(size):
            for j in range(size):
                f.write(str(int(image[i][j])))
            f.write("\n")
        return 0
    f.close()

def readFile():
    f = open("input.txt", "r")
    read = f.read().splitlines()
    f.close()

    count = 0
    tree = []
    method = read[0]
    size = int(read[1])
    liz = int(read[2])
    for i in range(3,int(size+3)):
    	for j in range(int(size)):
            if read[i][j] == '2':
                tree.append([i-3,j])
      
    if method == 'DFS':
        writeFile(dfs(size,liz,tree), size, liz, tree)
    elif method == 'BFS':
        writeFile(bfs(size,liz,tree), size, liz, tree)
    elif method == 'SA':
        writeFile(sa(size,liz,tree), size, liz, tree)

if __name__ == '__main__':
        readFile()
    
from collections import deque
import heapq
import time
import json
#opposite library
opposite = {"U": "D", "D": "U", "L": "R", "R": "L"}

#tuples are (move,col,row)
def getChildren(currState):
    children = []
    #up
    if currState[1] - 1 >= 0:
        children.append(('U', currState[0], currState[1] - 1))
    #down
    if currState[1] + 1 <= 3:
        children.append(('D', currState[0], currState[1] + 1))
    #left
    if currState[0] - 1 >= 0:
        children.append(('L', currState[0] - 1, currState[1]))
    #right
    if currState[0] + 1 <= 3:
        children.append(('R', currState[0] + 1, currState[1]))
    return children


#make a new function called makeChildren
def makeChild(board, blankRow, blankCol, newRow, newCol):
    newBoard = [list(row2) for row2 in board]
    newBoard[blankRow][blankCol], newBoard[newRow][newCol] = newBoard[newRow][newCol], newBoard[blankRow][blankCol] 
    return tuple(tuple(row) for row in newBoard)

#search methods will track these variables and call output
#solutionFound is a bool 0 = success 1 = failure, 
def output(solutionFound, numMoves, sequence, statesRem, maxSize, time):
    if solutionFound == 0 :
        print('\nSolution found')
    elif solutionFound == 1:
        print('Solution not found')
    print(f'The number of moves: {numMoves} \nThe sequence of moves: {", ".join(sequence)} \n')
    print (f'The number of states removed: {statesRem} \nThe maximum size of the queue/stack: {maxSize} \nCPU time: {time}' )


#is solvable function
def isSolvable(start, goal):
    flatS = [t for row in start for t in row]
    flatG = [t for row in goal for t in row]
    if sorted(flatS) != sorted(flatG):
        return False
    posG = {t: i for i, t in enumerate(flatG)}
    perm = [posG[t] for t in flatS]
    #parity of the permutation = (16 - number of cycles) mod 2
    seen = [False] * 16
    cycles = 0
    for i in range(16):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    permParity = (16 - cycles) % 2
    #every move is one swap with the blank, so blank distance parity must match
    r1, c1 = findBlank(start)
    r2, c2 = findBlank(goal)
    blankParity = (abs(r1 - r2) + abs(c1 - c2)) % 2
    return permParity == blankParity


#finding empty space on the board
def findBlank(board):
     for row in range (4):
        for col in range(4):
            if board[row][col] == 0:
                 return row,col

#takes current empty space and coordinates to swap to and creates a new board with the swap
def swap(board, row, col, newRow, newCol):
    newBoard = [] 
    for r in board: 
        newBoard.append(r[:])
    newBoard[row][col], newBoard[newRow][newCol] = newBoard[newRow][newCol], newBoard[row][col] 
    return newBoard

#Best first search
def bestFirst(start, goal,h=lambda x: 0):


    #start and goal to a tuple of tuples
    start = tuple(tuple(row) for row in start)
    goal = tuple(tuple(row) for row in goal)

    g = {start: 0}                  #best known cost to each generated state
    parent = {start: None}          #state -> (parent state, move)
    counter = 0                     #tiebreaker so the heap never compares boards
    heap = [(h(start), counter, start)]
    openSet = {start}               #states currently in Open
    closed = set()   

    # remove is set to zero
    removed = 0
    #maxSize is set to 1
    maxSize = 1

    #while queue is not empty
    while openSet:
        #u is set to remove the first state from the queue
        f, _, board = heapq.heappop(heap)

        if board not in openSet or f!= h(board) + g[board]:
            continue

        openSet.remove(board)
        removed += 1

        #if u is equal to the goal state then we have found a solution
        if board == goal : 
            path = []
            while parent[board] is not None:
                board, move = parent[board]
                path.append(move)
            return "found", path[::-1], removed, maxSize

        closed.add(board)

        # otherwise fine the blank position
        blankRow, blankCol = findBlank(board)

        # for each legal move, state, new row, and new col from the blank
        for move, newCol, newRow in getChildren((blankCol, blankRow)):

            visitedState = makeChild(board, blankRow, blankCol, newRow, newCol)
            tentative_g = g[board] + 1

            if visitedState in closed:

                if tentative_g >= g[visitedState]:
                    continue
                closed.remove(visitedState)
                openSet.add(visitedState)
            elif visitedState in openSet:
                #already generated: only update if this path is cheaper
                if tentative_g >= g[visitedState]:
                    continue
            else:
                #never seen before
                openSet.add(visitedState)
 
            g[visitedState] = tentative_g
            parent[visitedState] = (board, move)
            counter += 1
            heapq.heappush(heap, (tentative_g + h(visitedState), counter, visitedState))
 
        #max size of the queue = size of open
        maxSize = max(maxSize, len(openSet))
    # return failure, removed, maxqueue
    return "failure", "", removed, maxSize
                
        



#Iterative deepening search
def ids(start, goal, maxDepth=80):

    totalRemoved = 0
    peakStack = 0

    #for depth = 0 to infinity do
    for limit in range(maxDepth+1):

        #result is set to the depth limited serach(problem, depth)
        result, path, removed, maxSize = dls(start, goal, limit)
        totalRemoved += removed
        peakStack = max(peakStack, maxSize)
        #if the result doesnt equal the cuttoff then return the result
        if result != "cutoff":
            return result, path, totalRemoved, peakStack
    return "cutoff", "", totalRemoved, peakStack
            

#Depth limited search
def dls(start, goal, limit):
        #make a stack to start the lifo process, copy down the puzzle/matrix from user
        stack = [(start,"", 0)]

        #counters
        nodes_removed = 0
        max_stackSize = 1
        result = "failure"

    
        #while frontier isnt empty
        while len(stack) > 0:
            #node is set to Pop (frontier) taking the top of the stack
            board, path, depth = stack.pop()
            nodes_removed += 1
            
            #if the depth(node > the limit then result is to cutoff)
            if board == goal:
                 return "found", path , nodes_removed, max_stackSize
            
            if depth >=limit:
                result = "cutoff"
                continue



            #finding the blank again 
            row, col = findBlank(board)

            #swapping
            for move, newCol, newRow in getChildren((col,row)):
            #get the goal state
                if move == opposite.get(path[-1:]):
                    continue

                #make a new board and push the correct boards together
                newBoard = [row2[:] for row2 in board]
                newBoard[row][col], newBoard[newRow][newCol] = newBoard[newRow][newCol], newBoard[row][col] 
                stack.append((newBoard, path + move, depth +1))
                
            max_stackSize = max(max_stackSize, len(stack))

                 
        #outside the loop return the result
        return result, "", nodes_removed, max_stackSize

def main():

    #json.loads takes out string and turns it into a python list of lists 
    #this allows us to directly pass it to functions
    startState = json.loads(input('Enter Start State: '))
    goalState = json.loads(input('Enter Goal State:'))

    startState = tuple(tuple(row) for row in startState)
    goalState = tuple(tuple(row) for row in goalState)

    #as it should look
    search = input ('Pick a search method by entering a number: \n (1)BFS \n (2)IDS \n (3)DLS \n (4)Compare all \n')

    #max amount a 4x4 grid can search
    limit = 80 

    #Breadth First Search
    if search == '1' or search == '(1)':
        print('You selected Best First Search')
        startTime = time.process_time()
        status, path, removed, maxSize = bestFirst(startState, goalState)
        elapsed = time.process_time() - startTime
        output(status,len(path), path, removed, maxSize, elapsed)

    #Iterative Deepening Search
    elif search == '2' or search == '(2)':
        #printout 
        print('You selected Iterative Deepening Search')
        startTime = time.process_time()
        status, path, removed, maxSize = ids(startState, goalState, limit)
        elapsed = time.process_time() - startTime

        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed)
        else:
            output(1,0,"none",removed, maxSize, elapsed)

    #Depth Limited Search
    elif search == '3' or search == '(3)':
        #printout
        print('You selected Depth Limited Search') 
        startTime = time.process_time()
        status, path, removed, maxSize = dls(startState, goalState, limit)
        elapsed = time.process_time() - startTime


        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed)
        else:
            output(1,0,"none",removed, maxSize, elapsed)   

    #comparing all searches    
    elif search == '4' or search == '(4)':
        print('You selected to compare all searches')


        print('\nBest First Search Stats:')
        startTime1 = time.process_time()
        status, path, removed, maxSize = bestFirst(startState, goalState)
        elapsed1 = time.process_time() - startTime1
        output(status,len(path), path, removed, maxSize, elapsed1)

        print('\nIterative Deepening Search Stats:')
        startTime2 = time.process_time()
        status, path, removed, maxSize = ids(startState, goalState, limit)
        elapsed2 = time.process_time() - startTime2

        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed2)
        else:
            output(1,0,"none",removed, maxSize, elapsed2)

        print('Depth Limited Search Stats:') 
        startTime = time.process_time()
        status, path, removed, maxSize = dls(startState, goalState, limit)
        elapsed = time.process_time() - startTime
        
        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed)
        else:
            output(1,0,"none",removed, maxSize, elapsed)   

    
if __name__ == "__main__":
    main()



    
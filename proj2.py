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

#calculates Manhattan Distance 
def heuristic1(board, goal):
    total = 0
    for row in range(4):
        for col in range(4):
            tile = board[row][col] #iterate through board tiles
            if tile == 0:
                continue                     
            for goalRow in range(4):              
                for goalCol in range(4):
                    if goal[goalRow][goalCol] == tile: #find board tile in goal state
                        total += abs(row - goalRow) + abs(col - goalCol) #calculate the distance
    return total    

#grouping tiles to 2 different groups
def colorBoard(board):
    newBoard = [] #creates a new board for 
    for row in board:
        newRow = []
        for i in row:
            if i == 0:
                newRow.append(0)
            elif i <= 8:
                newRow.append(1)#Red
            else:
                newRow.append(2)#Green
        newBoard.append(tuple(newRow))
    return tuple(newBoard) #tuple so it can be hashable

#ids is performed to fill out patter database heuristic
def patterDataBase(goal):
    table = {}
    ids(colorBoard(goal), None, 80, table) 
    return table

#takes board state and refers to database
def heuristic2 (board, table):
    return table[colorBoard(board)]

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
def ids(start, goal, maxDepth=80, table=None):

    totalRemoved = 0
    peakStack = 0

    #for depth = 0 to infinity do
    for limit in range(maxDepth+1):
        sizeBefore = len(table) if table is not None else 0
        #result is set to the depth limited serach(problem, depth)
        result, path, removed, maxSize = dls(start, goal, limit, table)
        totalRemoved += removed
        peakStack = max(peakStack, maxSize)
        if table is None:
        #if the result doesnt equal the cuttoff then return the result
            if result != "cutoff":
                return result, path, totalRemoved, peakStack
        elif len(table) == sizeBefore:
            return "complete", "", totalRemoved, peakStack
    return "cutoff", "", totalRemoved, peakStack
            

#Depth limited search
def dls(start, goal, limit, table=None):
        #make a stack to start the lifo process, copy down the puzzle/matrix from user
    stack = [(start,"", 0)]

        #counters
    nodes_removed = 0
    max_stackSize = 1
    result = "failure"
    shallowest = {start: 0}

    
        #while frontier isnt empty
    while len(stack) > 0:
            #node is set to Pop (frontier) taking the top of the stack
        board, path, depth = stack.pop()
        nodes_removed += 1

        if table is None:
            #if the depth(node > the limit then result is to cutoff)
            if board == goal:
                return "found", path , nodes_removed, max_stackSize
        elif board not in table:
            table[board] = depth

        if depth >=limit:
            result = "cutoff"
            continue



            #finding the blank again 
        row, col = findBlank(board)

            #swapping
        for move, newCol, newRow in getChildren((col,row)):
            #get the goal state
            if table is None and move == opposite.get(path[-1:]):
                continue
                
            child = makeChild(board, row, col, newRow, newCol)
            if table is not None: #in table mode it skips all states already seen
                if child in shallowest and shallowest[child] <= depth + 1:
                    continue
                shallowest[child] = depth + 1
            stack.append((child, path + move, depth + 1))
        max_stackSize = max(max_stackSize, len(stack))
    return result, "", nodes_removed, max_stackSize                #make a new board and push the correct boards together

def main():


    #json.loads takes out string and turns it into a python list of lists 
    #this allows us to directly pass it to functions
    startState = json.loads(input('Enter Start State: '))
    goalState = json.loads(input('Enter Goal State: '))
 
    startState = tuple(tuple(row) for row in startState)
    goalState = tuple(tuple(row) for row in goalState)
 
    #the parity check tells us right away if the goal can never be reached
    solvable = isSolvable(startState, goalState)
    if not solvable:
        print('\nThis start/goal pair is unreachable, so no solution exists.')
 
    #one-time cost: build the pattern database for this goal (used by h2 and h3)
    startTime = time.process_time()
    table = patterDataBase(goalState)
    print(f'Pattern database built: {len(table)} states, CPU time {time.process_time() - startTime:.3f}')
 
    h1 = lambda board: heuristic1(board, goalState)
    h2 = lambda board: heuristic2(board, table)
    h3 = lambda board: max(h1(board), h2(board))
    heuristics = {'1': ('Manhattan Distance Heuristic', h1),
                  '2': ('Pattern Database Heuristic', h2),
                  '3': ('Max Heuristic', h3)}
 
    #loop through the options until 4 (halt) is chosen
    while True:
        choice = input('\nPick the algorithm(s) to run (any combination of 1, 2, 3, e.g. 123): \n'
                       ' (1) Best First Search with heuristic 1 \n'
                       ' (2) Best First Search with heuristic 2 \n'
                       ' (3) Best First Search with heuristic 3 \n'
                       ' (4) Halt \n').strip()
 
        if '4' in choice:
            print('Halting.')
            break
 
        #run the chosen options in order 1, 2, 3 (ignores repeats and other characters)
        picks = [c for c in '123' if c in choice]
        if not picks:
            print('Invalid choice, please enter 1, 2, 3 or 4.')
            continue
 
        for c in picks:
            name, h = heuristics[c]
            print(f'\nStarting Best First Search with {name}')
 
            if not solvable:
                output(1, 0, ["none"], 0, 0, 0.0)
                continue
 
            startTime = time.process_time()
            status, path, removed, maxSize = bestFirst(startState, goalState, h)
            elapsed = time.process_time() - startTime
 
            if status == "found":
                output(0, len(path), path, removed, maxSize, elapsed)
            else:
                output(1, 0, ["none"], removed, maxSize, elapsed)

    
    '''
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
        status, path, removed, maxSize = dls(startState, goalState, limit, table=None)
        elapsed = time.process_time() - startTime
        
        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed)
        else:
            output(1,0,"none",removed, maxSize, elapsed)   
    '''
    
if __name__ == "__main__":
    main()

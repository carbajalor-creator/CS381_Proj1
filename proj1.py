from collections import deque
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

def bfs(start, goal):
    startTime = time.process_time()
    if start == goal : 
        output(0, 0, 'none', 0, 1, time.process_time() - startTime)
        return 
    
    queue = deque()
    queue.append(start)
    print(queue)
    time = time.process_time() - startTime
    output()
    return


#search methods will track these variables and call output
#solutionFound is a bool 0 = success 1 = failure, 
def output(solutionFound, numMoves, sequence, statesRem, maxSize, time):
    if solutionFound == 0 :
        print('\nSolution found')
    elif solutionFound == 1:
        print('Solution not found')
    print(f'The number of moves: {numMoves} \nThe sequence of moves: {sequence} \n')
    print (f'The number of states removed: {statesRem} \nThe maximum size of the queue/stack: {maxSize} \nCPU time: {time}' )


#finding empty space on the board
def findBlank(board):
     for row in range (4):
        for col in range(4):
            if board[row][col] == 0:
                 return row,col



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


    #as it should look
    search = input ('Pick a search method by entering a number: \n (1)BFS \n (2)IDS \n (3)BFS & IDS \n (4)DLS \n')

    #max amount a 4x4 grid can search
    limit = 80 

    if search == '1' or search == '(1)':
        #print('You selected Breadth First Search')
        pass
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
        
    elif search == '3' or search == '(3)':
        print('You selected Breadth First Search & Iterative Deepening Search')
        dls(startState, goalState, limit)
    elif search == '4' or search == '(4)':
        #printout
        print('You selected Depth Limited Search') 
        startTime = time.process_time()
        status, path, removed, maxSize = dls(startState, goalState, limit)
        elapsed = time.process_time() - startTime


        if status == "found":
            output(0,len(path), path, removed, maxSize, elapsed)
        else:
            output(1,0,"none",removed, maxSize, elapsed)   


   
    
if __name__ == "__main__":
    main()



    
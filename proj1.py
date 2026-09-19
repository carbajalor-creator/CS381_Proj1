from collections import deque
import time

#tuples are (move, row, col)
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
    if currState[1] + 1 <= 3:
        children.append(('R', currState[0] + 1, currState[0]))
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


def main():

    startState = input ('Enter Start State: ')
    goalState = input ('Enter Goal State:')

    #as it should look

    search = input ('Pick a search method by entering a number: \n (1)BFS \n (2)IDS \n (3)BFS & IDS \n (4)DLS \n')

    if search == '1' or search == '(1)':
        print('You selected Breadth First Search')
        bfs(startState, goalState)
    elif search == '2' or search == '(2)':
        print('You selected Iterative Deepening Search')
        #ids(startState, goalState)
    elif search == '3' or search == '(3)':
        print('You selected Breadth First Search & Iterative Deepening Search')
    elif search == '4' or search == '(4)':
        print('You selected Depth Limited Search')   
        #dls(startState, goalState) 


if __name__ == "__main__":
    main()
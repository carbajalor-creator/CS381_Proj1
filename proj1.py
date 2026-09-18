def bfs(startState):

def ids(startState):

def dls(startState):

#should be under def main 
puzzle = input ("Enter Puzzle: ")
startState = input ('Enter Start State: ')
goalState = input ('Enter Goal State: ')
search = input ('Pick a search method by entering a number: \n (1)BFS \n (2)IDS \n (3)BFS & IDS \n (4)DLS \n')

if search == '1' or search == '(1)':
    print('You selected Breadth First Search')
elif search == '2' or search == '(2)':
    print('You selected Iterative Deepening Search')
elif search == '3' or search == '(3)':
    print('You selected Breadth First Search & Iterative Deepening Search')
elif search == '4' or search == '(4)':
    print('You selected Depth Limited Search')    


def bfs(startState):{}

def ids(startState):{}

#returns either a solution or failure
def idsDFSearch():
    
        #for depth = 0 to infinity do
            #result is set to the depth limited serach(problem, depth)
            #if the result doesnt equal the cuttoff then return the result
    pass     

#depth limited search 
def dLSearch(puzzle, start, goal):
        #frontier a lifo stack with NODE(problem.initial) as an element
        #make a stack to start the lifo process, copy down the puzzle/matrix from user
        stack = [start]
        
        #result is failure
        result = "failure"
        #while frontier isnt empty
        while len(stack) > 0:
             
            #node is set to Pop (frontier) taking the top of the stack
            node = stack.pop()
            #if problem.is-goal(node.state) then return the node
            if (stack.at(start) == stack.at(goal)):
                return stack.at(start)
            #if the depth(node > the limit then result is to cutoff)
            

            #else if not is-cycle(node)
                #for each child in expand (problem,node)
                #add child to frontier (push onto stack)

        #outside the loop return the result
        return result
    

def main():


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


   
    
if __name__ == "__main__":
    main()

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


import copy

resultDict = {}

def solve(path, maze, availableMovesLeft, timeToLive):
    """ Recursive solver function for given maze. Function writes answers to global variable "resultsDict".

    Parameters:

    path (tuple) :  Starting location when starting to solve the maze
    maze (list) :  2D list of the maze
    availableMovesLeft :  How many available moves there is to solve the maze. This should be reduced everytime when recursively calling the function.
    timeToLive :  How many available moves there is to solve the maze
    
    """
    cur = path[-1]
    possibles = [(cur[0], cur[1] + 1), (cur[0], cur[1] - 1), (cur[0] + 1, cur[1]), (cur[0] - 1, cur[1])] # Possible moves: Right, left, down, up
    if availableMovesLeft == 0:
        return

    for i in possibles: # Looping through the possible moves
        if i[0] < 0 or i[1] < 0 or i[0] >= len(maze) or i[1] >= len(maze[0]): # Out of the maze
            continue
        elif maze[i[0]][i[1]] == "#": # About to hit a wall
            continue
        elif i in path: # Dont go backwards the path
            continue
        elif maze[i[0]][i[1]] == "E": # The finish line
            path = path + (i,)

            if timeToLive not in resultDict:
                resultDict[timeToLive] = len(path)-1
            else:
                currentBest = resultDict[timeToLive]
                if currentBest > len(path)-1: # Replace current lowest path
                    resultDict[timeToLive] = len(path)-1
            
        else: # If got thorugh all of above check, it is possible continue solving
            newPath = path + (i,)
            solve(newPath, maze, availableMovesLeft - 1, timeToLive) # Recursive call with current location added to the path and one move taken away
            maze[i[0]][i[1]] = "#"


def getMazeList(chosenMaze):
    """ Get 2D list from txt file maze

    Parameters:

    chosenMaze (str) :  Text file name where maze is stored. Must be a rectangle. "#" presents wall. "E" presents exit. "^" presents starting location.

    Return:

    row (int) :  Y-cordinate of starting position
    col (int) :  X-cordinate of starting position
    mazeList (list) :  2D list of the maze

    
    """

    if chosenMaze == "maze1":
        with open('maze1.txt') as f:
            lines = f.readlines()
    elif chosenMaze == "maze2":
        with open('maze2.txt') as f:
            lines = f.readlines()

    mazeList = []
    for i in lines:
        mazeList.append(list(i))

    for i in mazeList:
        if ("\n") in i:
            i.remove("\n")
        
    for pos, i in enumerate(mazeList):
        if "^" in i:
            row = pos
            col = i.index("^")

    return row, col, mazeList


def writeToFile(results, mazeName, fileName = "results.txt"):
    """ Write results to txt file

    Parameters

    results (dict) :  Dictionary of results you want append to file
    mazeName (str) :  Name of the maze that went through the algorithm
    fileName (str) :  Name of the file you want results to be written in
    
    """

    with open(fileName, 'a') as f:
        for i in [20, 150, 200]:
            if i not in results:
                f.write(f'Could not get out of maze ({mazeName}) with {i} moves\n')
         
        for k,v in results.items():
            sentance = f'{k} was enough moves. Exited the maze ({mazeName}) with {v} moves\n'
            f.write(sentance)
        f.write("\n")


if __name__ == "__main__":

    moves = [20, 150, 200]
    mazeOfChoice = "maze2" # Choose maze1 or maze2
    row, col, originalMazeList = getMazeList(mazeOfChoice)

    for i in moves:
        mazeList = copy.deepcopy(originalMazeList) # Create a deepcopy of the original maze list so we can modify the list when solving it
        solve(path = ((row,col), ), maze = mazeList, availableMovesLeft = i, timeToLive = i)

    writeToFile(resultDict, mazeOfChoice)

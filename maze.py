from collections import deque
import heapq

BIG_MAZE = "bigMaze.txt"
MED_MAZE = "mediumMaze.txt"

###### Helper Functions ######

def findMazeEnd(maze):
  for row in range(len(maze)):
    for col in range(len(maze[row])):
      if(maze[row][col] == '.'):
        return row, col
  return -1, -1

def findNeighbours(maze, row, col):
  # Create list of neighbours
  neighbours = []
  # Check all adjacent locations in grid
  for offx, offy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    nRow = row + offx
    nCol = col + offy
    # Make sure that coordinate is within bounds
    if nRow >= 0 and nRow < len(maze) and nCol >= 0 and nCol < len(maze[0]):
      if (maze[nRow][nCol] != '%'):
        neighbours.append((nRow, nCol))
  return neighbours

def backtrackPath(parent, start, end):
  path = [end]
  while path[-1] != start:
    path.append(parent[path[-1]])
  path.reverse()
  return path

"""
Reads in a maze file line by line and stores it
in a 2d array.

Returns the array and the starting coordinates
"""
def createMaze(file):
  maze = []
  row = 0
  file.seek(0)
  for line in file.readlines():
    col = 0
    temp = []
    for char in line:
      if (char == 'P' or char == 'p'):
        p_row = row
        p_col = col
      if (char != '\n'):
        temp.append(char)
      col+=1
    maze.append(temp)
    row+=1
  return maze, p_row, p_col

# Summarizes search results
def generateReport(maze, p_row, p_col, path, node_count):
  drawPath(maze, path)
  printMaze(maze)
  print("End of maze found at ({}, {})".format(p_row, p_col))
  print("Total path cost: {}".format(len(path)-1))
  print("Total number of nodes expanded: {}".format(node_count))

# Prints the maze to console
def printMaze(maze):
  for line in maze:
    for char in line:
      print(char, end='')
    print()
  return

# Creates dots on the maze to show path
def drawPath(maze, path):
  for row, col in path[1:]:
    maze[row][col] = '.'
  return

# Manhattan approximation heuristic
def manhattan(cur_posX, cur_posY, goal_posX, goal_posY):
  return abs(cur_posX - goal_posX) + abs(cur_posY - goal_posY)

###### Searching Algorithms ######

def greedy_solve(maze, start_row, start_col):
  # Initialize the PQ
  frontier = []
  # Create a parent dictionary
  parent = {}
  # Get ending coordinates
  end_row, end_col = findMazeEnd(maze)
  # Node count to keep track of nodes expanded
  node_count = 1
  # Append the starting position (node)
  frontier.append((manhattan(start_col, start_row, end_col, end_row), 0, (start_row, start_col)))

  while frontier:
    (_, cost, (p_row, p_col)) = heapq.heappop(frontier)
    # if current position is destination, then we are done
    if(maze[p_row][p_col] == '.'):
      path = backtrackPath(parent, (start_row, start_col), (p_row, p_col))
      generateReport(maze, p_row, p_col, path, node_count)
      return
    else:
      # Find all unvisited neighbours and append them
      neighbours = findNeighbours(maze, p_row, p_col)
      for node in neighbours:
        # Check if node is already in frontier
        found = -1
        for i in range(len(frontier)):
          temp = frontier[i]
          if(node == temp[2]):
            found = i
            break

        # If its not, add it to frontier
        newNode = (manhattan(node[0], node[1], end_row, end_col) + cost + 1, cost + 1, node)
        if (found == -1 and node not in parent):
          parent[(node[0], node[1])] = (p_row, p_col)
          heapq.heappush(frontier, newNode)
          node_count += 1
        elif (found >= 0):
          # decrease key
          if(newNode[0] < frontier[i][0]):
            parent[(node[0], node[1])] = (p_row, p_col)
            frontier[i] = newNode
      heapq.heapify(frontier)
    

  print("Priority Queue was emptied and path was not found.")
  return -1, -1


# Depth-first search
def dfs_solve(maze, start_row, start_col):
  # Create our Stack
  stack = deque()
  # Push the starting position (node)
  stack.append((start_row, start_col))
  # Create a parent dictionary
  parent = {}
  # Node count to keep track of nodes expanded
  node_count = 1

  while stack:
    (p_row, p_col) = stack.pop()
    # If current position is destination, then we are done
    if(maze[p_row][p_col] == '.'):
      path = backtrackPath(parent, (start_row, start_col), (p_row, p_col))
      generateReport(maze, p_row, p_col, path, node_count)
      return
    else:
      # Otherwise, find all unvisited neighbours and push them to stack
      neighbours = findNeighbours(maze, p_row, p_col)
      for (row, col) in neighbours:
        # Check if node has been visited
        if((row, col) not in parent):
          parent[(row, col)] = (p_row, p_col)
          stack.append((row, col))
          node_count += 1

  print("Stack was emptied and path was not found.")
  return -1, -1

# Breadth-first search
def bfs_solve(maze, start_row, start_col):
  # Create our Queue
  queue = deque()
  # Append the starting position (node)
  queue.append((start_row, start_col))
  # Create a parent dictionary
  parent = {}
  # Node count to keep track of nodes expanded
  node_count = 1

  while queue:
    (p_row, p_col) = queue.popleft()
    # if current position is destination, then we are done
    if(maze[p_row][p_col] == '.'):
      path = backtrackPath(parent, (start_row, start_col), (p_row, p_col))
      generateReport(maze, p_row, p_col, path, node_count)
      return
    else:
      # Find all unvisited neighbours and append them
      neighbours = findNeighbours(maze, p_row, p_col)
      for (row, col) in neighbours:
        # Check if node has been visited
        if((row, col) not in parent):
          parent[(row, col)] = (p_row, p_col)
          queue.append((row, col))
          node_count += 1

  print("Queue was emptied and path was not found.")
  return -1, -1

###### Main ######

def main():
  # Initialize file and load maze into 2D array
  file = open(BIG_MAZE, "r")
  # DFS
  print("Solving maze using DFS")
  maze, p_row, p_col = createMaze(file)
  print("Player beginning at index ({}, {})".format(p_row,p_col))
  dfs_solve(maze, p_row, p_col)

  print("-" * 30)
  # BFS
  print("Solving maze using BFS")
  maze, p_row, p_col = createMaze(file)
  print("Player beginning at index ({}, {})".format(p_row,p_col))
  bfs_solve(maze, p_row, p_col)

  print("-" * 30)
  # Greedy
  print("Solving maze using Greedy Best-first Search")
  maze, p_row, p_col = createMaze(file)
  print("Player beginning at index ({}, {})".format(p_row,p_col))
  greedy_solve(maze, p_row, p_col)

if __name__ == "__main__":
  main()
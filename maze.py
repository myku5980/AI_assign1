from collections import deque
from queue import PriorityQueue

BIG_MAZE = "bigMaze.txt"
MED_MAZE = "mediumMaze.txt"

###### Helper Functions ######

def findMazeEnd(maze):
  for row in range(len(maze)):
    for col in range(len(maze[row])):
      if(maze[row][col] == '.'):
        return row, col
  return -1, -1

def findNeighbours(maze, parent, row, col):
  # Create list of neighbours
  neighbours = []
  # Check all adjacent locations in grid
  for offx, offy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    nRow = row + offx
    nCol = col + offy
    # Make sure that coordinate is within bounds
    if nRow >= 0 and nRow < len(maze) and nCol >= 0 and nCol < len(maze[0]):
      # Check if node has been visited
      if(maze[nRow][nCol] != '%' and (nRow, nCol) not in parent):
        parent[(nRow, nCol)] = (row, col)
        neighbours.append((nRow, nCol))
  return neighbours

def backtrackPath(parent, start, end):
  path = [end]
  while path[-1] != start:
    path.append(parent[path[-1]])
  path.reverse()
  return path

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

def generateReport(maze, p_row, p_col, path, node_count):
  drawPath(maze, path)
  printMaze(maze)
  print("End of maze found at ({}, {})".format(p_row, p_col))
  print("Total path cost: {}".format(len(path)-1))
  print("Total number of nodes expanded: {}".format(node_count))
  
def printMaze(maze):
  for line in maze:
    for char in line:
      print(char, end='')
    print()
  return

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
  pq_open = PriorityQueue()
  # Create a parent dictionary
  parent = {}
  # Get ending coordinates
  end_row, end_col = findMazeEnd(maze)
  # Node count to keep track of nodes expanded
  node_count = 1
  # Append the starting position (node)
  pq_open.put((5, (start_row, start_col)))

  while not pq_open.empty():
    (dist, (p_row, p_col)) = pq_open.get()

    # if current position is destination, then we are done
    if(maze[p_row][p_col] == '.'):
      path = backtrackPath(parent, (start_row, start_col), (p_row, p_col))
      generateReport(maze, p_row, p_col, path, node_count)
      return
    else:
      # Find all unvisited neighbours and append them
      neighbours = findNeighbours(maze, parent, p_row, p_col)
      for node in neighbours:
        pq_open.put((manhattan(node[0], node[1], end_row, end_col), node))
        node_count += 1
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
      neighbours = findNeighbours(maze, parent, p_row, p_col)
      for node in neighbours:
        stack.append(node)
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
      neighbours = findNeighbours(maze, parent, p_row, p_col)
      for node in neighbours:
        queue.append(node)
        node_count += 1

  print("Queue was emptied and path was not found.")
  return -1, -1

###### Main ######

def main():
  # Initialize file and load maze into 2D array
  file = open(BIG_MAZE ,"r")
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
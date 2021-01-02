from queue import PriorityQueue
import pygame
from node import Node

# get the next move by choosing the next move of the A* algorithm considering, head of snake as start, apple as end and snake body as walls
def getNextMove(grid,start,end):
    #initialize variables
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    came_from = {}
    g_score = {node:float("inf") for row in grid for node in row}       
    g_score[start] = 0
    f_score = {node:float("inf") for row in grid for node in row}       
    f_score[start] = h(start.get_pos(),end.get_pos())
    open_set_hash = {start}
    path_length = 0
    #update the neighbors of all nodes
    for row in grid:
        for node in row:
            node.update_neighbors(grid)
    # loop to find best path
    while not open_set.empty():
        
        #allow to quit the program during the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        #found end return the first move
        if current == end:
            return get_first_move(came_from,end,end).get_pos()

        # calculate scores of the neighbors and decide best move
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
    # end not found, choose first neighbor
    if len(start.neighbors) >0:
        return start.neighbors[0]
    else:
        # no path found and no neighbors move 1 to the right to end game (trapped)
        return start.get_pos()[0]+1,start.get_pos()[1]

# calculate manhatten distance for A* algorithm
def h(p1,p2):                                           
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)

# get the first move 
def get_first_move(came_from,current,end):
    path = []     
    while current in reversed(came_from):
        current = came_from[current]
        path.append(current)
    if(len(path)>1):
        return path[-2]
    return end
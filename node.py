import pygame
from colors import *

class Node:
    def __init__(self, row,col,width,total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.total_rows = total_rows
        self.tail = None
        self.neighbors = [] 
    #return position of the node 
    def get_pos(self):
        return self.row,self.col
    # return true if node is a snake
    def is_snake(self):
        return self.color == BLACK
    # return true if node is an apple
    def is_apple(self):
        return self.color == RED
    # reset node back to white
    def reset(self):
        self.color = WHITE
    # make the node an apple
    def make_apple(self):
        self.color = RED
    # make the node empty
    def make_empty(self):
        self.color = WHITE
    # make the node a snake
    def make_snake(self):
        self.color = BLACK
    # update the neighbors(as long as valid and not a snake)
    def update_neighbors(self,grid):                     
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_snake():   
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row >0 and not grid[self.row - 1][self.col].is_snake():                      
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_snake():   
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col>0 and not grid[self.row][self.col-1].is_snake():                         
            self.neighbors.append(grid[self.row][self.col-1])
    # draw the node
    def draw(self,win):                                 
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
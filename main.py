import pygame
import math
import pygame_menu
from queue import PriorityQueue
from functools import partial
import random
from auto_player import *
from node import Node
from colors import *
from how_to_use import *

WIDTH = 800
HEIGHT = WIDTH
WIN = pygame.display.set_mode((WIDTH,WIDTH))

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

#make a grid of nodes
def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    return grid

#draw a grid on the GUI
def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))

# draw the colors of the nodes onto the GUI
def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

#color the snake onto the GUI
def colorSnake(snake):
    for node in snake:
        node.make_snake()

#randomly add an apple to the grid
def get_apple_pos(snake, rows):
    x = random.randint(0,rows-1)
    y = random.randint(0,rows-1)
    for node in snake:
        if (x,y) == node.get_pos():
            x,y = get_apple_pos(snake,rows)
    return x,y

#menu that will say "play again" rather than "play" and change the menu title based on parameter
def play_again_menu(lost):
    pygame.display.set_caption("Menu")
    surface = pygame.display.set_mode((WIDTH,WIDTH))
    if(not lost):
        menu = pygame_menu.Menu(300,400,"Menu",theme=pygame_menu.themes.THEME_BLUE)
    else:
        menu = pygame_menu.Menu(300,400,"Game Over",theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button("Play Again",partial(main,WIN,WIDTH))
    menu.add_button("How To Play", how_to_use)
    menu.add_button("Quit",pygame_menu.events.EXIT)
    menu.mainloop(surface)

# main function to run the game
def main(win,width):
    # change the caption on the top corner
    pygame.display.set_caption("Snake")
    #set local variables
    direction = RIGHT
    ROWS = 25
    grid = make_grid(ROWS,width)
    snake = []
    grid[0][0].make_snake()
    snake.append(grid[0][0])
    clock = pygame.time.Clock()
    has_apple = False
    apple =None
    FPS =8
    lost_count = 0
    run = True
    lost = False
    font = pygame.font.Font('freesansbold.ttf', 20)
    auto = False
    #loop to run the game
    while run:
        #set speed of game
        clock.tick(FPS)
        # react to lost game
        if lost:
            # timer ended display play again menu
            if lost_count > FPS *5:
                play_again_menu(True)
                run = False
                break
            # add overlay to display game over and snake length
            else:
                lost_label = font.render("GAME OVER",1,BLACK)
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,HEIGHT/2))
                snake_label = font.render(f"Snake Length = {len(snake)}",1,BLACK)
                WIN.blit(snake_label, (WIDTH/2 - snake_label.get_width()/2,HEIGHT/2 + 25))
                lost_count+=1
                pygame.display.update()
                continue
        # update GUI
        draw(win,grid,ROWS,width)
        # react to events (close GUI and keypress)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and (direction != DOWN or len(snake) == 1):
                    direction = UP
                elif event.key == pygame.K_DOWN and (direction != UP or len(snake) == 1):
                    direction = DOWN
                elif event.key == pygame.K_RIGHT and (direction != LEFT or len(snake) == 1):
                    direction = RIGHT
                elif event.key == pygame.K_LEFT and (direction != RIGHT or len(snake) == 1):
                    direction = LEFT
                elif event.key == pygame.K_a:
                    auto= not auto
                elif event.key == pygame.K_p:
                    if FPS < 121:
                        FPS +=1
                elif event.key == pygame.K_m:
                    if FPS>1:
                        FPS-=1
                elif event.key == pygame.K_c:
                    play_again_menu(False)
        # run in manual mode
        if not auto:
            if(direction == UP):
                x,y = snake[0].get_pos()
                if(y-1 <0):
                    lost = True
                    continue
                x,y = x,y-1
                snake.insert(0,grid[x][y])
                if(grid[x][y].is_snake()):
                    lost = True
                elif(not grid[x][y].is_apple()):
                    (snake.pop()).make_empty()
                else:
                    has_apple = False
            if(direction == DOWN):
                x,y = snake[0].get_pos()
                if y+1 > ROWS -1:
                    lost = True
                    continue
                x,y = x,y+1
                snake.insert(0,grid[x][y])
                if(grid[x][y].is_snake()):
                    lost = True
                elif(not grid[x][y].is_apple()):
                    (snake.pop()).make_empty()
                else:
                    has_apple = False
            if(direction == RIGHT):
                x,y = snake[0].get_pos()
                if x+1>ROWS-1:
                    lost = True
                    continue
                x,y = x+1,y
                snake.insert(0,grid[x][y])
                if(grid[x][y].is_snake()):
                    lost = True
                elif(not grid[x][y].is_apple()):
                    (snake.pop()).make_empty()
                else:
                    has_apple = False
            if(direction == LEFT):
                x,y = snake[0].get_pos()
                if x-1 < 0:
                    lost = True
                    continue
                x,y = x-1,y
                snake.insert(0,grid[x][y])
                if(grid[x][y].is_snake()):
                    lost = True
                elif(not grid[x][y].is_apple()):
                    (snake.pop()).make_empty()
                else:
                    has_apple = False
            colorSnake(snake)
        #check if an apple needs to be added
        if(not has_apple):
            xApple,yApple = get_apple_pos(snake,ROWS)
            grid[xApple][yApple].make_apple()
            apple = grid[xApple][yApple]
            has_apple = True
        #run in auto mode
        if auto:
            try:
                x,y = getNextMove(grid,snake[0],apple)
            except:
                temp = grid[:]
                found = False
                for neighbor in snake[0].neighbors:
                    x,y = neighbor.get_pos()
                    temp[x][y].make_snake()
                    x1,y1 = snake[-1].get_pos()
                    temp[x1][y1].make_empty()
                    if getNextMove(temp,neighbor,apple)!=None:
                        found = True
                        temp[x][y].make_empty()
                        break
                    temp[x][y].make_empty()
                if(not found):
                    lost = True 
            snake.insert(0,grid[x][y])
            if(grid[x][y].is_snake()):
                lost = True
            elif(not grid[x][y].is_apple()):
                (snake.pop()).make_empty()
            else:
                has_apple = False
            colorSnake(snake)

# display the main menu 
def main_menu():
    pygame.init()
    pygame.display.set_caption("Menu")
    surface = pygame.display.set_mode((WIDTH,WIDTH))
    menu = pygame_menu.Menu(300,400,"Welcome",theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button("Play",partial(main,WIN,WIDTH))
    menu.add_button("How To Play", partial(how_to_use,WIDTH))
    menu.add_button("Quit",pygame_menu.events.EXIT)
    menu.mainloop(surface)

if __name__ == "__main__":
    main_menu()
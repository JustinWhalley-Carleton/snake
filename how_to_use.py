from colors import *
import pygame

#create text page 
def how_to_use(width):
    TEXTSPACING = 20
    HEADERSPACING = 25
    PARAGRAPHSPACING = 10

    display_surface = pygame.display.set_mode((width, width))

    pygame.display.set_caption('How To')
    

    header_font = pygame.font.Font('freesansbold.ttf', 20)
    text_font = pygame.font.SysFont('timesnewroman',15)
    

    header1 = make_header("Goal")
    text1 = make_text("Try to get the largest snake possible before hitting a wall or hitting a snake block. Each apple eaten will extend the snake by 1.")

    header2 = make_header("How to Move")
    text2 = make_text("Use the arrow keys to move. Note you cannot change direction by 180degrees (e.g. if going left, cannot change to right).")

    header3 = make_header("How to Use Auto Player")
    text3 = make_text("Click key 'a' to toggle between manual and auto play. The auto play only considers up to 1 move ahead and so it can trap itself.")

    header4 = make_header("How to Modify Speed")
    text4 = make_text("The 'p' key will increase the speed of the game and the 'm' key will decrease the speed of the game. It can be reduced to 1 frame")
    text5 = make_text("per second and be increased to 120 frames per second.")

    header5 = make_header("Go Back To Menu")
    text6 = make_text("To go back to menu, push key 'c'")
    

    while True:
        display_surface.fill(WHITE)

        i = 0
        j = 0

        display_surface.blit(header1, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text1, (i,j))
        j+=TEXTSPACING+PARAGRAPHSPACING

        display_surface.blit(header2, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text2, (i,j))
        j+=TEXTSPACING+PARAGRAPHSPACING

        display_surface.blit(header3, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text3, (i,j))
        j+=TEXTSPACING+PARAGRAPHSPACING

        display_surface.blit(header4, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text4, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text5, (i,j))
        j+=TEXTSPACING+PARAGRAPHSPACING

        display_surface.blit(header5, (i,j))
        j+=HEADERSPACING
        display_surface.blit(text6, (i,j))
        j+=TEXTSPACING+PARAGRAPHSPACING
        
        # react to keypress
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    pygame.display.set_caption("Menu")
                    return
            
            if event.type == pygame.QUIT:
    
                pygame.quit()
    
                quit()
           
            pygame.display.update()
#make header text
def make_header(text):
    header_font = pygame.font.Font('freesansbold.ttf', 20)
    return header_font.render(text, True, BLACK, WHITE)
#make regular text
def make_text(text):
    text_font = pygame.font.SysFont('timesnewroman',15)
    return text_font.render(text, True, BLACK, WHITE)
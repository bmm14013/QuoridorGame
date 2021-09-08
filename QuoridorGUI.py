#Author: Brendan MacIntyre
#Date:
#Description: 

from QuoridorEngine import *
import pygame, sys

#Width and height of window
BOARDSIZE = 500
SQUARESIZE = BOARDSIZE/9.8
FENCEWIDTH = BOARDSIZE/98

#Colors
WHITE = (255,255,255)
RED = (205,78,56)
BLUE = (50,147,198)
GRAY = (241,241,241)

#Initialize game and window
game = QuoridorGame()
WIN = pygame.display.set_mode((BOARDSIZE,BOARDSIZE))
pygame.display.set_caption("Quoridor")

def draw_board(win, board):
    """
    Draws the game board with fences. Takes as inputs the surface to draw the rectangles on and the board list 
    representation from the QuoridorEngine. SQUARESIZE and FENCEWIDTH, WHITE and GRAY are globally defined constants. 
    """
    win.fill(WHITE)
    
    #Draw board
    for row in board:
        for col in row:
            #Current grid position
            cords = col['cord']

            #Cords
            h_fence_cords = (cords[0]*(SQUARESIZE+FENCEWIDTH), cords[1]*SQUARESIZE+FENCEWIDTH*(cords[1]-1))
            v_fence_cords = (cords[0]*SQUARESIZE+FENCEWIDTH*(cords[0]-1), cords[1]*(SQUARESIZE+FENCEWIDTH))
            board_spotcords = (cords[0]*(SQUARESIZE+FENCEWIDTH), cords[1]*(SQUARESIZE+FENCEWIDTH))
            
            #Rect objects
            h_fence = pygame.Rect(h_fence_cords, (SQUARESIZE,FENCEWIDTH))
            v_fence = pygame.Rect(v_fence_cords, (FENCEWIDTH,SQUARESIZE))
            board_spot = pygame.Rect(board_spotcords, (SQUARESIZE,SQUARESIZE))
            
            #Draw grid portion           
            if cords[1] != 0 and cords[1] != 9 and cords[0] != 9:
                pygame.draw.rect(win, WHITE, h_fence)
            if cords[0] != 0 and cords[0] != 9 and cords[1] != 9:
                pygame.draw.rect(win, WHITE, v_fence)
            if cords[1] != 9 and cords[0] != 9:
                pygame.draw.rect(win, GRAY, board_spot)

def draw_players(win, p1_location, p2_location):
    """
    Draws players on board. Takes an input the surface to draw on and the board list representation from
    QuoridorEngine. SQUARESIZE, FENCEWIDTH, RED, BLUE are all global constants. 
    """

    p1_cords = (p1_location[0]*(SQUARESIZE+FENCEWIDTH), p1_location[1]*(SQUARESIZE+FENCEWIDTH))
    p1_center_cords = (p1_cords[0]+SQUARESIZE/2, p1_cords[1]+SQUARESIZE/2)
    
    p2_cords = (p2_location[0]*(SQUARESIZE+FENCEWIDTH), p2_location[1]*(SQUARESIZE+FENCEWIDTH))
    p2_center_cords = (p2_cords[0]+SQUARESIZE/2, p2_cords[1]+SQUARESIZE/2)

    #Draw P1
    pygame.draw.circle(win, RED, p1_center_cords, SQUARESIZE/4)
    pygame.draw.circle(win, BLUE, p2_center_cords, SQUARESIZE/4)

def move_pawn():
    """
    """



def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
            board_list = game.get_board()
            draw_board(WIN, board_list)
            draw_players(WIN, game.get_p1_location(), game.get_p2_location())
            pygame.display.update()

    pygame.quit()

main()



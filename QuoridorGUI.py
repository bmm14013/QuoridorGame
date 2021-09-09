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
LIGHTRED = (255,127,127)
BLUE = (50,147,198)
LIGHTBLUE = (183,225,240)
GRAY = (241,241,241)

FPS = 60

#Initialize game and window
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
            
            #Draw horizontal fence           
            if cords[1] != 0 and cords[1] != 9 and cords[0] != 9:
                if col['h'] == 1:
                    pygame.draw.rect(win, RED, h_fence)
                elif col['h'] == 2:
                    pygame.draw.rect(win, BLUE, h_fence)
                else:
                    pygame.draw.rect(win, WHITE, h_fence)
            
            #Draw vertical fence
            if cords[0] != 0 and cords[0] != 9 and cords[1] != 9:
                if col['v'] == 1:
                    pygame.draw.rect(win, RED, v_fence)
                elif col['v'] == 2:
                    pygame.draw.rect(win, BLUE, v_fence)
                else:
                    pygame.draw.rect(win, WHITE, v_fence)
            
            #Draw grid square
            if cords[1] != 9 and cords[0] != 9:
                if cords[1] == 0:
                    pygame.draw.rect(win, LIGHTRED, board_spot)
                elif cords[1] == 8:
                    pygame.draw.rect(win, LIGHTBLUE, board_spot)
                else:
                    pygame.draw.rect(win, GRAY, board_spot)

def draw_players(win, p1_location, p2_location):
    """
    Draws players on board. Takes an input the surface to draw on and the board list representation from
    QuoridorEngine. SQUARESIZE, FENCEWIDTH, RED, BLUE are all global constants. 
    """

    #Get P1 cords
    p1_cords = (p1_location[0]*(SQUARESIZE+FENCEWIDTH), p1_location[1]*(SQUARESIZE+FENCEWIDTH))
    p1_center_cords = (p1_cords[0]+SQUARESIZE/2, p1_cords[1]+SQUARESIZE/2)
    
    #Get P2 cords
    p2_cords = (p2_location[0]*(SQUARESIZE+FENCEWIDTH), p2_location[1]*(SQUARESIZE+FENCEWIDTH))
    p2_center_cords = (p2_cords[0]+SQUARESIZE/2, p2_cords[1]+SQUARESIZE/2)

    #Draw P1 and P2
    pygame.draw.circle(win, RED, p1_center_cords, SQUARESIZE/4)
    pygame.draw.circle(win, BLUE, p2_center_cords, SQUARESIZE/4)

def move_pawn(pos, game):
    """
    Moves pawn. Takes as input a tuple of the x,y coordinates from the mouse input, and the current game state object. 
    """

    #Convert coordinates to row and column
    row = int(pos[1]//(SQUARESIZE+FENCEWIDTH))
    col = int(pos[0]//(SQUARESIZE+FENCEWIDTH))
    #Make move
    game.move_pawn(game.get_player_turn(), (col,row))

def place_horizontal_fence(pos,game):
    """
    """
    #Convert y coordinate to column
    col = int(pos[0]//(SQUARESIZE+FENCEWIDTH))
    
    #Convert x coordinate to row, if it is between two squares
    h_fence_low_range = (SQUARESIZE/(SQUARESIZE+FENCEWIDTH))
    row_float = pos[1]/(SQUARESIZE+FENCEWIDTH)
    row_int = pos[1]//(SQUARESIZE+FENCEWIDTH)
    if row_float-row_int-h_fence_low_range > 0:
        row = int(round(row_float))
    else:
        return
    
    #Place horizontal fence
    game.place_fence(game.get_player_turn(), 'h', (col,row))

def place_vertical_fence(pos,game):
    """
    """
    #Convert x coordinate to row
    row = int(pos[1]//(SQUARESIZE+FENCEWIDTH))
    
    #Convert y coordinate to column, if it is between two squares
    v_fence_low_range = (SQUARESIZE/(SQUARESIZE+FENCEWIDTH))
    col_float = pos[0]/(SQUARESIZE+FENCEWIDTH)
    col_int = pos[0]//(SQUARESIZE+FENCEWIDTH)
    if col_float-col_int-v_fence_low_range > 0:
        col = int(round(col_float))
    else:
        return
    
    #Place vertical fence
    game.place_fence(game.get_player_turn(), 'v', (col,row))


def main():
    game = QuoridorGame()
    run = True
    clock = pygame.time.Clock()
    move_type = None

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            board_list = game.get_board()
            player_turn = game.get_player_turn()
        
            draw_board(WIN, board_list)
            draw_players(WIN, game.get_p1_location(), game.get_p2_location())
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    move_type = 'p'
                    #display moves
                if event.key == pygame.K_h:
                    move_type = 'h'
                    #display available fences
                if event.key == pygame.K_v:
                    move_type = 'v'
                    #display verticle fences
            
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'p':
                pos = pygame.mouse.get_pos()
                move_pawn(pos, game)
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'h':
                pos = pygame.mouse.get_pos()
                place_horizontal_fence(pos, game)
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'v':
                pos = pygame.mouse.get_pos()
                place_vertical_fence(pos, game)
            
            if player_turn != game.get_player_turn():
                move_type = None
            
            pygame.display.update()

            
               

    pygame.quit()

main()



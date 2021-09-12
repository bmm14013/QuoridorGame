#Author: Brendan MacIntyre
#Date: 9/10/2021
#Description: This program uses the pygame module to generate a GUI for a user to player a 
#               Quoridor board game. This program uses QuoridorEngine.py to handle the game mechanics. 

from QuoridorEngine import *
import pygame

#Width and height of window
BOARDSIZE = 500
SQUARESIZE = BOARDSIZE/9.8
FENCEWIDTH = BOARDSIZE/98

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (205,78,56)
LIGHTRED = (255,127,127)
LIGHTERRED = (247,198,197)
BLUE = (50,147,198)
LIGHTBLUE = (137,214,238)
LIGHTERBLUE = (197,226,238)
LIGHTGREEN = (139,231,139)
GRAY = (241,241,241)

#Window refresh rate
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
            coords = col['coord']

            #coords
            h_fence_coords = (coords[0]*(SQUARESIZE+FENCEWIDTH), coords[1]*SQUARESIZE+FENCEWIDTH*(coords[1]-1))
            v_fence_coords = (coords[0]*SQUARESIZE+FENCEWIDTH*(coords[0]-1), coords[1]*(SQUARESIZE+FENCEWIDTH))
            board_spotcoords = (coords[0]*(SQUARESIZE+FENCEWIDTH), coords[1]*(SQUARESIZE+FENCEWIDTH))
            
            #Rect objects
            h_fence = pygame.Rect(h_fence_coords, ((2*SQUARESIZE+FENCEWIDTH),FENCEWIDTH))
            v_fence = pygame.Rect(v_fence_coords, (FENCEWIDTH,2*SQUARESIZE+FENCEWIDTH))
            board_spot = pygame.Rect(board_spotcoords, (SQUARESIZE,SQUARESIZE))
            
            #Draw horizontal fence           
            if coords[1] != 0 and coords[1] != 9 and coords[0] != 8:
                if col['h'] == 1:
                    pygame.draw.rect(win, RED, h_fence)
                elif col['h'] == 2:
                    pygame.draw.rect(win, BLUE, h_fence)

            
            #Draw vertical fence
            if coords[0] != 0 and coords[0] != 9 and coords[1] != 9:
                if col['v'] == 1:
                    pygame.draw.rect(win, RED, v_fence)
                elif col['v'] == 2:
                    pygame.draw.rect(win, BLUE, v_fence)
 
            
            #Draw grid square
            if coords[1] != 9 and coords[0] != 9:
                if coords[1] == 0:
                    pygame.draw.rect(win, LIGHTRED, board_spot)
                elif coords[1] == 8:
                    pygame.draw.rect(win, LIGHTBLUE, board_spot)
                else:
                    pygame.draw.rect(win, GRAY, board_spot)


def draw_players(win, p1_location, p2_location):
    """
    Draws players on board. Takes an input the surface to draw on and the board list representation from
    QuoridorEngine. SQUARESIZE, FENCEWIDTH, RED, BLUE are all global constants. 
    """
    #Get P1 coords
    p1_coords = (p1_location[0]*(SQUARESIZE+FENCEWIDTH), p1_location[1]*(SQUARESIZE+FENCEWIDTH))
    p1_center_coords = (p1_coords[0]+SQUARESIZE/2, p1_coords[1]+SQUARESIZE/2)
    
    #Get P2 coords
    p2_coords = (p2_location[0]*(SQUARESIZE+FENCEWIDTH), p2_location[1]*(SQUARESIZE+FENCEWIDTH))
    p2_center_coords = (p2_coords[0]+SQUARESIZE/2, p2_coords[1]+SQUARESIZE/2)

    #Draw P1 and P2
    pygame.draw.circle(win, RED, p1_center_coords, SQUARESIZE/4)
    pygame.draw.circle(win, BLUE, p2_center_coords, SQUARESIZE/4)


def move_pawn(pos, game):
    """
    Moves pawn. Takes as input a tuple of the x,y coordinates from the mouse input, and the current game state object. 
    SQUARESIZE and FENCEWIDTH are global constants.
    """
    #Convert coordinates to row and column
    row = int(pos[1]//(SQUARESIZE+FENCEWIDTH))
    col = int(pos[0]//(SQUARESIZE+FENCEWIDTH))
    #Make move
    game.move_pawn(game.get_player_turn(), (col,row))


def place_horizontal_fence(pos,game):
    """
    Places a horizontal fence. Takes as input a tuple of the x,y coordinates from the mouse input, and the current
    game state object. The y input must be between two squares. SQUARESIZE and FENCEWIDTH are 
    global constants.
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
    Places a vertical fence. Takes as input a tuple of the x,y coordinates from the mouse input, and the current
    game state object. The x input must be between two squares. SQUARESIZE and FENCEWIDTH are 
    global constants.
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


def player_one_won(win):
    """
    Display a message that player one has won the game. Takes the display window as an input. 
    """
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    text = font.render('Red wins! Press space to play again.', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (BOARDSIZE//2, BOARDSIZE//2)
    win.blit(text, textRect)


def player_two_won(win):
    """
    Display a message that player two has won the game. Takes the display window as an input. 
    """
    pygame.font.init()
    font = pygame.font.Font(None, 32)
    text = font.render('Blue wins! Press space to play again.', True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.center = (BOARDSIZE//2, BOARDSIZE//2)
    win.blit(text, textRect)


def highlight_moves(win, game):
    """
    Highlights available moves for pawn movement. Takes the display surface and game state object as inputs.  
    """
    player_turn = game.get_player_turn()
    moves_available = game.possible_moves(game.get_pawn(player_turn))
    if None in moves_available:
        moves_available.remove(None)
    for move in moves_available:
        move_coords = (move[0]*(SQUARESIZE+FENCEWIDTH), move[1]*(SQUARESIZE+FENCEWIDTH))
        move_center_coords = (move_coords[0]+SQUARESIZE/2, move_coords[1]+SQUARESIZE/2)
        pygame.draw.circle(win, LIGHTGREEN, move_center_coords, SQUARESIZE/4)


def highlight_available_h_fences(win, game):
    """
    Highlights available horizontal fences. Takes the display surface and game state object as inputs. 
    """
    #Check if player has remaining fences
    player_turn = game.get_player_turn()
    if game.get_pawn(player_turn).get_remaining_fences() == 0:
        return

    board = game.get_board()
    
    #Set highlight color
    if player_turn == 1:
        color = LIGHTERRED
    else:
        color = LIGHTERBLUE
   
    for row in range(len(board)-1):
        for col in range(len(board)-2):
            #Highlight fence if no fence placed
            if not board[row][col]['h'] and not board[row][col+1]['h'] and board[row][col+1]['v'] != "Fence Continued":
                coords = board[row][col]['coord']
                h_fence_coords = (coords[0]*(SQUARESIZE+FENCEWIDTH), coords[1]*SQUARESIZE+FENCEWIDTH*(coords[1]-1))
                h_fence = pygame.Rect(h_fence_coords, (SQUARESIZE,FENCEWIDTH))
                pygame.draw.rect(win, color, h_fence)
            

def highlight_available_v_fences(win, game):
    """
    Highlights available vertical fences. Takes the display surface and game state object as inputs. 
    """
    #Check if player has remaining fences
    player_turn = game.get_player_turn()
    if game.get_pawn(player_turn).get_remaining_fences() == 0:
        return

    board = game.get_board()

    #Set highlight color
    if player_turn == 1:
        color = LIGHTERRED
    else:
        color = LIGHTERBLUE
    
    for row in range(len(board)-2):
        for col in range(len(board)-1):
            #Highlight fence if no fence placed. 
            if not board[row][col]['v'] and not board[row+1][col]['v'] and board[row+1][col]['h'] != "Fence Continued":
                coords = board[row][col]['coord']
                v_fence_coords = (coords[0]*SQUARESIZE+FENCEWIDTH*(coords[0]-1), coords[1]*(SQUARESIZE+FENCEWIDTH))
                v_fence = pygame.Rect(v_fence_coords, (FENCEWIDTH,SQUARESIZE))
                pygame.draw.rect(win, color, v_fence)


def main():
    #Initialize game
    game = QuoridorGame()
    run = True
    clock = pygame.time.Clock()
    move_type = None

    #Run loop
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            #Quit if user exits window
            if event.type == pygame.QUIT:
                run = False

            #Get board list representation and player turn
            board_list = game.get_board()
            player_turn = game.get_player_turn()

            #Draw board and player pawns
            draw_board(WIN, board_list)
            draw_players(WIN, game.get_p1_location(), game.get_p2_location())
            if move_type == 'p':
                highlight_moves(WIN, game)
            if move_type == 'h':
                highlight_available_h_fences(WIN, game)
            if move_type == 'v':
                highlight_available_v_fences(WIN, game)
           
           #Get user move type 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    move_type = 'p'
                if event.key == pygame.K_h:
                    move_type = 'h'
                if event.key == pygame.K_v:
                    move_type = 'v'
            
            #Make move based on mouse input and move type
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'p':
                pos = pygame.mouse.get_pos()
                move_pawn(pos, game)
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'h':
                pos = pygame.mouse.get_pos()
                place_horizontal_fence(pos, game)
            if event.type == pygame.MOUSEBUTTONDOWN and move_type == 'v':
                pos = pygame.mouse.get_pos()
                place_vertical_fence(pos, game)
            
            #Reset move type after player makes a valid move
            if player_turn != game.get_player_turn():
                move_type = None
            
            #Display message if either user has won the game. 
            if game.is_winner(1):
                player_one_won(WIN)
            if game.is_winner(2):
                player_two_won(WIN)

            #Reset game if space bar is pressed. 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game = QuoridorGame()

            #Update display window
            pygame.display.update()

    pygame.quit()

main()



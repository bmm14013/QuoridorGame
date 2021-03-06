#Author: Brendan MacIntyre
#Date: 08/03/2021
#Description: This program contains an implementation of the Quoridor board game. It uses a class called 
#             QuoridorGame that handles the majority of the board and game rules. 

import copy
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Pawn:
    """
    This class represents a pawn object to be used in a Quoridor game.
    """

    def __init__(self,player,starting_coords):
        """
        Initializes pawn object. Used by the QuoridorGame class
        to generate pawn objects for game.
        
        Args:
            player: Integer representing the player the pawn belogns to.
            starting_cords: Tuple representing the starting coordinates of the pawn.
        """
        self._player = player
        self._location = starting_coords
        self._fences = 10
    
    def get_player(self):
        """
        Returns the integer representing the player number of the pawn.
        """
        return self._player

    def get_location(self):
        """
        Returns a tuple containing the coordinates of the pawns current location.
        """
        return self._location
    
    def move_pawn(self,new_location):
        """
        Change the location of the pawn. 
        
        Args:
            new_location: Tuple containing the coordinates of the desired location.
        """
        self._location = new_location
    
    def get_remaining_fences(self):
        """
        Returns the remaining fences available to the pawn/player.
        """
        return self._fences
    
    def decrement_fences(self):
        """
        Decreases amount of remaining fences by 1.
        """
        self._fences -= 1



class QuoridorGame:
    """
    This class represents a Quoridor game board object. Player 1 will start the game. On a player's turn
    they will make one move. They can either move the pawn or place a fence. Uses the Pawn class to generate
    pawn objects.
    Main methods available to use are as follows:
    
    print_board: Prints the game board
    move_pawn: Moves pawn to desired location. 
    place_fence: Places a fence at a desired location
    is_winner: Tells the user if a player has won the game
    get_player_turn: Tells the user whose turn it is
    """

    def __init__(self):
        """
        Initializes the game board with fences (four board edges) and pawns (P1 and P2) placed in the correct
        positions.
        """
        #Create players
        self._p1 = Pawn(1, (4,0))
        self._p2 = Pawn(2, (4,8))
        self._player_turn = 1

        #Create board
        self._board = []
        for row in range(10):
            self._board.append([{'coord': (column,row), 'h': False, 'v': False, 'pawn': False} for column in range(10)])
        
        #Populate borders with fences
        for row in self._board:
            for column in row:
                #Left and right edges
                if (column['coord'][0] == 0 or column['coord'][0] == 9) and column['coord'][1] != 9:
                    column['v'] = True
                #Top and bottom edges
                if (column['coord'][1] == 0 or column['coord'][1] == 9) and column['coord'][0] != 9:
                    column['h'] = True

        #Place players on board
        p1_location = self._p1.get_location()
        p2_location = self._p2.get_location()
        self._board[p1_location[1]][p1_location[0]]['pawn'] = True
        self._board[p2_location[1]][p2_location[0]]['pawn'] = True

    
    def get_board(self):
        """
        Returns the board list representation.
        """
        return self._board

    def get_pawn(self, player):
        """
        Returns the pawn object of a given player. 
        
        Args:
            player: Integer representing the player of interest.
        """
        if player == 1:
            return self._p1
        
        if player == 2:
            return self._p2

    def get_p1_location(self):
        """
        Returns coordinates of player 1 location.
        """
        return self._p1.get_location()

    def get_p2_location(self):
        """
        Returns coordinates of player 2 location.
        """
        return self._p2.get_location()

    def get_player_turn(self):
        """
        Returns the integer representing the player whose turn it is. 
        """    
        return self._player_turn
    
    def set_player_turn(self,player):
        """
        Change player turn.
        
        Args:
            player: Integer representing the player who's turn it will be.
        """
        self._player_turn = player
    
    def print_board(self):
        """
        Prints the game board board.
        """
        for row in self._board:
            #Initialize row strings
            horiz_edges = ""
            vert_edges = ""
            for column in row:
                #Generate horizontal edge
                if not column['h']:
                    horiz_edges += "+  "
                else:
                    horiz_edges += "+=="
                
                #Generate verticle edges
                if not column['v']:
                    vert_edges += " "
                else:
                    vert_edges += "|"
                
                #Place player on board
                if column['coord'] == self._p1.get_location():
                    vert_edges += 'P1'
                elif column['coord'] == self._p2.get_location():
                    vert_edges += 'P2'
                else:
                    vert_edges += "  "
           
            #Print line
            print(horiz_edges)
            print(vert_edges)
    
    def can_move_left(self,pawn):
        """
        Determines all left moves(if any) available to the pawn of interest.
        
        Args: 
            pawn: Pawn object of interest.
        
        Returns:
            A set of one or more tuples containing the coordinates of possible moves in the left
            direction. 
        """
        location = pawn.get_location()
        #Row containing pawn
        row = self._board[location[1]]

        #Left cell obstructed by fence
        if row[location[0]]['v']:
            return {None}
        
        #Cell to left of pawn
        left_cell = row[location[0]-1]
        #Left cell is unobstructed
        if not left_cell['pawn']:
            return {left_cell['coord']}
        
        #Left cell is obstructed by pawn and can jump
        if left_cell['pawn'] and not left_cell['v']:
            return {row[location[0]-2]['coord']}

        #Left cell is blocked by pawn and fence. Calculate diagonal moves
        if left_cell['pawn'] and left_cell['v']:
            diagonal_moves = set()
            #Upper-left cell not blocked by fence
            if not left_cell['h']:
                diagonal_moves.add((location[0]-1,location[1]-1))
            #Lower-left cell not blocked by fence
            if not self._board[location[1]+1][location[0]-1]['h']:
                diagonal_moves.add((location[0]-1,location[1]+1))
            return diagonal_moves
        

    def can_move_right(self,pawn): 
        """
        Determines all right moves(if any) available to the pawn of interest.
        
        Args: 
            pawn: Pawn object of interest.
        
        Returns:
            A set of one or more tuples containing the coordinates of possible moves in the right
            direction. 
        """
        location = pawn.get_location()
        #Row containing pawn
        row = self._board[location[1]]
        #Cell to right of pawn
        right_cell = row[location[0]+1]

        #Right cell obstructed by fence
        if right_cell['v']:
            return {None}
        
        #Right cell is unobstructed
        if not right_cell['pawn']:
            return {right_cell['coord']}
        
        #Right cell is obstructed by pawn and can jump
        if right_cell['pawn'] and not row[location[0]+2]['v']:
            return {row[location[0]+2]['coord']}
        
        #Right cell blocked by a pawn and fence. Calculate diagonal moves
        if right_cell['pawn'] and row[location[0]+2]['v']:
            diagonal_moves = set()
            #Upper-right cell not blocked by fence
            if not row[location[0]+1]['h']: 
                diagonal_moves.add((location[0]+1,location[1]-1))
            #Lower-right cell not blocked by fence
            if not self._board[location[1]+1][location[0]+1]['h']:
                diagonal_moves.add((location[0]+1,location[1]+1))
            return diagonal_moves
    
    def can_move_up(self,pawn):
        """
        Determines all up moves(if any) available to the pawn of interest.
        
        Args: 
            pawn: Pawn object of interest.
        
        Returns:
            A set of one or more tuples containing the coordinates of possible moves in the up
            direction. 
        """
        location = pawn.get_location()

        #Upper cell is obstructed by fence
        if self._board[location[1]][location[0]]['h']:
            return {None}
        
        #Upper cell is unobstructed
        if not self._board[location[1]-1][location[0]]['pawn']:
            return {(location[0],location[1]-1)}
        
        #Upper cell is obstructed by pawn and can jump
        if self._board[location[1]-1][location[0]]['pawn'] and not self._board[location[1]-1][location[0]]['h']:
            return {(location[0],location[1]-2)}
        
        #Upper cell is obstructed by pawn and fence. Calculate diagonal moves
        if self._board[location[1]-1][location[0]]['pawn'] and self._board[location[1]-1][location[0]]['h']:
            diagonal_moves = set()
            #Upper-right cell not blocked by fence
            if not self._board[location[1]-1][location[0]+1]['v']:
                diagonal_moves.add((location[0]+1,location[1]-1))
            #Upper-left cell not blocked by fence
            if not self._board[location[1]-1][location[0]]['v']:
                diagonal_moves.add((location[0]-1,location[1]-1))
            return diagonal_moves
    
    def can_move_down(self,pawn):
        """
        Determines all down moves(if any) available to the pawn of interest.
        
        Args: 
            pawn: Pawn object of interest.
        
        Returns:
            A set of one or more tuples containing the coordinates of possible moves in the down
            direction. 
        """
        location = pawn.get_location()

        #Lower cell is obstructed by fence
        if self._board[location[1]+1][location[0]]['h']:
            return {None}
        
        #Lower cell is unobstructed
        if not self._board[location[1]+1][location[0]]['pawn']:
            return {(location[0],location[1]+1)}
        
        #Lower cell is obstructed by pawn and can jump
        if self._board[location[1]+1][location[0]]['pawn'] and not self._board[location[1]+2][location[0]]['h']:
            return {(location[0],location[1]+2)}

        #Lower cell is obstructed by pawn and fence. Calculate diagonal moves
        if self._board[location[1]+1][location[0]]['pawn'] and self._board[location[1]+2][location[0]]['h']:
            diagonal_moves = set()
            #Lower-right cell not blocked by fence
            if not self._board[location[1]+1][location[0]+1]['v']:
                diagonal_moves.add((location[0]+1,location[1]+1))
            #Lower-left cell not blocked by fence
            if not self._board[location[1]+1][location[0]]['v']:
                diagonal_moves.add((location[0]-1,location[1]+1))
            return diagonal_moves

    def possible_moves(self,pawn):
        """
        Returns a set of tuples containing the coordinates of all possible moves for a pawn.
        
        Args: 
            pawn: Pawn object of interest.
        
        Returns:
            A set of one or more tuples containing coordinates of all possible moves for a pawn.
        """
        right = self.can_move_right(pawn)
        left = self.can_move_left(pawn)
        up = self.can_move_up(pawn)
        down = self.can_move_down(pawn)
        return right.union(left,up,down)

  
    def is_winner(self,player):
        """
        This method checks if a player has won the game.

        Args:
            player: Integer representing the player of interest.
        
        Returns:
            True if the player has won and False if the player has not won. 
        """
        #Check player 1 win
        if player == 1 and self._p1.get_location()[1] == 8:
            return True
        
        #Check player 2 win
        if player == 2 and self._p2.get_location()[1] == 0:
            return True
        
        #No player has won
        return False
    
    def move_pawn(self,player,coords):
        """
        This method is used to move a pawn. The method checks if the move is valid and then makes the 
        move if so. Pawn location is updated both in the Pawn object and on the board. 

        Args:
            player: Integer represting the player making the move.
            coords: Tuple containing the coordinates the pawn will move to.
        
        Returns:
            True if the move was successful or causes a win, and False if the move is invalid or 
            the game has already been won. 
       
        """
        #Check if either player has won
        if self.is_winner(1) or self.is_winner(2):
            return False
        
        #Calculate moves if player 1
        if player == 1 and self.get_player_turn() == player:
            moves_available = self.possible_moves(self._p1)
            #Check if move is in possible moves
            if coords in moves_available:
                #Clear current location on board
                location = self._p1.get_location()
                self._board[location[1]][location[0]]['pawn'] = False
                #Make move and set new location on board
                self._p1.move_pawn(coords)
                self._board[coords[1]][coords[0]]['pawn'] = True
                
                #Update player turn
                self.set_player_turn(2)
                return True

        #Calculate moves if player 2
        if player == 2 and self.get_player_turn() == player:
            moves_available = self.possible_moves(self._p2)
            #Check if move is in possible moves
            if coords in moves_available:
                #Clear current location on board
                location = self._p2.get_location()
                self._board[location[1]][location[0]]['pawn'] = False
                #Make move and set new location on board
                self._p2.move_pawn(coords)
                self._board[coords[1]][coords[0]]['pawn'] = True
                
                #Update player turn
                self.set_player_turn(1)
                return True
                
        #Move is invalid
        return False
    
    def fair_play_check(self,fence_type,coords):
        """
        This method checks if placing a fence will break the fair play rule. 
        
        Args:
            fence_type: String character containing the type of the fence (either 'h' or 'v').
            coords: Tuple containing the coordinates where a fence is to be placed.
        
        Returns:
            True if there remains a path for both players after the fence is placed and False if 
            it breaks the fair play rule.
        """
        #Copy board and place fence
        board_copy = copy.deepcopy(self.get_board())
        if fence_type == 'h':
            board_copy[coords[1]][coords[0]]['h'] = True
            board_copy[coords[1]][coords[0]+1]['h'] = True
        if fence_type == 'v':
            board_copy[coords[1]][coords[0]]['v'] = True
            board_copy[coords[1]+1][coords[0]]['v'] = True
        
        #Create matrix grid representing board copy
        matrix = [[1 for _ in range(17)] for _ in range(17)]
        for row in range(len(board_copy)-1):
            for col in range(len(board_copy)-1):
                #Set vertical fences
                if col != 0 and board_copy[row][col]['v'] != False:
                    matrix[2*row][2*col-1] = 0
                #Set horizontal fences
                if row != 0 and board_copy[row][col]['h'] != False:
                    matrix[2*row-1][2*col] = 0
                #Restrict diagonal movement
                if row != 8 and col != 8:
                    matrix[2*row+1][2*col+1] = 0    


        #Initialize A* algorithm
        grid = Grid(matrix = matrix)
        finder = AStarFinder()

        #Initialize A* algorithm for player 1 path
        p1_location = self.get_p1_location()
        p1_path_found = False
        endpoint_counter = 0
        start = grid.node(2*p1_location[0],2*p1_location[1])
        
        #Find path to goal for p1. Starts at left most square and checks for path to all goal squares if neccessary
        while not p1_path_found and endpoint_counter < len(board_copy)-1:
            end = grid.node(2*endpoint_counter,16)
            path, runs = finder.find_path(start,end,grid)
            if len(path) > 0:
                p1_path_found = True 
            grid.cleanup()
            endpoint_counter += 1

        #Initialize A* algorithm for player 2 path
        p2_location = self.get_p2_location()
        p2_path_found = False
        endpoint_counter = 0
        start = grid.node(2*p2_location[0],2*p2_location[1])

        #Find path to goal for p2. Starts at left most square and checks for path to all goal squares if neccessary
        while not p2_path_found and endpoint_counter < len(board_copy)-1:
            end = grid.node(2*endpoint_counter,0)
            path, runs = finder.find_path(start,end,grid)
            if len(path) > 0:
                p2_path_found = True 
            grid.cleanup()
            endpoint_counter += 1
        
        #Return True if path found for both players. 
        return p1_path_found and p2_path_found
        

    def place_fence(self,player,fence_type,coords):
        """
        Places a fence for a player. This method checks that the fence placement is valid and if 
        so places the fence specified. 
        
        Args:
            player: Integer representing the player making the move.
            fence_type: String character representing the type of fence to be placed (either 'h' or v').
            coords: Tuple containing the coordinates where the fence will be placed. 
        
        Returns:
            True if the fence placement is valid and move is made, False if the move is invalid or the game
            has already been won. 
        """

        #Check if game has already been won, and player turn is correct
        if self.is_winner(1) or self.is_winner(2) or player != self.get_player_turn():
            return False
        
        valid_h_coords = (set(range(8)), set(range(9)))
        valid_v_coords = (set(range(9)), set(range(8)))

        #Placing horizontal fence
        if fence_type == 'h' and coords[0] in valid_h_coords[0] and coords[1] in valid_h_coords[1]:
            if not self._board[coords[1]][coords[0]]['h'] and not self._board[coords[1]][coords[0]+1]['h'] and self._board[coords[1]][coords[0]+1]['v'] != "Fence Continued":
                #Check that placement satisfies fair play rule
                if not self.fair_play_check('h',coords):
                    return False
                self._board[coords[1]][coords[0]]['h'] = player
                self._board[coords[1]][coords[0]+1]['h'] = "Fence Continued"
                #Decrement fences and change player turn
                self.get_pawn(player).decrement_fences()
                if player == 1:
                    self.set_player_turn(2)
                else:
                    self.set_player_turn(1)
        
        #Placing vertical fence
        if fence_type == 'v' and coords[0] in valid_v_coords[0] and coords[1] in valid_v_coords[1] and self._board[coords[1]+1][coords[0]]['h'] != "Fence Continued":
            if not self._board[coords[1]][coords[0]]['v'] and not self._board[coords[1]+1][coords[0]]['v']:
                #Check that placement satisfies fair play rule
                if not self.fair_play_check('v',coords):
                    return False
                self._board[coords[1]][coords[0]]['v'] = player
                self._board[coords[1]+1][coords[0]]['v'] = "Fence Continued"
                #Decrement fences and change player turn
                self.get_pawn(player).decrement_fences()
                if player == 1:
                    self.set_player_turn(2)
                else:
                    self.set_player_turn(1)

        #Move is invalid
        return False

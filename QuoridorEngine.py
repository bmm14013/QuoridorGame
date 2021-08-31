#Author: Brendan MacIntyre
#Date: 08/03/2021
#Description: This program contains an implementation of the Quoridor board game. It uses a class called 
#             QuoridorGame that handles the majority of the board and game rules. 


class Pawn:
    """
    This class represents a pawn object to be used in a Quoridor game.
    """

    def __init__(self,player,starting_cords):
        """
        Initializes pawn object. Takes as parameters an integer representing the player the pawn belongs to,
        and a tuple representing the starting coordinates of the pawn. Used by the QuoridorGame class
        to generate pawn objects for game.
        """
        self._player = player
        self._location = starting_cords
        self._fences = 10
    
    def get_player(self):
        """
        Returns the integer representing the player number of the pawn
        """
        return self._player

    def get_location(self):
        """
        Returns a tuple containing the coordinates of the pawns current location
        """
        return self._location
    
    def move_pawn(self,new_location):
        """
        Change the location of the pawn. Takes as a parameter a tuple containing the coordinates of the 
        desired location. 
        """
        self._location = new_location
    
    def get_remaining_fences(self):
        """
        Returns the remaining fences available to the pawn/player 
        """
        return self._fences
    
    def decrement_fences(self):
        """
        Decreases amount of remaining fences by 1
        """
        self._fences -= 1



class QuoridorGame:
    """
    This class represents a Quoridor game board object. Player 1 will start the game. On a player's turn
    they will make one move. They can either move the pawn or place a fence. Uses the Pawn class to generate
    pawn objects. There is a fair play rule that an opponent cannot block off access to the other players goal line,
    however this is not enforced. 
    Main methods available to use are as follows:
    
    :print_board: Prints the game board
    :move_pawn: Moves pawn to desired location. 
    :place_fence: Places a fence at a desired location
    :is_winner: Tells the user if a player has won the game
    :get_player_turn: Tells the user whose turn it is
    """

    def __init__(self):
        """
        Initializes the game board with fences (four board edges) and pawns (P1 and P2) placed in the correct
        positions
        """
        #Create players
        self._p1 = Pawn(1, (4,0))
        self._p2 = Pawn(2, (4,8))
        self._player_turn = 1

        #Create board
        self._board = []
        for row in range(10):
            self._board.append([{'cord': (column,row), 'h': False, 'v': False, 'pawn': False} for column in range(10)])
        
        #Populate borders with fences
        for row in self._board:
            for column in row:
                #Left and right edges
                if (column['cord'][0] == 0 or column['cord'][0] == 9) and column['cord'][1] != 9:
                    column['v'] = True
                #Top and bottom edges
                if (column['cord'][1] == 0 or column['cord'][1] == 9) and column['cord'][0] != 9:
                    column['h'] = True

        #Place players on board
        p1_location = self._p1.get_location()
        p2_location = self._p2.get_location()
        self._board[p1_location[1]][p1_location[0]]['pawn'] = True
        self._board[p2_location[1]][p2_location[0]]['pawn'] = True

    def get_player_turn(self):
        """
        Returns the integer representing the player whose turn it is. 
        """    
        return self._player_turn
    
    def set_player_turn(self,player):
        """
        Change player turn. Takes as a parameter the integer representing the player who's turn it will be.
        """
        self._player_turn = player
    
    def print_board(self):
        """
        Prints the game board board
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
                if column['cord'] == self._p1.get_location():
                    vert_edges += 'P1'
                elif column['cord'] == self._p2.get_location():
                    vert_edges += 'P2'
                else:
                    vert_edges += "  "
           
            #Print line
            print(horiz_edges)
            print(vert_edges)
    
    def can_move_left(self,pawn):
        """
        Determines all left moves(if any) available to the pawn of interest. Returns a set of one or more
        tuples containing the coordinates of possible moves. 
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
            return {left_cell['cord']}
        
        #Left cell is obstructed by pawn and can jump
        if left_cell['pawn'] and not left_cell['v']:
            return {row[location[0]-2]['cord']}

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
        Determines all right moves(if any) available to the pawn of interest. Returns a set of one or more
        tuples containing the coordinates of possible moves. Takes as a parameter the pawn object of interest.
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
            return {right_cell['cord']}
        
        #Right cell is obstructed by pawn and can jump
        if right_cell['pawn'] and not row[location[0]+2]['v']:
            return {row[location[0]+2]['cord']}
        
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
        Determines all up moves(if any) available to the pawn of interest. Returns a set of one or more
        tuples containing the coordinates of possible moves. Takes as a parameter the pawn object of interest.
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
        Determines all down moves(if any) available to the pawn of interest. Returns a set of one or more
        tuples containing the coordinates of possible moves. Takes as a parameter the pawn object of interest.
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
        Returns a set of tuples containing coordintes of possible moves for a pawn. Takes as a parameter
        the pawn of interest.
        """
        right = self.can_move_right(pawn)
        left = self.can_move_left(pawn)
        up = self.can_move_up(pawn)
        down = self.can_move_down(pawn)
        return right.union(left,up,down)

  
    def is_winner(self,player):
        """
        This method takes as a parameter a single integer representing the player of interest and returns 
        True if that player has won and False if that player has not won
        """
        #Check player 1 win
        if player == 1 and self._p1.get_location()[1] == 8:
            return True
        
        #Check player 2 win
        if player == 2 and self._p2.get_location()[1] == 0:
            return True
        
        #No player has won
        return False
    
    def move_pawn(self,player,cords):
        """
        This method takes two parameters, an integer that represents which player is making the move and 
        a tuple with the coordinates of where the pawn is going to be moved to. If the move is forbidden
        by the rule or blocked by the fence, returns False. If the move was successful or causes a win, returns 
        True and make the move. If the game has already been won, returns False
        """
        #Check if either player has won
        if self.is_winner(1) or self.is_winner(2):
            return False
        
        #Calculate moves if player 1
        if player == 1 and self.get_player_turn() == player:
            moves_available = self.possible_moves(self._p1)
            #Check if move is in possible moves
            if cords in moves_available:
                #Clear current location on board
                location = self._p1.get_location()
                self._board[location[1]][location[0]]['pawn'] = False
                #Make move and set new location on board
                self._p1.move_pawn(cords)
                self._board[cords[1]][cords[0]]['pawn'] = True
                
                #Update player turn
                self.set_player_turn(2)
                return True

        #Calculate moves if player 2
        if player == 2 and self.get_player_turn() == player:
            moves_available = self.possible_moves(self._p2)
            #Check if move is in possible moves
            if cords in moves_available:
                #Clear current location on board
                location = self._p2.get_location()
                self._board[location[1]][location[0]]['pawn'] = False
                #Make move and set new location on board
                self._p2.move_pawn(cords)
                self._board[cords[1]][cords[0]]['pawn'] = True
                
                #Update player turn
                self.set_player_turn(1)
                return True
                
        #Move is invalid
        return False
        
    def place_fence(self,player,fence_type,cords):
        """
        This method takes as parameters an integer which represents which player is making the move, a letter
        indicating whether it is verticle (v) or horizontal (h) fence, a tuple of integers that represents the position
        on which the fence is to be placed (will be placed on top left corner of cell). If the player has no
        fences left, or if the fence is out of bounds, or if there is already a fence there, returns False. 
        If the fence can be placed, returns True and places the fence. If the game has already been won, returns False.
        """
        
        #Check if game has already been won
        if self.is_winner(1) or self.is_winner(2):
            return False
        
        #Check if player one can place fence (Is currently their turn and has remaining fences)
        if player == 1 and self.get_player_turn() == 1 and self._p1.get_remaining_fences() != 0:
            #Check that cell has no fence of desired type
            if not self._board[cords[1]][cords[0]][fence_type]:
                #Place fence
                self._board[cords[1]][cords[0]][fence_type] = True
                #Update player turn and fences available
                self._p1.decrement_fences()
                self.set_player_turn(2)
                return True
        
        #Check if player two can place fence
        if player == 2 and self.get_player_turn() == 2 and self._p2.get_remaining_fences() != 0:
            #Check that cell has no fence of desired type
            if not self._board[cords[1]][cords[0]][fence_type]:
                #Place fence
                self._board[cords[1]][cords[0]][fence_type] = True
                #Update player turn and fences available
                self._p2.decrement_fences()
                self.set_player_turn(1)
                return True
        
        #Move is invalid
        return False

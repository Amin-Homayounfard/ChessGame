from PrintChessBoard import *
import copy

chessboard = [[('R', 'w'), ('N', 'w'), ('B', 'w'), ('Q', 'w'), ('K', 'w'), ('B', 'w'), ('N', 'w'), ('R', 'w')],
              [('P', 'w'), ('P', 'w'), ('P', 'w'), ('P', 'w'), ('P', 'w'), ('P', 'w'), ('P', 'w'), ('P', 'w')],
              [(        ), (        ), (        ), (        ), (        ), (        ), (        ), (        )],
              [(        ), (        ), (        ), (        ), (        ), (        ), (        ), (        )],
              [(        ), (        ), (        ), (        ), (        ), (        ), (        ), (        )],
              [(        ), (        ), (        ), (        ), (        ), (        ), (        ), (        )],
              [('P', 'b'), ('P', 'b'), ('P', 'b'), ('P', 'b'), ('P', 'b'), ('P', 'b'), ('P', 'b'), ('P', 'b')],
              [('R', 'b'), ('N', 'b'), ('B', 'b'), ('Q', 'b'), ('K', 'b'), ('B', 'b'), ('N', 'b'), ('R', 'b')]]

white_pieces_locations = []
black_pieces_locations = []
kings_locations = dict()


for row in range(8):
    for column in range(8):
        if len(chessboard[row][column]) != 0:
            if chessboard[row][column][1] == 'w' and chessboard[row][column][0] != 'K':
                white_pieces_locations.append((column, row))
            elif chessboard[row][column][1] == 'b' and chessboard[row][column][0] != 'K':
                black_pieces_locations.append((column, row))
            if chessboard[row][column][0] == 'K':
                kings_locations[chessboard[row][column][1]] = (column, row)


def can_be_moved(origin, destination):
    selected_piece = chessboard[origin[1]][origin[0]][0]
    selected_piece_color = chessboard[origin[1]][origin[0]][1]
    if ((selected_piece == 'P' and pawn_legal_move(origin, destination)) or 
        (selected_piece == 'R' and rook_legal_move(origin, destination)) or          
        (selected_piece == 'B' and bishop_legal_move(origin, destination)) or
        (selected_piece == 'N' and knight_legal_move(origin, destination)) or
        (selected_piece == 'Q' and queen_legal_move(origin, destination)) or
        (selected_piece == 'K' and king_legal_move(origin, destination))):
        return not checked_after_move(origin, destination, selected_piece_color)

def checked_after_move(origin, destination, selected_piece_color):
    global white_pieces_locations
    global black_pieces_locations
    global kings_locations
    global chessboard
    temp_board = copy.deepcopy(chessboard)
    temp_white_locations = copy.deepcopy(white_pieces_locations)
    temp_black_locations = copy.deepcopy(black_pieces_locations)
    temp_kings_locations = copy.deepcopy(kings_locations)
    move(origin, destination)
    if (selected_piece_color == 'b' and is_checked(kings_locations['b'], 'b') or
        selected_piece_color == 'w' and is_checked(kings_locations['w'], 'w')):

            white_pieces_locations = temp_white_locations
            black_pieces_locations = temp_black_locations
            kings_locations = temp_kings_locations
            chessboard = temp_board
            return True
        
    else:
        white_pieces_locations = temp_white_locations
        black_pieces_locations = temp_black_locations
        kings_locations = temp_kings_locations
        chessboard = temp_board
        return False

def update_locations(origin, destination):
    selected_piece = chessboard[origin[1]][origin[0]][0]
    selected_piece_color = chessboard[origin[1]][origin[0]][1]
    if selected_piece == 'K':
        kings_locations[selected_piece_color] = destination
    elif selected_piece_color == 'w':
        white_pieces_locations[white_pieces_locations.index(origin)] = destination
    elif selected_piece_color == 'b':
        black_pieces_locations[black_pieces_locations.index(origin)] = destination

def move(origin, destination):
    selected_piece_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0: empty_tile = True
    else: empty_tile = False
    oy, ox = origin[1], origin[0]
    dy, dx = destination[1], destination[0]
    update_locations(origin, destination)   

    if empty_tile:
        chessboard[oy][ox], chessboard[dy][dx] = chessboard[dy][dx], chessboard[oy][ox]
    else:
        if selected_piece_color == 'w' and chessboard[dy][dx][0] != 'K':
            black_pieces_locations.remove(destination)
        elif selected_piece_color == 'b' and chessboard[dy][dx][0] != 'K':
            white_pieces_locations.remove(destination)
        chessboard[dy][dx] = ()
        chessboard[oy][ox], chessboard[dy][dx] = chessboard[dy][dx], chessboard[oy][ox]
    
def in_bounds(origin):
    return 0 <= origin[0] <= 7 and 0 <= origin[1] <= 7

def pawn_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if origin_color == 'w':
        if direction == (0,1):
            return empty_tile
        elif direction == (0,2):
            return origin[1] == 1 and empty_tile
        elif direction == (1,1) or direction == (-1,1):
            return not empty_tile and destination_color == 'b'
    elif origin_color == 'b':
        if direction == (0,-1):
            return empty_tile
        elif direction == (0,-2):
            return origin[1] == 6 and empty_tile
        elif direction == (1,-1) or direction == (-1,-1):
            return not empty_tile and destination_color == 'w'

def rook_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if direction[0] == 0 and isinstance(direction[1], int):
        if direction[1] > 0:
            for i in range(origin[1] + 1, destination[1]):
                if len(chessboard[i][origin[0]]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
        elif direction[1] < 0:
            for i in range(origin[1] -1, destination[1], -1):
                if len(chessboard[i][origin[0]]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

    elif direction[1] == 0 and isinstance(direction[0], int):
        if direction[0] > 0:
            for i in range(origin[0] + 1, destination[0]):
                if len(chessboard[origin[1]][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
        elif direction[0] < 0:
            for i in range(origin[0] -1, destination[0], -1):
                if len(chessboard[origin[1]][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

def bishop_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if abs(direction[0]) == abs(direction[1]):
        if direction[0] > 0 and direction[1] > 0:
            for i,j in zip(range(origin[0] + 1, destination[0]), range(origin[1] + 1, destination[1])):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

        elif direction[0] > 0 and direction[1] < 0:
            for i, j in zip(range(origin[0] + 1, destination[0]), range(origin[1] - 1, destination[1], -1)):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
  
        elif direction[0] < 0 and direction[1] > 0:
            for i, j in zip(range(origin[0] - 1, destination[0], -1), range(origin[1] + 1, destination[1])):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

        elif direction[0] < 0 and direction[1] < 0:
            for i,j in zip(range(origin[0] - 1, destination[0], -1), range(origin[1] - 1, destination[1], -1)):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

def knight_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if (abs(direction[0]), abs(direction[1])) == (1,2) or (abs(direction[0]), abs(direction[1])) == (2,1):
        return empty_tile or origin_color != destination_color 

def king_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if direction in [(1, 1), (1, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]:
        return empty_tile or origin_color != destination_color

def queen_legal_move(origin, destination):
    origin_color = chessboard[origin[1]][origin[0]][1]
    if len(chessboard[destination[1]][destination[0]]) == 0:
        empty_tile = True
    else:
        empty_tile = False
        destination_color = chessboard[destination[1]][destination[0]][1]
    direction = tuple(map(lambda x, y: x - y, destination, origin))
    if direction[0] == 0 and isinstance(direction[1], int):
        if direction[1] > 0:
            for i in range(origin[1] + 1, destination[1]):
                if len(chessboard[i][origin[0]]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
        elif direction[1] < 0:
            for i in range(origin[1] -1, destination[1], -1):
                if len(chessboard[i][origin[0]]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

    elif direction[1] == 0 and isinstance(direction[0], int):
        if direction[0] > 0:
            for i in range(origin[0] + 1, destination[0]):
                if len(chessboard[origin[1]][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
        elif direction[0] < 0:
            for i in range(origin[0] -1, destination[0], -1):
                if len(chessboard[origin[1]][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

    elif abs(direction[0]) == abs(direction[1]):
        if direction[0] > 0 and direction[1] > 0:
            for i,j in zip(range(origin[0] + 1, destination[0]), range(origin[1] + 1, destination[1])):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

        elif direction[0] > 0 and direction[1] < 0:
            for i, j in zip(range(origin[0] + 1, destination[0]), range(origin[1] - 1, destination[1], -1)):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
  
        elif direction[0] < 0 and direction[1] > 0:
            for i, j in zip(range(origin[0] - 1, destination[0], -1), range(origin[1] + 1, destination[1])):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color

        elif direction[0] < 0 and direction[1] < 0:
            for i,j in zip(range(origin[0] - 1, destination[0], -1), range(origin[1] - 1, destination[1], -1)):
                if len(chessboard[j][i]) != 0:
                    return False
            else: return empty_tile or origin_color != destination_color
 
def get_the_coordinates(origin, destination):
    origin_column = ord(origin[0]) - 97
    origin_row = int(origin[1]) - 1
    destination_column = ord(destination[0]) - 97
    destination_row = int(destination[1]) - 1
    return ((origin_column, origin_row), (destination_column, destination_row))

def is_checked(king_location, king_color):
    pieces_checked_king = []
    if king_color == 'w':
        for location in black_pieces_locations:
            if can_be_moved(location, king_location):
                pieces_checked_king.append(location)

        if can_be_moved(kings_locations['b'], king_location):
           pieces_checked_king.append(kings_locations['b']) 

    elif king_color == 'b':
        for location in white_pieces_locations:
            if can_be_moved(location, king_location):
                pieces_checked_king.append(location)

        if can_be_moved(kings_locations['w'], king_location):
           pieces_checked_king.append(kings_locations['w'])

    return pieces_checked_king

def removable_threat(king_location, king_color):            
    pieces_checked_king = is_checked(king_location, king_color)
    path_tiles = []
    the_piece_location = pieces_checked_king[0]
    the_piece = chessboard[the_piece_location[1]][the_piece_location[0]][0]
    if the_piece != 'N':
        direction = tuple(map(lambda x, y: x - y, king_location, the_piece_location))

        if direction[0] == 0 and isinstance(direction[1], int):
            if direction[1] > 0:
                for i in range(the_piece_location[1], king_location[1]):
                    path_tiles.append((the_piece_location[0], i))              
            elif direction[1] < 0:
                for i in range(the_piece_location[1], king_location[1], -1):
                    path_tiles.append((the_piece_location[0], i))

        elif direction[1] == 0 and isinstance(direction[0], int):
            if direction[0] > 0:
                for i in range(the_piece_location[0], king_location[0]):
                    path_tiles.append((i, the_piece_location[1]))        
            elif direction[0] < 0:
                for i in range(the_piece_location[0], king_location[0], -1):
                    path_tiles.append((i, the_piece_location[1]))
        
        elif abs(direction[0]) == abs(direction[1]):
            if direction[0] > 0 and direction[1] > 0:
                for i,j in zip(range(the_piece_location[0], king_location[0]), range(the_piece_location[1], king_location[1])):
                    path_tiles.append((i,j))    

            elif direction[0] > 0 and direction[1] < 0:
                for i, j in zip(range(the_piece_location[0], king_location[0]), range(the_piece_location[1], king_location[1], -1)):
                    path_tiles.append((i,j))
                
            elif direction[0] < 0 and direction[1] > 0:
                for i, j in zip(range(the_piece_location[0], king_location[0], -1), range(the_piece_location[1], king_location[1])):
                    path_tiles.append((i,j))
                
            elif direction[0] < 0 and direction[1] < 0:
                for i,j in zip(range(the_piece_location[0], king_location[0], -1), range(the_piece_location[1], king_location[1], -1)):
                    path_tiles.append((i,j))
    else:
        path_tiles.append(the_piece_location)
    
    if king_color == 'w':
        for location in white_pieces_locations:
            for tile in path_tiles:
                if can_be_moved(location, tile):
                    return True
        else: return False
    
    elif king_color == 'b':
        for location in black_pieces_locations:
            for tile in path_tiles:
                if can_be_moved(location, tile):
                    return True
        else: return False

def is_checkmated(king_location, king_color):
    king_possible_moves = [(1, 1), (1, -1), (1, 0), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for direction in king_possible_moves:
        destination = tuple(map(lambda x, y: x + y, king_location, direction))
        if in_bounds(destination) and can_be_moved(king_location, destination):
            return False
    else:
        return not removable_threat(king_location, king_color)

def pawn_reached_end(selected_color, destination_pos):
    if selected_color == 'w':
        return destination_pos[1] == 7
    elif selected_color == 'b':
        return destination_pos[1] == 0 

def can_castling(selected_color, origin_pos, destination_pos):
    empty_path = True
    path_under_attack = False
    if selected_color == 'w' and castling_situation['wK']:
        if destination_pos == (6,0) and castling_situation['rwR']:
            for i in range(origin_pos[0] + 1, 7):
                if len(chessboard[0][i]) != 0: 
                    return False
            for location in black_pieces_locations:
                if can_be_moved(location, (5,0)):
                    return False
            return (empty_path and 
                    not path_under_attack and
                    not is_checked(origin_pos, selected_color) and
                    not checked_after_move(origin_pos, destination_pos, selected_color))
        
        elif destination_pos == (2,0) and castling_situation['lwR']:
            for i in range(origin_pos[0] - 1, 0, -1):
                if len(chessboard[0][i]) != 0: 
                    return False
            for location in black_pieces_locations:
                if can_be_moved(location, (3,0)):
                    return False
            return (empty_path and 
                    not path_under_attack and
                    not is_checked(origin_pos, selected_color) and
                    not checked_after_move(origin_pos, destination_pos, selected_color))
    
    elif selected_color == 'b' and castling_situation['bK']:
        if destination_pos == (6,7) and castling_situation['rbR']:
            for i in range(origin_pos[0] + 1, 7):
                if len(chessboard[7][i]) != 0: 
                    return False
            for location in white_pieces_locations:
                if can_be_moved(location, (5,7)):
                    return False
            return (empty_path and 
                    not path_under_attack and
                    not is_checked(origin_pos, selected_color) and
                    not checked_after_move(origin_pos, destination_pos, selected_color))
        
        elif destination_pos == (2,7) and castling_situation['lbR']:
            for i in range(origin_pos[0] - 1, 0, -1):
                if len(chessboard[7][i]) != 0: 
                    return False
            for location in white_pieces_locations:
                if can_be_moved(location, (3,7)):
                    return False
            return (empty_path and 
                    not path_under_attack and
                    not is_checked(origin_pos, selected_color) and
                    not checked_after_move(origin_pos, destination_pos, selected_color))     

def update_castling_situation(selected_piece, selected_color, origin_pos):
    if selected_piece == 'K':
        if selected_color == 'w' and origin_pos == (4, 0):
            castling_situation['wK'] = False
        elif selected_color == 'b' and origin_pos == (4, 7):
            castling_situation['bK'] = False
        else: return
    elif selected_piece == 'R':
        if selected_color == 'w' and origin_pos == (7, 0):
            castling_situation['rwR'] = False
        elif selected_color == 'w' and origin_pos == (0, 0):
            castling_situation['lwR'] = False
        elif selected_color == 'b' and origin_pos == (7, 7):
            castling_situation['rbR'] = False
        elif selected_color == 'b' and origin_pos == (0, 7):
            castling_situation['lbR'] = False
        else: return


castling_situation = {'wK': True, 'bK': True, 'rwR': True, 'lwR': True, 'rbR': True, 'lbR': True }
playing = True
white_turn = True
#print("\nEnter the origin and destination coordinates to move the chess piece e.g., b1 c3.")
while playing:
    printChessBoard(chessboard)
    while True:
        try:
            origin, destination = input(">>> ").split()
            origin_pos, destination_pos = get_the_coordinates(origin.lower(), destination.lower())
        except KeyboardInterrupt: exit()
        except: continue
        if not in_bounds(origin_pos) or not in_bounds(destination_pos):
            print('The selection is off the chessboard.')
        elif len(chessboard[origin_pos[1]][origin_pos[0]]) == 0:
            print('You have not selected any pieces')
        elif white_turn and chessboard[origin_pos[1]][origin_pos[0]][1] == 'b':
            print('You have selected the wrong piece.')
        elif not white_turn and chessboard[origin_pos[1]][origin_pos[0]][1] == 'w':
            print('You have selected the wrong piece.')
        else:
            selected_piece, selected_color = chessboard[origin_pos[1]][origin_pos[0]]
            if can_be_moved(origin_pos, destination_pos):
                move(origin_pos, destination_pos)
                if selected_piece == 'R' or selected_piece == 'K':
                    update_castling_situation(selected_piece, selected_color, origin_pos)
                break
            elif (selected_piece == 'K' and
                  origin_pos in [(4,0), (4,7)] and
                  destination_pos in [(6,0), (2,0), (6,7), (2,7)] and 
                  can_castling(selected_color, origin_pos, destination_pos)):
                move(origin_pos, destination_pos)
                if destination_pos == (6,0):
                    move((7,0), (5,0))
                elif destination_pos == (2,0):
                    move((0,0), (3,0))
                elif destination_pos == (6,7):
                    move((7,7), (5,7))
                elif destination_pos == (2,7):
                    move((0,7), (3,7))
                break
            else: print('This piece cannot be moved to its destination.')
    
    if selected_piece == 'P' and pawn_reached_end(selected_color, destination_pos):
        while True:
            print('Select Your Piece: [B]ishop, [R]ook, [Q]ueen or K[N]ight')
            chosen_piece = input().upper()
            valid_pieces = ['B', 'R', 'Q', 'N']
            if chosen_piece in valid_pieces:
                chessboard[destination_pos[1]][destination_pos[0]] = (chosen_piece, selected_color)
                break
            else:
                print('Invalid choice.')
              
    if is_checked(kings_locations['w'], 'w'):
        print("The white's King is checked")
        if is_checkmated(kings_locations['w'], 'w'):
            printChessBoard()
            print('Black Won!')
            playing = False

    elif is_checked(kings_locations['b'], 'b'):
        print("The black's King is checked")
        if is_checkmated(kings_locations['b'], 'b'):
            printChessBoard()
            print('White Won!')
            playing = False
    
    white_turn = not white_turn


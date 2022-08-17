import re
import copy
import time
from tables import *
class Game:

    '''
    this is the Game class that stores the current game state
    is able to move a piece and stores the current statistics
    of the game

    '''

    def __init__(self):
        #  2D 8x8 list that indicates the piece in that current location
        #  -- reprisents and empty space
        self.board = [
                     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                     ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                     ["--", "--", "--", "--", "--", "--", "--", "--"],
                     ["--", "--", "--", "--", "--", "--", "--", "--"],
                     ["--", "--", "--", "--", "--", "--", "--", "--"],
                     ["--", "--", "--", "--", "--", "--", "--", "--"],
                     ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"], ]

        self.movelog = []
        self.WhitesTurn = True

    def move_piece(self, move):
        self.board[move.current_row][move.current_col] = "--"
        self.board[move.new_row][move.new_col] = move.Piece_type
        self.movelog.append(move)

    def extended_board(self, move, board):
        new_board = copy.deepcopy(board)
        new_board[move.current_row][move.current_col] = "--"
        new_board[move.new_row][move.new_col] = move.Piece_type
        return new_board

    def moved_board(self, move):
        new_board = copy.deepcopy(self.board)
        new_board[move.current_row][move.current_col] = "--"
        new_board[move.new_row][move.new_col] = move.Piece_type
        return new_board

    def wpawn_moves(self, move, board):
        '''
        method that validates wether a pawn move is legal
        moves if valid
        '''
        #  need to add that ist checks if there is ally piece on position it doesnt add
        self.potential_moves = []

        if re.search('^b', board[move.current_row - 1][move.current_col]) is None:
            if board[move.current_row - 1][move.current_col] == '--':
                self.potential_moves.append((move.current_row - 1, move.current_col))
            else:
                pass
        if move.current_col + 1 >= 8:  # checks wether in index range
            pass
        elif re.search('^w', board[move.current_row - 1][move.current_col + 1]) is None:
            if board[move.current_row - 1][move.current_col + 1] != '--':
                self.potential_moves.append((move.current_row - 1, move.current_col + 1))
            else:
                pass
        if move.current_col - 1 <= -1:  # checks wether in index range
            pass
        elif re.search('^w', board[move.current_row - 1][move.current_col - 1]) is None:
            if board[move.current_row - 1][move.current_col - 1] != '--':
                self.potential_moves.append((move.current_row - 1, move.current_col - 1))
            else:
                pass
        if move.current_row == 6:
            if re.search('^b', board[move.current_row - 2][move.current_col]) is None:
                if board[move.current_row - 2][move.current_col] == '--':
                    self.potential_moves.append((move.current_row - 2, move.current_col))
        else:
            pass

        return self.potential_moves

    def bpawn_moves(self, move, board):
        '''
        method that validates wether a pawn move is legal
        moves if valid
        '''
        #  need to add that ist checks if there is ally piece on position it doesnt add
        self.potential_moves = []

        if re.search('^w', board[move.current_row + 1][move.current_col]) is None:
            if board[move.current_row + 1][move.current_col] == '--':
                self.potential_moves.append((move.current_row + 1, move.current_col))
            else:
                pass
        if move.current_col + 1 >= 8:  # checks wether in index range
            pass
        elif re.search('^b', board[move.current_row + 1][move.current_col + 1]) is None:
            if board[move.current_row + 1][move.current_col + 1] != '--':
                self.potential_moves.append((move.current_row + 1, move.current_col + 1))
            else:
                pass
        if move.current_col - 1 <= -1:  # checks wether in index range
            pass
        elif re.search('^b', board[move.current_row + 1][move.current_col - 1]) is None:
            if board[move.current_row + 1][move.current_col - 1] != '--':
                self.potential_moves.append((move.current_row + 1, move.current_col - 1))
            else:
                pass
        if move.current_row == 1:
            if re.search('^w', board[move.current_row + 2][move.current_col]) is None:
                if board[move.current_row + 2][move.current_col] == '--':
                    self.potential_moves.append((move.current_row + 2, move.current_col))
        else:
            pass

        return self.potential_moves

    def rook_moves(self, move, board, colour):
        self.potential_moves = []
        for x in range(1, move.current_row + 1):
            if board[move.current_row - x][move.current_col] == '--':
                self.potential_moves.append((move.current_row - x, move.current_col))
            elif re.search('^' + colour, board[move.current_row - x][move.current_col]) is None:
                self.potential_moves.append((move.current_row - x, move.current_col))
                break
            else:
                break

        for x in range(1, move.current_col + 1):
            if board[move.current_row][move.current_col - x] == '--':
                self.potential_moves.append((move.current_row, move.current_col - x))
            elif re.search('^' + colour, board[move.current_row][move.current_col - x]) is None:
                self.potential_moves.append((move.current_row, move.current_col - x))
                break
            else:
                break

        for x in range(1, 8 - move.current_row):
            if board[move.current_row + x][move.current_col] == '--':
                self.potential_moves.append((move.current_row + x, move.current_col))
            elif re.search('^' + colour, board[move.current_row + x][move.current_col]) is None:
                self.potential_moves.append((move.current_row + x, move.current_col))
                break
            else:
                break

        for x in range(1, 8 - move.current_col):
            if board[move.current_row][move.current_col + x] == '--':
                self.potential_moves.append((move.current_row, move.current_col + x))
            elif re.search('^' + colour, board[move.current_row][move.current_col + x]) is None:
                self.potential_moves.append((move.current_row, move.current_col + x))
                break
            else:
                break
        return self.potential_moves

    def bishop_moves(self, move, board, colour):
        self.potential_moves = []
        for x in range(1, move.current_row + 1):
            if move.current_row - x > -1 and move.current_col - x > -1:
                if board[move.current_row - x][move.current_col - x] == '--':
                    self.potential_moves.append((move.current_row - x, move.current_col - x))
                elif re.search('^' + colour, board[move.current_row - x][move.current_col - x]) is None:
                    self.potential_moves.append((move.current_row - x, move.current_col - x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, move.current_row + 1):
            if move.current_row - x > -1 and move.current_col + x < 8:
                if board[move.current_row - x][move.current_col + x] == '--':
                    self.potential_moves.append((move.current_row - x, move.current_col + x))
                elif re.search('^' + colour, board[move.current_row - x][move.current_col + x]) is None:
                    self.potential_moves.append((move.current_row - x, move.current_col + x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, 8 - move.current_row):
            if move.current_row + x < 8 and move.current_col - x > -1:
                if board[move.current_row + x][move.current_col - x] == '--':
                    self.potential_moves.append((move.current_row + x, move.current_col - x))
                elif re.search('^' + colour, board[move.current_row + x][move.current_col - x]) is None:
                    self.potential_moves.append((move.current_row + x, move.current_col - x))
                    break
                else:
                    break
            else:
                break

        for x in range(1, 8 - move.current_row):
            if move.current_row + x < 8 and move.current_col + x < 8:
                if board[move.current_row + x][move.current_col + x] == '--':
                    self.potential_moves.append((move.current_row + x, move.current_col + x))
                elif re.search('^' + colour, board[move.current_row + x][move.current_col + x]) is None:
                    self.potential_moves.append((move.current_row + x, move.current_col + x))
                    break
                else:
                    break
            else:
                break

        return self.potential_moves

    def knight_moves(self, move, board, colour):
        self.potential_moves = []
        if move.current_row + 1 < 8 and move.current_col + 2 < 8:
            if re.search('^' + colour, board[move.current_row + 1][move.current_col + 2]) is None:
                self.potential_moves.append((move.current_row + 1, move.current_col + 2))
            elif board[move.current_row + 1][move.current_col + 2] == '--':
                self.potential_moves.append((move.current_row + 1, move.current_col + 2))
            else:
                pass

        if move.current_row + 1 < 8 and move.current_col - 2 > -1:
            if re.search('^' + colour, board[move.current_row + 1][move.current_col - 2]) is None:
                self.potential_moves.append((move.current_row + 1, move.current_col - 2))
            elif board[move.current_row + 1][move.current_col - 2] == '--':
                self.potential_moves.append((move.current_row + 1, move.current_col - 2))
            else:
                pass

        if move.current_row + 2 < 8 and move.current_col + 1 < 8:
            if re.search('^' + colour, board[move.current_row + 2][move.current_col + 1]) is None:
                self.potential_moves.append((move.current_row + 2, move.current_col + 1))
            elif board[move.current_row + 2][move.current_col + 1] == '--':
                self.potential_moves.append((move.current_row + 2, move.current_col + 1))
            else:
                pass

        if move.current_row + 2 < 8 and move.current_col - 1 > -1:
            if re.search('^' + colour, board[move.current_row + 2][move.current_col - 1]) is None:
                self.potential_moves.append((move.current_row + 2, move.current_col - 1))
            elif board[move.current_row + 2][move.current_col - 1] == '--':
                self.potential_moves.append((move.current_row + 2, move.current_col - 1))
            else:
                pass

        if move.current_row - 2 > -1 and move.current_col + 1 < 8:
            if re.search('^' + colour, board[move.current_row - 2][move.current_col + 1]) is None:
                self.potential_moves.append((move.current_row - 2, move.current_col + 1))
            elif board[move.current_row - 2][move.current_col + 1] == '--':
                self.potential_moves.append((move.current_row - 2, move.current_col + 1))
            else:
                pass

        if move.current_row - 2 > -1 and move.current_col - 1 > -1:
            if re.search('^' + colour, board[move.current_row - 2][move.current_col - 1]) is None:
                self.potential_moves.append((move.current_row - 2, move.current_col - 1))
            elif board[move.current_row - 2][move.current_col - 1] == '--':
                self.potential_moves.append((move.current_row - 2, move.current_col - 1))
            else:
                pass

        if move.current_row - 1 > -1 and move.current_col + 2 < 8:
            if re.search('^' + colour, board[move.current_row - 1][move.current_col + 2]) is None:
                self.potential_moves.append((move.current_row - 1, move.current_col + 2))
            elif board[move.current_row - 1][move.current_col + 2] == '--':
                self.potential_moves.append((move.current_row - 1, move.current_col + 2))
            else:
                pass

        if move.current_row - 1 > -1 and move.current_col - 2 > -1:
            if re.search('^' + colour, board[move.current_row - 1][move.current_col - 2]) is None:
                self.potential_moves.append((move.current_row - 1, move.current_col - 2))
            elif board[move.current_row - 1][move.current_col - 2] == '--':
                self.potential_moves.append((move.current_row - 1, move.current_col - 2))
            else:
                pass

        return self.potential_moves

    def king_moves(self, move, board, colour):
        '''
        needs index checks
        '''
        self.potential_moves = []
        self.legal_moves = []
        for x in range(0, 9):
            for y in range(0, 9):
                iter_coord = (x, y)
                if move.current_row - iter_coord[0] == 1 or move.current_row - iter_coord[0] == -1:
                    if move.current_col - iter_coord[1] == 1 or move.current_col - iter_coord[1] == -1:
                        self.potential_moves.append(iter_coord)
                    elif move.current_col == iter_coord[1]:
                        self.potential_moves.append(iter_coord)
                if move.current_row == iter_coord[0]:
                    if move.current_col - iter_coord[1] == 1 or move.current_col - iter_coord[1] == -1:
                        self.potential_moves.append(iter_coord)
                    elif move.current_col == iter_coord[1]:
                        self.potential_moves.append(iter_coord)

        for item in self.potential_moves:
            if item[0] < 0 or item[0] > 7:
                pass
            elif item[1] < 0 or item[1] > 7:
                pass
            elif re.search('^' + colour, board[item[0]][item[1]]) is not None:
                pass
            else:
                self.legal_moves.append(item)

        return self.legal_moves

    def queen_moves(self, move, board, colour):
        self.potential_moves = self.bishop_moves(move, board, colour) + self.rook_moves(move, board, colour)
        return self.potential_moves

    def all_moves(self, board, colour):
        '''
        function used to collect all the moves of the oponent
        needed for check and checkmate validation
        needs board and colour of side that needs to be checked
        as arguements
        '''
        self.moves_list = []
        self.movelist = []

        if colour == 'w':
            for y in range(0, 8):
                for x in range(0, 8):
                    coord = (y, x)
                    move_i = Move(coord, (0, 0), board)
                    if board[move_i.current_row][move_i.current_col] == "wp":
                        self.moves_list.append(self.wpawn_moves(move_i, board))
                    if board[move_i.current_row][move_i.current_col] == "wR":
                        self.moves_list.append(self.rook_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "wB":
                        self.moves_list.append(self.bishop_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "wN":
                        self.moves_list.append(self.knight_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "wK":
                        self.moves_list.append(self.king_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "wQ":
                        self.moves_list.append(self.queen_moves(move_i, board, colour))

        elif colour == 'b':
            for y in range(0, 8):
                for x in range(0, 8):
                    coord = (y, x)
                    move_i = Move(coord, (0, 0), board)
                    if board[move_i.current_row][move_i.current_col] == "bp":
                        self.moves_list.append(self.bpawn_moves(move_i, board))
                    if board[move_i.current_row][move_i.current_col] == "bR":
                        self.moves_list.append(self.rook_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "bB":
                        self.moves_list.append(self.bishop_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "bN":
                        self.moves_list.append(self.knight_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "bK":
                        self.moves_list.append(self.king_moves(move_i, board, colour))
                    if board[move_i.current_row][move_i.current_col] == "bQ":
                        self.moves_list.append(self.queen_moves(move_i, board, colour))

        for item in self.moves_list:
            for point in item:
                self.movelist.append(point)

        return self.movelist

    def checkmate_moves(self, board, colour):
        '''
        returns dictionary of
        {piece coord : [piece type, possible moves]}
        '''
        self.moves_dict = {}

        if colour == 'w':
            for y in range(0, 8):
                for x in range(0, 8):
                    coord = (y, x)
                    move_i = Move(coord, (0, 0), board)
                    if board[move_i.current_row][move_i.current_col] == "wp":
                        self.moves_dict.update({coord: ["wp", self.wpawn_moves(move_i, board)]})
                    if board[move_i.current_row][move_i.current_col] == "wR":
                        self.moves_dict.update({coord: ["wR", self.rook_moves(move_i, board, 'w')]})
                    if board[move_i.current_row][move_i.current_col] == "wB":
                        self.moves_dict.update({coord: ["wB", self.bishop_moves(move_i, board, 'w')]})
                    if board[move_i.current_row][move_i.current_col] == "wN":
                        self.moves_dict.update({coord: ["wN", self.knight_moves(move_i, board, 'w')]})
                    if board[move_i.current_row][move_i.current_col] == "wK":
                        self.moves_dict.update({coord: ["wK", self.king_moves(move_i, board, 'w')]})
                    if board[move_i.current_row][move_i.current_col] == "wQ":
                        self.moves_dict.update({coord: ["wQ", self.queen_moves(move_i, board, 'w')]})

        if colour == 'b':
            for y in range(0, 8):
                for x in range(0, 8):
                    coord = (y, x)
                    move_i = Move(coord, (0, 0), board)
                    if board[move_i.current_row][move_i.current_col] == "bp":
                        self.moves_dict.update({coord: ["bp", self.bpawn_moves(move_i, board)]})
                    if board[move_i.current_row][move_i.current_col] == "bR":
                        self.moves_dict.update({coord: ["bR", self.rook_moves(move_i, board, 'b')]})
                    if board[move_i.current_row][move_i.current_col] == "bB":
                        self.moves_dict.update({coord: ["bB", self.bishop_moves(move_i, board, 'b')]})
                    if board[move_i.current_row][move_i.current_col] == "bN":
                        self.moves_dict.update({coord: ["bN", self.knight_moves(move_i, board, 'b')]})
                    if board[move_i.current_row][move_i.current_col] == "bK":
                        self.moves_dict.update({coord: ["bK", self.king_moves(move_i, board, 'b')]})
                    if board[move_i.current_row][move_i.current_col] == "bQ":
                        self.moves_dict.update({coord: ["bQ", self.queen_moves(move_i, board, 'b')]})

        return self.moves_dict

    def check(self, board, colour):
        '''
        check wether game after user has made a move is in check
        if True not in check
        False means in check
        if false move should be blocked
        '''

        if colour == 'w':
            for y in range(0, 8):
                for x in range(0, 8):
                    if board[y][x] == 'wK':
                        if (y, x) in self.all_moves(board, 'b'):
                            return False
            else:
                return True

        if colour == 'b':
            for y in range(0, 8):
                for x in range(0, 8):
                    if board[y][x] == 'bK':
                        if (y, x) in self.all_moves(board, 'w'):
                            return False
            else:
                return True

    def tree_contructer(self, dictionary, board):
        self.gamestates = []
        for item in dictionary.keys():
            for coord in dictionary[item][1]:
                move = Move(item, coord, board)
                self.gamestates.append(self.extended_board(move, board))

        return self.gamestates

    def checkmate(self, colour, board):
        '''
        generates a tree of depth one of all possible game states of current gamestate
        if one not in check is detected the loop is broken and it returns true
        if they are all in check count variable will be the same as the len of this
        gamestate list meaning there is no way out for the user
        '''
        self.test = []
        self.count = 0
        self.user_moves = self.tree_contructer(self.checkmate_moves(board, colour), board)
        for item in self.user_moves:
            if self.check(item, colour) is True:
                return True
            elif self.check(item, colour) is False:
                self.count = self.count + 1

            if self.count == len(self.user_moves):
                return False

    def heuristic(self, board):
        score = 0
        for y in range(0, 8):
            for x in range(0, 8):
                if board[y][x] == "bp":
                    score = score + 10 + PAWN_TABLE[y][x]
                if board[y][x] == "bR":
                    score = score + 50 + ROOK_TABLE[y][x]
                if board[y][x] == "bB":
                    score = score + 33 + BISHOP_TABLE[y][x]
                if board[y][x] == "bN":
                    score = score + 32 + KNIGHT_TABLE[y][x]
                if board[y][x] == "bK":
                    score = score + 900 + KING_TABLE[y][x]
                if board[y][x] == "bQ":
                    score = score + 90 + QUEEN_TABLE[y][x]
                if board[y][x] == "wp":
                    score = score - 10 - PAWN_TABLE[y][x]
                if board[y][x] == "wR":
                    score = score - 50 - ROOK_TABLE[y][x]
                if board[y][x] == "wB":
                    score = score - 33 - BISHOP_TABLE[y][x]
                if board[y][x] == "wN":
                    score = score - 32 - KNIGHT_TABLE[y][x]
                if board[y][x] == "wK":
                    score = score - 900 - KING_TABLE[y][x]
                if board[y][x] == "wQ":
                    score = score - 90 - QUEEN_TABLE[y][x]
        return score

    def ai_data(self, board):
        root_node = Node(root=True, gamestate=board)
        for item in (self.tree_contructer(self.checkmate_moves(root_node.gamestate, 'b'), root_node.gamestate)):
            root_node.children.append(Node(parent=root_node, gamestate=item))

        for item in root_node.children:
            for x in (self.tree_contructer(self.checkmate_moves(item.gamestate, 'w'), item.gamestate)):
                item.children.append(Node(parent=item, gamestate=x))

        for item in root_node.children:
            for x in item.children:
                maximum = -10000000
                for y in (self.tree_contructer(self.checkmate_moves(x.gamestate, 'b'), x.gamestate)):
                    if self.heuristic(y) > maximum:
                        maximum = self.heuristic(y)
                x.score = maximum

        for item in root_node.children:
            minimum = 1000000
            for x in item.children:
                if x.score < minimum:
                    minimum = x.score
            item.score = minimum
            print(item.score)

        maximum = -10000000
        best_move = None
        for item in root_node.children:
            if item.score > maximum:
                maximum = item.score
                print(item.score)
                best_move = item.gamestate

        return best_move

class Move:

    '''
    this class simply establishes the type of piece, its current position and
    what end location it is going to be placed at

    '''

    def __init__(self, current_sq, new_sq, board):
        self.current_coord = current_sq
        self.current_row = current_sq[0]
        self.current_col = current_sq[1]
        self.new_row = new_sq[0]
        self.new_col = new_sq[1]
        self.new_coord = new_sq
        self.Piece_type = board[self.current_row][self.current_col]  # means we can hold piece type
        self.piece_moved = board[self.new_row][self.new_col]

class Node:

    def __init__(self, root=False, parent=None, gamestate=None):
        self.root = root
        self.parent = parent
        self.gamestate = gamestate
        self.score = 0
        self.children = []

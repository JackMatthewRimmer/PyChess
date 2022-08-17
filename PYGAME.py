import pygame as p
from MainGame import Game, Move
import sys
import time

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# create a dictionary of loaded peice images for pygame


def Load_Images():
    pieces = ['wp', 'bp', 'bB', 'bN', 'bR', 'bQ', 'bK',
              'wB', 'wN', 'wR', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('textures/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))


'''
main function that brings all subprocesses together,
also deals with the event handles provided within pygame

'''


def Main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    game = Game()
    screen.fill(p.Color('white'))
    Load_Images()
    running = True
    sq_selected = ()  # iniitially has no coord
    click_list = []  # initially has no value
    while running:
        if game.WhitesTurn is False:
            if game.checkmate('b', game.board) is True:
                game.board = game.ai_data(game.board)
                game.WhitesTurn = not game.WhitesTurn
            else:
                print('checkmate')
                sys.exit()
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONUP:
                location = p.mouse.get_pos()  # location of mouse
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, column):
                    sq_selected = ()  # reverse select back to normal
                    click_list = []
                else:
                    sq_selected = (row, column)
                    click_list.append(sq_selected)
                if len(click_list) == 2:
                    moves = Move(click_list[0], click_list[1], game.board)

                    if game.WhitesTurn is True:
                        if game.checkmate('w', game.board) is True:
                            if game.check(game.moved_board(moves), 'w') is True:
                                if white_moves(moves, game.board, game) is True:
                                    game.move_piece(moves)
                                    game.WhitesTurn = not game.WhitesTurn
                                else:
                                    pass
                            else:
                                print('check w')
                        else:
                            print("checkmate")
                            sys.exit()

                    click_list = []
                    sq_selected = ()



        Draw_Game(screen, game)
        clock.tick(MAX_FPS)
        p.display.flip()


def Draw_Game(screen, game):
    Draw_Board(screen)
    Draw_Pieces(screen, game.board)


'''
both helper functions for the draw game function where the board
and pieces are brought onto the users screen

'''


def Draw_Board(screen):
    colours = [p.Color("white"), p.Color("grey")]
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            colour = colours[((x + y) % 2)]
            p.draw.rect(screen, colour,
                        p.Rect(x * SQ_SIZE, y * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def Draw_Pieces(screen, board):
    for y in range(DIMENSION):
        for x in range(DIMENSION):
            piece = board[x][y]
            if piece != "--":
                screen.blit((IMAGES[piece]),
                            p.Rect(y * SQ_SIZE, x * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def black_moves(move, board, game):
    '''
    function for validating black move attempts
    returns true if legal move was provided
    '''
    if move.Piece_type == "bp":
        if move.new_coord in game.bpawn_moves(move, board):
            return True
    if move.Piece_type == "bR":
        if move.new_coord in game.rook_moves(move, board, 'b'):
            return True
    if move.Piece_type == "bB":
        if move.new_coord in game.bishop_moves(move, board, 'b'):
            return True
    if move.Piece_type == "bN":
        if move.new_coord in game.knight_moves(move, board, 'b'):
            return True
    if move.Piece_type == "bK":
        if move.new_coord in game.king_moves(move, board, 'b'):
            return True
    if move.Piece_type == "bQ":
        if move.new_coord in game.queen_moves(move, board, 'b'):
            return True
    else:
        return False


def white_moves(move, board, game):
    '''
    function for validating white move attempts
    returns true if legal move was provided
    '''
    if move.Piece_type == "wp":
        if move.new_coord in game.wpawn_moves(move, board):
            return True
    if move.Piece_type == "wR":
        if move.new_coord in game.rook_moves(move, board, 'w'):
            return True
    if move.Piece_type == "wB":
        if move.new_coord in game.bishop_moves(move, board, 'w'):
            return True
    if move.Piece_type == "wN":
        if move.new_coord in game.knight_moves(move, board, 'w'):
            return True
    if move.Piece_type == "wK":
        if move.new_coord in game.king_moves(move, board, 'w'):
            return True
    if move.Piece_type == "wQ":
        if move.new_coord in game.queen_moves(move, board, 'w'):
            return True
    else:
        return False


if __name__ == "__main__":
    Main()

import chess
import chess.engine
import random
import numpy
import os
import subprocess
import tensorflow
import tensorflow.keras.callbacks as callbacks
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
from keras.models import load_model

STOCKFISHPATH = 'C:/Users/zihan/Desktop/School_Work/Game Design/MLchessAi/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe'

def random_board(max_depth=200):
  board = chess.Board()
  depth = random.randint(0, max_depth)

  for _ in range(depth):
    all_moves = list(board.legal_moves)
    random_move = random.choice(all_moves)
    board.push(random_move)
    if board.is_game_over():
      break

  return board

def stockfish(board, depth):

  engine_path = STOCKFISHPATH

  #if os.path.isfile(engine_path):
  #  print("The engine path exists and is a file.")
  #else:
  #  print("The engine path either does not exist or is not a file.")

  with chess.engine.SimpleEngine.popen_uci(engine_path) as sf:
    result = sf.analyse(board, chess.engine.Limit(depth=depth))
    score = result['score'].white().score()
    return score

board = random_board()
board

#chmod 755 /content/stockfish/stockfish/stockfish-ubuntu-x86-64-sse41-popcnt
#ls -l /content/stockfish/stockfish/stockfish-ubuntu-x86-64-sse41-popcnt

#print(stockfish(board, 20))

squares_index = {
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
}

def square_to_index(square):
  letter = chess.square_name(square)
  return 8 - int(letter[1]), squares_index[letter[0]]

def split_dims(board):
  # this is  the 3d matrix to represent the chessboard
  board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

  # here we add the pieces's view on the matrix
  for piece in chess.PIECE_TYPES:
    for square in board.pieces(piece, chess.WHITE):
      idx = numpy.unravel_index(square, (8,8))
      board3d[piece - 1][7 - idx[0]][idx[1]] = 1
    for square in board.pieces(piece, chess.BLACK):
      idx = numpy.unravel_index(square, (8,8))
      board3d[piece + 5][7 - idx[0]][idx[1]] = 1

  aux = board.turn
  board.turn = chess.WHITE
  for move in board.legal_moves:
    i, j = square_to_index(move.to_square)
    board3d[13][i][j] = 1
  board.turn = aux

  return board3d

split_dims(board)


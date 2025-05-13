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
import chessGame


STOCKFISHPATH = 'C:/Users/zihan/Desktop/School_Work/Game Design/MLchessAi/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe'
model = models.load_model('eval1_model.keras')

def minimax_eval(board):
  board3d = chessGame.split_dims(board)
  board3d = numpy.expand_dims(board3d, 0)
  return model(board3d)[0][0]

def minimax(board, depth, alpha, beta, maximizing_player):
  if depth == 0 or board.is_game_over():
    return minimax_eval(board)

  if maximizing_player:
    max_eval = -numpy.inf
    for move in board.legal_moves:
      board.push(move)
      eval = minimax(board, depth - 1, alpha, beta, False)
      board.pop()
      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
    return max_eval
  else:
    min_eval = numpy.inf
    for move in board.legal_moves:
      board.push(move)
      eval = minimax(board, depth - 1, alpha, beta, True)
      board.pop()
      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
    return min_eval

def get_ai_move(board, depth):
  max_move = None
  max_eval = numpy.inf

  for move in board.legal_moves:
    board.push(move)
    eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, True)
    board.pop()

    if eval <= max_eval:
      max_eval = eval
      max_move = move


  return max_move

"""
board = chess.Board()
board

with chess.engine.SimpleEngine.popen_uci(STOCKFISHPATH) as engine:
  while True:
    move = get_ai_move(board, 1)
    board.push(move)
    print(f'\n{board}')
    if board.is_game_over():
      break

    move = engine.analyse(board, chess.engine.Limit(time=1), info=chess.engine.INFO_PV)['pv'][0]
    board.push(move)
    print(f'\n{board}')
    if board.is_game_over():
      break
"""
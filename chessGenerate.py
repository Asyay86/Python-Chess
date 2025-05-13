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

# Initialize the Stockfish engine
engine = subprocess.Popen([STOCKFISHPATH], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Set the思考深度 to 1 for faster evaluations
engine.stdin.write('setoption name Skill Level value 1\n')
engine.stdin.flush()

# Initialize empty numpy arrays for board positions and evaluations
board_positions = numpy.empty(100000, dtype=object)
evaluations = numpy.empty(100000, dtype=float)

data_dict = {}
# Generate 10000 random boards
for i in range(100000):
    # Create a new random board
    board = chessGame.random_board()

    # Extract the evaluation from the Stockfish output
    evaluation = chessGame.stockfish(board, 0)

    while (evaluation is None or evaluation == 0):
      board = chessGame.random_board()
      evaluation = chessGame.stockfish(board, 0)

    #print(evaluation)

    # Append the board position and evaluation to the arrays
    board_positions[i] = chessGame.split_dims(board)
    evaluations[i] = evaluation
    

board_positions_4d = numpy.stack(board_positions, axis=0)
evaluations_4d = numpy.stack(evaluations, axis=0)
data_dict = {'b': board_positions_4d, 'v': evaluations_4d}

# Save the dataset to a file
numpy.savez('zero.npz', **data_dict)
print('done')
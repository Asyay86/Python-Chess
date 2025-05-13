import pygame
import subprocess
import chess
import chess.engine
import chessPlay
import chessGame

# Initialize Pygame
pygame.init()

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STOCKFISHPATH = 'C:/Users/zihan/Desktop/School_Work/Game Design/MLchessAi/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe'

# Set up the window
WIDTH = HEIGHT = 480
WINDOW_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess GUI")

# Load chessboard and pieces images
board_image = pygame.image.load("resources/chessboard.png")
board_image = pygame.transform.scale(board_image, (WIDTH, HEIGHT))

# Function to draw the chessboard
def draw_board():
    screen.blit(board_image, (0, 0))

# Function to draw pieces
def draw_pieces(board):
    piece_images = {
        'P': pygame.image.load("resources/wpawn.png"),
        'N': pygame.image.load("resources/wknight.png"),
        'B': pygame.image.load("resources/wbishop.png"),
        'R': pygame.image.load("resources/wrook.png"),
        'Q': pygame.image.load("resources/wqueen.png"),
        'K': pygame.image.load("resources/wking.png"),
        'p': pygame.image.load("resources/bpawn.png"),
        'n': pygame.image.load("resources/bknight.png"),
        'b': pygame.image.load("resources/bbishop.png"),
        'r': pygame.image.load("resources/brook.png"),
        'q': pygame.image.load("resources/bqueen.png"),
        'k': pygame.image.load("resources/bking.png")
    }
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_image = piece_images[piece.symbol()]
            screen.blit(piece_image, pygame.Rect((square % 8) * 60, (7 - square // 8) * 60, 60, 60))

# Function to handle user input
def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def quit_game():
    print("Quitting the game...")
    pygame.quit()
    stockfish.terminate()
    quit()

# Initialize chess engine
stockfish = subprocess.Popen(
    STOCKFISHPATH,  # Path to Stockfish executable
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

# Main loop
def main():
    board = chess.Board()
    running = True
    while running:
        draw_board()
        draw_pieces(board)
        pygame.display.flip()
        
        if board.is_game_over():
            print("Game Over")
            break
        
        if board.turn == chess.WHITE:
            try:
                move = input("Enter your move: ")
                if move.lower() == 'q':
                    quit_game()
                board.push_san(move)
                print(chessGame.stockfish(board, 0))  
            except ValueError:
                print("Invalid move. Please try again.")
            except chess.MoveError:
                print("Illegal move. Please try again.")
        else:
            print('AI is thinking')
            best_move = chessPlay.get_ai_move(board, 2)
            board.push(best_move)
            print(chessGame.stockfish(board, 0))            

        running = not handle_input()

    stockfish.terminate()
    pygame.quit()

if __name__ == "__main__":
    main()

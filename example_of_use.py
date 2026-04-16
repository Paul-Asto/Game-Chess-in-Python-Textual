

# Crear la clase ChessGame con el Builder, esta clase   maneja la logica del juego de ajedrez
from src.core.game import ChessGame
from src.builder import BuilderChess

game: ChessGame = BuilderChess.build_game()

# Inicializa el juego
game.init()


# Visualizacion de FEN
print(game.notation_forsyth_edwards)     #  rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

# Verifiar si el juego aun no termina
state: bool = game.in_running_game # True or False

# Visualizacion de datos con Rich
from src.term.term_view_components import get_view_term_board
from rich.console import Console

console = Console()

# Imprimir el tablero
view_board = get_view_term_board(game.board)
console.print(view_board)

'''

____________________________
|          Board            |
|___________________________|

   A   B   C   D   E  F   G   H  

8  ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖   8
7  ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙   7
6  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ   6
5  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ   5
4  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ   4
3  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ  Ｘ   3
2  ♙  ♙  ♙  ♙  ♙  ♙  ♙  ♙   2
1  ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖   1

   A   B   C   D   E  F   G   H  
'''


# Realiza un movimiento ejemplo: (d2d4, f7e6, g3f2, h8h6)
# Para promocion de peon se añade al final del movimiento el caracter de la ficha al cual sera promovido (q, r, b, n)
from src.core.protocol_uci import FormatUCI

str_mov = "d2d4"
mov_uci = FormatUCI(str_mov)

game.make_mov(mov_uci)

# Visualiza los cambios imprimiendo otra ves el tablero

console.print(view_board)

# reinicia el juego 
game.restart_game()


# ejemplo de obtencion de un movimiento de stockfish
from src.utilities_stockfish import get_mov_uci_chess_bot
fen: str = game.notation_forsyth_edwards # "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"   FEN de una posición de ajedrez
#mejor_jugada = get_mov_uci_chess_bot(fen_inicial)

uci: str = get_mov_uci_chess_bot(fen)
print(uci) # Obtiene un best move para usarlo como un movimiento enemigo

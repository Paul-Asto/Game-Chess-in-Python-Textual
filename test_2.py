from src.term.term_view_components import get_view_term_board
from rich.console import Console
from src.utilities_stockfish import get_mov_uci_chess_bot
from src.core.protocol_uci import FormatUCI
from src.builder import BuilderChess

game = BuilderChess.build_game()
game.init()
counter = 0
console = Console() 
list_fen: list[str] = []

while True: 
    
    str_fen = get_mov_uci_chess_bot(game.notation_forsyth_edwards)
    list_fen.append(str_fen)
    
    try:
        console.print(f"Fen: {game.notation_forsyth_edwards}  Mov_Uci: {str_fen}")
        game.make_mov(FormatUCI(str_fen))
        
        movs_deads = game.board.get_movs_of_dead_pieces()
        
        if len(movs_deads) != 0:
            console.print()
            for key, mov in movs_deads.items():
                text = f"La ficha en la posicion {key}: tiene los siguientes objetivos: {[mov]}"
                console.print(text)
            console.print()

        
    
    except Exception as e:
        console.print("\nUltimo movimiento realizado")
        console.print(f"In running game: {game.in_running_game}")
        console.print("FENS = ", list_fen)
        console.print(f"Blancos en hackemate: {game.army_white.in_hacke_mate}")
        console.print([(coord.value, ob) for _, piece in game.army_white.pieces for coord, ob in piece.get_coords_objetive()])
        console.print(f"Negros en hackemate: {game.army_black.in_hacke_mate}")
        console.print([(coord.value, ob) for _, piece in game.army_black.pieces for coord, ob in piece.get_coords_objetive()])
        console.print(get_view_term_board(game.board))
        console.print(str_fen)
        console.print(e.args)

        game.restart_game()
        list_fen.clear()
        break
        
    
    if not game.in_running_game:
        counter += 1
        console.print("\nJuego terminado correctamente")
        console.print(f"Resultado: {"Gano blanco" if game.army_black.in_hacke_mate else "Gano negro" if game.army_white.in_hacke_mate else "Resultado empate"}")
        console.print(game.notation_forsyth_edwards)
        console.print()
        
        game.restart_game()


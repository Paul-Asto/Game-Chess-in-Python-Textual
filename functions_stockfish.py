
import subprocess
from coord import Coord

RUTA_STOCKFISH = "stockfish/stockfish-windows-x86-64.exe"

def get_mov_uci_chess_bot(fen: str) -> str:
    # Iniciar el proceso de Stockfish
    stockfish = subprocess.Popen([RUTA_STOCKFISH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Enviar el comando para iniciar el motor en modo UCI
    stockfish.stdin.write("uci\n")
    stockfish.stdin.flush()

    # Establecer el FEN actual del tablero
    stockfish.stdin.write(f"position fen {fen}\n")
    stockfish.stdin.flush()

    # Pedir la mejor jugada
    stockfish.stdin.write("go movetime 500\n")  
    stockfish.stdin.flush()

    # Leer la respuesta de Stockfish
    response: str

    while True:
        line = stockfish.stdout.readline()
        
        if line.startswith("bestmove"):
            response = line
            break

    bestmove_uci: str = response.split()[1]

    # Cerrar el proceso de Stockfish
    stockfish.stdin.write("quit\n")
    stockfish.stdin.flush()
    stockfish.stdout.close()
    stockfish.stdin.close()
    
    # Retornar la mejor jugada
    return bestmove_uci


index_chess_x: dict[str, int] = { 
    "a": 0,
    "b": 1,
    "c": 2, 
    "d": 3, 
    "e": 4, 
    "f": 5, 
    "g": 6, 
    "h": 7 
}

index_chess_y: dict[str, str] = {
    "8": 0,
    "7": 1,
    "6": 2,
    "5": 3,
    "4": 4,
    "3": 5,
    "2": 6,
    "1": 7
}


def coords_chess_to_format_uci(uci: str) -> tuple[Coord, Coord]:
    xa, ya, xb, yb = uci

    coord_initial = Coord(index_chess_y[ya], index_chess_x[xa])
    coord_final = Coord(index_chess_y[yb], index_chess_x[xb])

    return coord_initial, coord_final
    

if __name__ == "__main__":
    # Ejemplo de uso
    fen_inicial = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # FEN de una posición inicial estándar
    #mejor_jugada = get_mov_uci_chess_bot(fen_inicial)

    uci = get_mov_uci_chess_bot(fen_inicial)
    coords = coords_chess_to_format_uci(uci)
    print(uci)
    print(coords)
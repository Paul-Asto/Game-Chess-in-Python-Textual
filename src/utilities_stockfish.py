
import subprocess

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


if __name__ == "__main__":
    # Ejemplo de uso
    fen_inicial = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # FEN de una posición inicial estándar
    #mejor_jugada = get_mov_uci_chess_bot(fen_inicial)

    uci = get_mov_uci_chess_bot(fen_inicial)
    print(uci)


from src.builder import BuilderChess
from src.term.chessAppTerm import ChessAppTerm




game = BuilderChess.build_game()

app = ChessAppTerm(game)


if __name__ == "__main__":
    app.run()







from src.core.chessGame import ChessGame
from src.ui.chessAppGui import ChessAppGui
from src.term.chessAppTerm import ChessAppTerm
from src.build_chess_game import build_react_chess_game



game: ChessGame = build_react_chess_game()

app_gui = ChessAppGui(
    game,
)

if __name__ == "__main__":
    app_gui.run()


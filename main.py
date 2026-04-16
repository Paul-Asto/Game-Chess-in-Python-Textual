from src.core.game import ChessGame
from src.ui.chessAppGui import ChessAppGui
from src.builder import BuilderChess


game: ChessGame = BuilderChess.build_game()

app_gui = ChessAppGui(
    game,
    True,
)

if __name__ == "__main__":
    app_gui.run()





from typing import TYPE_CHECKING
from time import sleep

from rich.text import Text
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from src.term.term_view_components import (
    get_view_term_board,
    get_view_term_piece, 
    get_view_term_square,
)
from src.core.format_uci import FormatUCI, UCI_SintaxisError
from src.core.chess_exceptions import IlegalMovChessError
from src.utilities_stockfish import get_mov_uci_chess_bot


if TYPE_CHECKING:
    from src.core.chessGame import ChessGame



class ChessAppTerm:
    
    def __init__(self, game: "ChessGame"):
        self.running: bool = False
        self.game: "ChessGame" = game
        self.console: Console = Console(height= 30)
        
        self.user_turn: str = self.game.army_white.id
        
        self.panel_console: Panel = Panel("", title= "Consola")
        self.panel_info_general: Panel = Panel("", title= "Informacion")
        self.panel_board_chess: Panel = Panel("", title= "Tablero de Ajedrez")
        self.panel_info_objects: Panel = Panel("", title= "Objetos")
        
        self.main_layout = Layout(size= 20)
        
        self.main_layout.split_column(
            Layout(
                name="principal",
                size= 25,
            ),
            Layout(
                name="console",
                size= 4,
            ),
        )
        
        self.main_layout["principal"].split_row(
            Layout(name="info_general"),
            Layout(name="board_chess"),
            Layout(name="info_objects"),
        )
    
    
    @property
    def view_info(self) -> Text:
        pass
    
    
    def run(self):
        self.running = True
        self.game.init()
        
        while self.running:
            self.update_view()
            self.console.print(self.main_layout)
            
            if not self.game.in_running_game:
                break
            
            if self.game.is_equals_turn(self.user_turn):
                self.user_action()
            else:
                self.computer_action()
            
            self.console.clear()
    
    
    def user_action(self):
        user_input: str = self.console.input("/: ")
        
        try:
            uci_input: FormatUCI = FormatUCI(user_input)
            self.game.make_mov(uci_input)
        
        except UCI_SintaxisError as e:
            self.panel_console.renderable = Text(e.args[0])
        
        except IlegalMovChessError as e:
            self.panel_console.renderable = Text(e.args[0])
        
        else:
            self.panel_console.renderable = "Movimiento realizado correctamente"
    
    
    def computer_action(self):
        sleep(0.7)
        
        computer_input: str = get_mov_uci_chess_bot(self.game.notation_forsyth_edwards)
        uci_input: FormatUCI = FormatUCI(computer_input)
        self.game.make_mov(uci_input)
    
    
    def update_view(self):
        self.panel_board_chess.renderable = get_view_term_board(self.game.board)
        self.panel_info_objects.renderable = get_view_term_square(self.game.board.content[2][0])
        
        
        self.main_layout["info_general"].update(self.panel_info_general)
        self.main_layout["console"].update(self.panel_console)
        self.main_layout["board_chess"].update(self.panel_board_chess)
        self.main_layout["info_objects"].update(self.panel_info_objects)

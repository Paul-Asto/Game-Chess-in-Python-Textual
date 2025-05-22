from textual.app import App, on
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button

from src.core.chess_constant import \
    BLOCK_BLACK,\
    BLOCK_WHITE,\
    CHESS_BOARD_SIZE_X,\
    CHESS_BOARD_SIZE_Y

from src.term.term_view_components import get_view_term_board
from src.core.coordinate import Coord
from src.ui.widgets import GroupBlock, ReactBlock, ViewCemetery, GroupPromotionBlock

from typing import TYPE_CHECKING, Generator

if TYPE_CHECKING:
    from src.core.chessGame import ChessGame

import asyncio
from src.utilities_stockfish import get_mov_uci_chess_bot
from src.core.format_uci import FormatUCI


def secuence_class_widget(): 
    x = 0; y = 0
    while True:
        if y % 8  == 0: 
            x += 1

        yield BLOCK_BLACK if x % 2 == 0 else BLOCK_WHITE
        x += 1; y += 1

generator_class_widget = secuence_class_widget()


def secuence_coord_widget() -> Generator[Coord, None, None]:
    for y in range(CHESS_BOARD_SIZE_Y):
        for x in range( CHESS_BOARD_SIZE_X):
            yield Coord(y, x)

generator_coord_widget: Generator[Coord, None, None] = secuence_coord_widget()


class ChessAppGui(App):
    CSS_PATH = "style.tcss"

    def __init__(self, chess_game: "ChessGame", in_vs_ia: bool = False) -> None:
        super().__init__()

        self.chess_game: "ChessGame" = chess_game
        self.id_player_self: str = self.chess_game.army_white.id
        self.in_vs_ia: bool = in_vs_ia


    def compose(self) -> Generator[Widget, None, None]:
        with Horizontal():
            with Widget(classes= "info"):
                self.info_piece = Static(classes= "content_data")
                yield self.info_piece

            with Vertical(classes= "principal"):

                with Vertical():
                    with Widget(classes= "content"):
                        self.turno = Static()
                        yield self.turno

                    with Widget(classes= "content"):
                        self.state_hacke = Static()
                        yield self.state_hacke

                self.promotion_group_white = GroupPromotionBlock("promotion_white")
                yield self.promotion_group_white

                with Horizontal(classes= "principal"):
                    self.killFichasAzules = ViewCemetery(classes= "azules")
                    yield self.killFichasAzules

                    self.tablero = GroupBlock(
                        children = [
                            (next(generator_coord_widget), ReactBlock(classes = next(generator_class_widget)))
                            for _ in range(CHESS_BOARD_SIZE_Y * CHESS_BOARD_SIZE_X)
                        ]
                    )

                    yield self.tablero
    
                    self.killFichasRojas = ViewCemetery(classes= "rojas")
                    yield self.killFichasRojas
                
                self.promotion_group_black = GroupPromotionBlock("promotion_black")
                yield self.promotion_group_black

                with Widget(classes= "content"):
                    yield Button("REINICIAR", id= "btn-reiniciar")
                
                with Widget(classes= "content"):
                    yield Button("SALIR", id= "btn-salir")
            
            with Widget(classes= "info"):
                self.info_board = Static("", classes= "content_data")
                yield self.info_board


    def on_mount(self) -> None:
        self.chess_game.init()

        # Conectar los observers con los observeds
        for coord, block in self.tablero.dict_blocks.items():
            block.observed = self.chess_game.get_square(coord)

        self.killFichasAzules.observed = self.chess_game.army_white
        self.killFichasRojas.observed = self.chess_game.army_black

        self.update_view()

        #asyncio.create_task(self.auto_game())

    # test
    async def auto_game(self) -> None:
        while self.chess_game.in_running_game:
            usi_str = get_mov_uci_chess_bot(self.chess_game.notation_forsyth_edwards)
            format_uci = FormatUCI(usi_str)
            coord_start, coord_end = format_uci.coords

            block = self.tablero.dict_blocks[coord_start]
            self.tablero.update_block_selected(block)
            await asyncio.sleep(0.6)

            self.tablero.accion_game()

            block = self.tablero.dict_blocks[coord_end]
            self.tablero.update_block_selected(block)
            await asyncio.sleep(0.6)

            self.tablero.accion_game()

            await asyncio.sleep(0.6)

        self.turno.update(f"El juego acabo, el equipo ganador es {self.chess_game.army_in_turn.id}")

        
    def update_view(self):
        self.info_board.update(get_view_term_board(self.chess_game.board))
        self.update_view_turno()


        text: str = "_________"
        if self.chess_game.army_in_turn.in_hacke:
            text = "IN HACKE"

        if self.chess_game.army_in_turn.in_hacke_mate:
            text = "IN HACKE MATE"

        self.state_hacke.update(text)


    @on(Button.Pressed, "#btn-reiniciar")
    def restart_app(self):
        self.chess_game.restart_game()
        self.update_view()
        self.info_piece.update("")


        
        
    @on(Button.Pressed, "#btn-salir")
    def exit_app(self):
        self.exit()


    def update_view_turno(self):
        army_white = self.chess_game.army_white
        army_in_turn = self.chess_game.army_in_turn
        
        if army_in_turn == army_white:
            turno = "azules" 
            self.turno.add_class("turno-azul") 
            self.turno.remove_class("turno-rojo")      

        else:
            turno = "rojos"
            self.turno.add_class("turno-rojo")
            self.turno.remove_class("turno-azul") 
        
        self.turno.update(f"Turno de los {turno}")

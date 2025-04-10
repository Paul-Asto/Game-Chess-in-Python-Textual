from textual.app import App, on
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button

from src.chess_constant import \
    BLOCK_BLACK,\
    BLOCK_WHITE,\
    CHESS_BOARD_SIZE_X,\
    CHESS_BOARD_SIZE_Y,\
    ID_ARMY_BLACK,\
    ID_ARMY_WHITE

from src.observer_interface import Observer
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.types import Generic_Square
    from src.chessGame import ChessGame
    from src.core.piece import PieceChess


from src.coordinate import Coord
from src.utilities_stockfish import get_mov_uci_chess_bot, coords_chess_to_format_uci




def secuence_class_widget():
    x = 0; y = 0
    while True:
        if y % 8  == 0: 
            x += 1

        yield BLOCK_BLACK if x % 2 == 0 else BLOCK_WHITE
        x += 1; y += 1

generator_class_widget = secuence_class_widget()


def secuence_coord_widget():
    for y in range(CHESS_BOARD_SIZE_Y):
        for x in range( CHESS_BOARD_SIZE_X):
            yield Coord(y, x)

generator_coord_widget = secuence_coord_widget()



class Block(Widget, Observer["Generic_Square"]):
    app: "ChessAppGui"

    def __init__(self, classes: str) -> None:
        super().__init__(classes=classes)
        
        self.view: Static = Static()   
        self._add_child(self.view) 

    # Event Click
    def on_click(self) -> None:
        self.app.chess_game.set_selected_ficha(self.observed.ficha)
        self.app.update_view_piece()

    # oberver update
    def react_changes(self):
        ficha: "PieceChess" = self.observed.ficha
        
        self.view.set_classes(ficha.clase)
        self.view.update(ficha.char)



class GroupBlocks(Vertical):
    app: "ChessAppGui"

    def __init__(self, children: list[tuple[Coord, Block]]) -> None:
        super().__init__()

        self.coords_ultimate_select: list[Coord] = []
        self.dict_blocks: dict[Coord, Block] = {}

        for coord, block in children:
            self.dict_blocks[coord] = block
            self._add_child(block)

    # funcions coords ultimate selected
    def add_ultimate_coord_selected(self, *coords: Coord) -> None:
        for coord in coords:
            self.addRegisterBlock([(coord, "moved")])

            self.coords_ultimate_select.append(coord)


    def deleted_parcial_ultimate_coord_selected(self) -> None:
        if len(self.coords_ultimate_select) > 2:
            coord_1 = self.coords_ultimate_select.pop(0)
            coord_2 = self.coords_ultimate_select.pop(0)

            self.clearRegisterBlock([(coord_1, "moved")])
            self.clearRegisterBlock([(coord_2, "moved")])
    

    def deleted_ultimate_ultimate_coord_selected(self) -> None:
        coord = self.coords_ultimate_select.pop()
        self.clearRegisterBlock([(coord, "moved")])

    
    # Funcions RegisterBlock
    def addRegisterBlock(self, list_data: list[tuple[Coord, str]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].add_class(key) 


    def clearRegisterBlock(self, list_data: list[tuple[Coord, str]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].remove_class(key) 


    async def on_click(self) -> None:
        await self.app.chess_game.accion_game(self)

        if self.app.chess_game.turn != ID_ARMY_BLACK:  
            return 

        self.app.update_view_board()
        await asyncio.sleep(0.3)
        
        mov_uci = get_mov_uci_chess_bot(self.app.chess_game.notation_forsyth_edwards)
        coord_initial, coord_final = coords_chess_to_format_uci(mov_uci)

        self.dict_blocks[coord_initial].on_click()
        await self.app.chess_game.accion_game(self)

        await asyncio.sleep(0.6)

        self.dict_blocks[coord_final].on_click()
        await self.app.chess_game.accion_game(self)

        self.app.update_view_board()

        await asyncio.sleep(0.3)



class ChessAppGui(App):
    CSS_PATH = "style.tcss"

    def __init__(self, chess_game: "ChessGame"):
        super().__init__()

        self.chess_game: "ChessGame" = chess_game

    def compose(self):
        with Horizontal():
            with Widget(classes= "info"):
                self.info_piece = Static(classes= "content_data")
                yield self.info_piece

            with Vertical(classes= "principal"):
                with Widget(classes= "content"):
                    yield Static("AJEDREZ vs IA")

                with Widget(classes= "content"):
                    self.turno = Static("Turno de los azules", classes= "turno-azul")
                    yield self.turno

                with Horizontal(classes= "principal"):
                    self.killFichasAzules = Widget(classes= "fichas azules")
                    yield self.killFichasAzules

                    self.tablero = GroupBlocks(
                        children = [
                            (next(generator_coord_widget), Block(classes = next(generator_class_widget)))
                            for _ in range(CHESS_BOARD_SIZE_Y * CHESS_BOARD_SIZE_X)
                        ]
                    )

                    yield self.tablero

                    self.killFichasRojas = Widget(classes= "fichas rojas")
                    yield self.killFichasRojas

                with Widget(classes= "content"):
                    yield Button("REINICIAR", id= "btn-reiniciar")

                with Widget(classes= "content"):
                    yield Button("SALIR", id= "btn-salir")
            
            with Widget(classes= "info"):
                self.info_board = Static(self.chess_game.board.view, classes= "content_data")
                yield self.info_board


    def on_mount(self):
        # Conectar los observers con los observeds
        for coord, block in self.tablero.dict_blocks.items():
            block.observed = self.chess_game.get_square(coord)

        self.chess_game.init()

        

    @on(Button.Pressed, "#btn-reiniciar")
    def restart_app(self):
        if isinstance(self.chess_game.selected_piece, PieceChess):
            self.tablero.clearRegisterBlock(self.chess_game.selected_piece.get_coords_objetive())

        self.chess_game.restart_game()

        self.update_view_turno(self.chess_game.turn)
        self.clear_view_kill()

        
    @on(Button.Pressed, "#btn-salir")
    def exit_app(self):
        self.exit()


    def update_view_turno(self, turno: str):
        turno:str
        
        if turno == ID_ARMY_WHITE:
            turno = "azules" 
            self.turno.add_class("turno-azul") 
            self.turno.remove_class("turno-rojo")      

        else:
            turno = "rojos"
            self.turno.add_class("turno-rojo")
            self.turno.remove_class("turno-azul") 
        
        self.turno.update(f"Turno de los {turno}")


    def save_view_kill(self, ficha: PieceChess):
        if ficha.clase == ID_ARMY_BLACK:
            self.killFichasRojas.mount(Static(ficha.char))
    
        else:
            self.killFichasAzules.mount(Static(ficha.char))
    

    def clear_view_kill(self):
        self.killFichasAzules.remove_children(Static)
        self.killFichasRojas.remove_children(Static)

    def update_view_board(self):
        self.info_board.update(self.chess_game.board.view)

    def update_view_piece(self):
        self.info_piece.update(self.chess_game.selected_piece.view)
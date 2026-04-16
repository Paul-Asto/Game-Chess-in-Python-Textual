import asyncio
from typing import TYPE_CHECKING, Generator, Optional

from rich.text import Text
from textual.app import App
from textual._on import on
from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Button

from src.term.term_view_components import get_view_term_board, get_view_term_square, get_view_term_piece
from src.utilities_stockfish import get_mov_uci_chess_bot
from src.core.types import PromotionPiece, IdPiece, ObjetiveChess, ArmyClass
from src.core.protocol_uci import FormatUCI
from src.core.coordinate import Coord

from src.ui.widgets import GroupBlock, Block, ViewCemetery, GroupPromotionBlock
from src.ui.events import EventClickedBlock, EventClickedPromotionBlock

if TYPE_CHECKING:
    from src.core.game import ChessGame
    from src.core.square import Square
    from src.core.types import PromotionPiece
    from src.ui.widgets import GroupPromotionBlock


BLOCK_WHITE = "white"
BLOCK_BLACK = "black"

CHESS_BOARD_SIZE_X = 8
CHESS_BOARD_SIZE_Y = 8


def secuence_class_widget() -> Generator[str, None, None]: 
    x = 0; y = 0
    while True:
        if y % 8  == 0: 
            x += 1
        
        yield BLOCK_BLACK if x % 2 == 0 else BLOCK_WHITE
        x += 1; y += 1

generator_class_widget: Generator[str, None, None] = secuence_class_widget()

def secuence_coord_widget() -> Generator[Coord, None, None]:
    for y in range(CHESS_BOARD_SIZE_Y):
        for x in range( CHESS_BOARD_SIZE_X):
            yield Coord(y, x)

generator_coord_widget: Generator[Coord, None, None] = secuence_coord_widget()



class ChessAppGui(App[None]):
    CSS_PATH = "style.tcss"
    
    def __init__(self, chess_game: "ChessGame", in_vs_ia: bool = False) -> None:
        super().__init__()
        
        self.chess_game: "ChessGame" = chess_game
        self.id_player_self: str = self.chess_game.army_white.clase
        self.in_vs_ia: bool = in_vs_ia
    
    
    def compose(self) -> Generator[Widget, None, None]:
        self.info_piece = Static(classes= "content_data")
        self.info_board = Static("", classes= "content_data")
        
        self.turn_view = Static()
        self.state_hacke = Static()
        
        self.promotion_group_white = GroupPromotionBlock("promotion_white")
        self.promotion_group_black = GroupPromotionBlock("promotion_black")
        self.view_kill_pieces_blues = ViewCemetery(classes= "azules")
        self.view_kill_pieces_reds = ViewCemetery(classes= "rojas")
        
        self.view_board = GroupBlock(
            children = [
                (coord:= next(generator_coord_widget), Block(coord= coord, classes = next(generator_class_widget)))
                for _ in range(CHESS_BOARD_SIZE_Y * CHESS_BOARD_SIZE_X)
            ]
        )
        
        with Horizontal():
            with Widget(classes= "info"):
                yield self.info_piece
            
            with Vertical(classes= "principal"):
                with Vertical():
                    with Widget(classes= "content"):
                        yield self.turn_view
                    
                    with Widget(classes= "content"):
                        yield self.state_hacke
                
                yield self.promotion_group_white
                
                with Horizontal(classes= "principal"):
                    yield self.view_kill_pieces_blues
                    
                    yield self.view_board
                    
                    yield self.view_kill_pieces_reds
                
                yield self.promotion_group_black
            
            
            with Widget(classes= "info"):
                yield self.info_board
                
                with Widget(classes= "content"):
                    yield Button("--")
                
                with Widget(classes= "content"):
                    yield Button("REINICIAR", id= "btn-reiniciar")
                
                with Widget(classes= "content"):
                    yield Button("SALIR", id= "btn-salir")
    

    def on_mount(self) -> None:
        self.chess_game.init()
        self.update_view()
        
        #asyncio.create_task(self.auto_game())
    
    
    async def auto_game(self) -> None:
        while self.chess_game.in_running_game:
            usi_str: str = get_mov_uci_chess_bot(self.chess_game.notation_forsyth_edwards)
            format_uci = FormatUCI(usi_str)
            coord_start, coord_end = format_uci.coords
            
            block: Block = self.view_board.dict_blocks[coord_start]
            self.view_board.update_block_selected(block)
            await asyncio.sleep(0.1)
            
            self.accion_game()
            self.update_view()
            
            block: Block = self.view_board.dict_blocks[coord_end]
            self.view_board.update_block_selected(block)
            await asyncio.sleep(0.1)
            
            self.accion_game()
            self.update_view()
            
        
        self.turn_view.update(f"El juego acabo, el equipo ganador es {self.chess_game.army_not_in_turn.clase}")
    
    
    def update_view(self) -> None:
        #info board update
        self.info_board.update(get_view_term_board(self.chess_game.board))
        
        # info piece update
        self.info_piece.update("")
        
        if  not (block:= self.view_board.selected_block) is None:
            square = self.chess_game.get_safe_square(block.coord)
            view: Text = get_view_term_square(square)
            if not square.piece is None:
                view.append(get_view_term_piece(square.piece))
            
            self.info_piece.update(view)
        
        # View turn Update
        army_in_turn = self.chess_game.army_in_turn
        
        self.turn_view.set_classes(
            "turno-azul" if army_in_turn == self.chess_game.army_white else "turno-rojo"
        )
        self.turn_view.update(
            f"Turno de los {"azules" if army_in_turn == self.chess_game.army_white else "rojos"}"
        )
        
        # view state hacke update
        self.state_hacke.update(
            "IN HACKE MATE"\
            if self.chess_game.army_in_turn.in_hacke_mate else\
            "IN HACKE" \
            if self.chess_game.army_in_turn.in_hacke else\
            "_________"
        )
        
        # view kill pieces update
        self.view_kill_pieces_blues.update_view(self.chess_game.army_white.pieces_in_cementery)
        self.view_kill_pieces_reds.update_view(self.chess_game.army_black.pieces_in_cementery)
        
        # view board update
        for coord, block in self.view_board.dict_blocks.items():
            square: Optional["Square"] = self.chess_game.get_square(coord)
            block.update_view(square.piece if not square is None else None)
    
    
    @on(Button.Pressed, "#btn-reiniciar")
    def restart_app(self) -> None:
        self.chess_game.restart_game()
        self.update_view()
    
    
    @on(Button.Pressed, "#btn-salir")
    def exit_app(self) -> None:
        self.exit()
    
    
    def accion_game(self) -> None:
        promotion_piece: Optional[PromotionPiece] = None
        
        previous_square: Optional["Square"] = \
            self.chess_game.get_safe_square(self.view_board.previous_block.coord) \
            if not self.view_board.previous_block is None else None
        
        selected_square: Optional["Square"] = \
            self.chess_game.get_safe_square(self.view_board.selected_block.coord) \
            if not self.view_board.selected_block is None else None
        
        # Condicion de desactivacion de promocion de peon
        if self.view_board.promoting:
            promotion_piece = self.view_board.id_promotion
            self.view_board.promoting = False
        
        else:
            # Condicion de limpieza de decoracion de objetivos anteriores
            if  not previous_square is None and not previous_square.piece is None:          
                self.view_board.clear_decoration_block(previous_square.get_coords_objetive())
                self.view_board.clear_block_selected(previous_square.coord)
            
            # Condicion para decoracion de objetivos
            if  not self.view_board.selecting:
                if  not selected_square is None and\
                    not selected_square.piece is None and\
                    self.chess_game.is_equals_turn(selected_square.piece.clase):
                    
                    self.view_board.add_decoration_block(selected_square.piece.get_coords_objetive())
                    self.view_board.decorate_block_selected(selected_square.coord)
                    self.view_board.selecting = True
                return
            
            if  selected_square is None or\
                previous_square is None:
                return
            
            # condicion de registro de blockes aliados
            if  not selected_square.piece is None and\
                self.chess_game.is_equals_turn(selected_square.piece.clase): 
                
                # En caso la pieza previa y la pieza seleccionada sean diferentes y sean del mismo equipo, se añade los registros
                if  previous_square.piece != selected_square.piece:
                    self.view_board.add_decoration_block(selected_square.get_coords_objetive())
                    self.view_board.decorate_block_selected(selected_square.coord)
                    self.view_board.selecting = True
                    
                # En caso las piezas sean iguales, no se muestran los registros y vuelve al estado de no seleccion
                else:
                    self.view_board.selecting = False
                return
            
            # Condicion de manejo activacion de posible promocion de peon
            if  not previous_square.piece is None and\
                previous_square.piece.id == IdPiece.PAWN and \
                selected_square.coord.y == previous_square.piece.data_pawn.index_column_meta and \
                (previous_square.piece.coord_is_objetive(selected_square.coord, ObjetiveChess.EMPTY) or\
                previous_square.piece.coord_is_objetive(selected_square.coord, ObjetiveChess.ENEMY)):
                
                self.view_board.promoting = True
                army_class: str = previous_square.piece.clase
                
                if army_class == ArmyClass.WHITE.value:
                    self.promotion_group_white.visible = True
                
                elif army_class == ArmyClass.BLACK.value:
                    self.promotion_group_black.visible = True
                return
        
        if  selected_square is None or\
            previous_square is None:
            return
        
        # Intento de ejecucion del movimiento
        format_uci: FormatUCI = FormatUCI.build_to_coords(
            previous_square.coord,
            selected_square.coord, 
            promotion_piece
        )
        
        try:
            self.chess_game.make_mov(format_uci)
        
        except Exception :
            pass
        
        self.view_board.selecting = False
    
    
    async def on_event_clicked_block(self, event: EventClickedBlock) -> None:
        if self.in_vs_ia and not self.chess_game.is_equals_turn(self.id_player_self):
            return
        
        self.view_board.update_block_selected(block=event.block)
        
        if self.view_board.promoting:
            self.view_board.promoting = False
            
            self.promotion_group_white.visible = False
            self.promotion_group_black.visible = False
        
        self.accion_game()
        self.update_view()
        
        if not self.in_vs_ia or self.chess_game.is_equals_turn(self.id_player_self):
            return
        
        await asyncio.sleep(0.3)
        
        mov_uci: str = get_mov_uci_chess_bot(self.chess_game.notation_forsyth_edwards)
        format_uci = FormatUCI(mov_uci)
        coord_initial, coord_final = format_uci.coords
        
        self.view_board.update_block_selected(self.view_board.dict_blocks[coord_initial])
        self.accion_game()
        self.update_view()
        
        await asyncio.sleep(0.6)
        
        self.view_board.update_block_selected(self.view_board.dict_blocks[coord_final])
        self.accion_game()
        self.update_view()
        
        await asyncio.sleep(0.3)
        
        # Manejo de promocion de Peon
        if not format_uci.is_promotion or  self.view_board.previous_block is None:
            return
        
        square: "Square" = self.chess_game.get_safe_square(self.view_board.previous_block.coord)
        
        if square.piece is None:
            return
        
        self.view_board.id_promotion = format_uci.promotion_id
        army_class: str = square.piece.clase
        
        if army_class == ArmyClass.WHITE.value:
            self.promotion_group_white.visible = True
        
        elif army_class == ArmyClass.BLACK.value:
            self.promotion_group_black.visible = True
        
        await asyncio.sleep(0.3)
        
        self.accion_game()
        self.update_view()
        self.view_board.id_promotion = None
        
        if army_class == ArmyClass.WHITE.value:
            self.promotion_group_white.visible = False
        
        elif army_class == ArmyClass.BLACK.value:
            self.promotion_group_black.visible = False
    
    
    def on_event_clicked_promotion_block(self, event: EventClickedPromotionBlock) -> None:
        id_promotion: "PromotionPiece" = event.promotion_id
        group: "GroupPromotionBlock" = event.group
        
        self.view_board.id_promotion = id_promotion
        group.visible = False
        self.accion_game()
        self.update_view()
        self.view_board.id_promotion = None

import asyncio
from typing import TYPE_CHECKING
from rich.text import Text

from src.core.types_chess import PromotioPiece
from src.ui.observer_interface import Observer
from src.core.chess_exceptions import IlegalMovChessError
from src.core.format_uci import FormatUCI
from src.utilities_stockfish import get_mov_uci_chess_bot

from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from src.core.chess_constant import ID_ARMY_BLACK, ID_ARMY_WHITE, OBJ_ENEMY, OBJ_EMPTY

from src.term.term_view_components import (
    get_view_term_board,
    get_view_term_piece, 
    get_view_term_square,
)

from src.core.pieces import (
    Peon,
    Torre,
    Alfil,
    Reina,
    Caballo,
)

if TYPE_CHECKING:
    from src.ui.react_component import ReactSquare
    from src.ui.chessAppGui import ChessAppGui
    from src.core.piece import PieceChess
    from src.core.coordinate import Coord
    from src.core.army import Army


class Block(Widget):
    app: "ChessAppGui"

    DEFAULT_CSS = '''
    Block{
        width: 7;
        height: 3;  
        align-vertical: middle; 
    }

    Block Static{
        width: 5;
        height: 1;
        content-align-horizontal: center;
    }
    '''

    def __init__(self, classes: str | None = None, view: str = "") -> None:
        super().__init__(classes=classes)
        
        self.view: Static = Static(view)   
        self._add_child(self.view) 



class ReactBlock(Block, Observer["ReactSquare"]):
    parent: "GroupBlock"

    DEFAULT_CSS = '''
    ReactBlock.blanco {
        background: white;
    }

    ReactBlock.negro{
        background: black;
    }

    ReactBlock.moved{
        background: yellow;
    }

    ReactBlock.enemy{
        background: red;
        border: solid;
    }

    ReactBlock.empty{
        background: green;
        border: solid;
    }

    /*
    Block.invalid{
        background: blue;
        border: solid;
    }
    */
    '''
    
    # Event Click
    def on_click(self) -> None:
        # Actualizacion de vista de informacion de square y piece
        piece: PieceChess = self.observed.piece
        view_info: Text = get_view_term_square(self.observed)

        if piece != None:
            view_info.append(get_view_term_piece(piece))
        
        self.app.info_piece.update(view_info)

        # Actualizacion de bocke seleccionado
        if self.app.in_vs_ia:
            if not self.app.chess_game.is_equals_turn(self.app.id_player_self):
                return

        self.parent.update_block_selected(self)

        if self.parent.promoting:
            self.parent.promoting = False

            self.app.promotion_group_white.visible = False
            self.app.promotion_group_black.visible = False

    
    # oberver update
    def react_changes(self) -> None:
        ficha: PieceChess = self.observed.piece
        
        if ficha == None:
            self.view.update("")
            return
        
        self.view.set_classes(ficha.clase)
        self.view.update(ficha.char_view)



class PromotionBlock(Block):

    DEFAULT_CSS = '''
    PromotionBlock{
        background: black;
    }
    '''

    def __init__(self, piece_promotion: "PieceChess") -> None:
        super().__init__(classes = None)

        self.piece_promotion:" PieceChess" = piece_promotion
        self.view.update(self.piece_promotion.char_view)

    
    async def on_click(self) -> None:
        if not self.parent.visible:
            return
        
        self.app.tablero.char_piece_promoting = PromotioPiece[self.piece_promotion.char_fen.upper()]
        self.parent.visible = False
        self.app.tablero.accion_game()



class GroupBlock(Vertical):
    app: "ChessAppGui"
    
    def __init__(self, children: list[tuple["Coord", ReactBlock]]) -> None:
        super().__init__()
        
        #self.coords_ultimate_select: list["Coord"] = []
        self.dict_blocks: dict["Coord", ReactBlock] = {}
        
        self.previous_block: ReactBlock = None
        self.selected_block: ReactBlock = None
        
        self.selecting: bool = False

        self.promoting: bool = False
        self.char_piece_promoting: PromotioPiece = None
        
        for coord, block in children:
            self.dict_blocks[coord] = block
            self._add_child(block)
    
    
    # Funcions RegisterBlock
    def add_decoration_block(self, list_data: list[tuple["Coord", str]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].add_class(key) 
    
    
    def clear_decoration_block(self, list_data: list[tuple["Coord", str]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].remove_class(key) 
    
    
    def update_block_selected(self, block: ReactBlock) -> None:
        self.previous_block = self.selected_block
        self.selected_block = block
    
    
    async def on_click(self) -> None:
        if self.app.in_vs_ia:
            if not self.app.chess_game.is_equals_turn(self.app.id_player_self):
                return
        
        self.accion_game()

        if not self.app.in_vs_ia:
            return
        
        if self.app.chess_game.is_equals_turn(self.app.id_player_self):  
            return 
        
        await asyncio.sleep(0.3)
        
        mov_uci: str = get_mov_uci_chess_bot(self.app.chess_game.notation_forsyth_edwards)
        format_uci = FormatUCI(mov_uci)
        coord_initial, coord_final = format_uci.coords
        
        self.update_block_selected(self.dict_blocks[coord_initial])
        self.accion_game()
        
        await asyncio.sleep(0.6)
        
        self.update_block_selected(self.dict_blocks[coord_final])
        self.accion_game()
        
        await asyncio.sleep(0.3)

        if format_uci.is_promotion:
            self.char_piece_promoting = PromotioPiece[format_uci.char_promotion.upper()]
            army_class: str = self.previous_block.observed.piece.clase

            if army_class == ID_ARMY_WHITE:
                self.app.promotion_group_white.on_click()

            elif army_class == ID_ARMY_BLACK:
                self.app.promotion_group_black.on_click()
    
    
    def accion_game(self) -> None:
        promotion_piece: PromotioPiece = None

        if self.promoting:
            promotion_piece = self.char_piece_promoting
            self.promoting = False
        
        else:

            if self.previous_block != None: # Se limpia las coordenadas objetivos anteriores
                self.clear_decoration_block(self.previous_block.observed.get_coords_objetive())
            
            if not self.selecting:
                piece_obj: PieceChess = self.selected_block.observed.piece
                
                # Si la pieza seleccionada es None, se retorna
                if piece_obj == None:
                    return
                
                # Si la pieza seleccionda es de diferente clase del turno actual, se retorna
                if not self.app.chess_game.is_equals_turn(piece_obj.clase):
                    return
                
                self.add_decoration_block(self.selected_block.observed.get_coords_objetive())
                self.selecting = True
                return
            
            previous_square: "ReactSquare" = self.previous_block.observed
            selected_square: "ReactSquare" = self.selected_block.observed
            
            # condicion de registro de blockes aliados
            if selected_square.piece != None and\
            self.app.chess_game.is_equals_turn(selected_square.piece.clase): 
                
                # En caso la pieza previa y la pieza seleccionada sean diferentes y sean del mismo equipo, se añade los registros
                if previous_square.piece != selected_square.piece:
                    self.add_decoration_block(selected_square.get_coords_objetive())
                # en caso las piezas sean iguales, no se muestran los registros y vuelve al estado de no seleccion
                else:
                    self.selecting = False
                
                return
            
            # Condicion de manejo de posible promocion de peon
            if isinstance(previous_square.piece, Peon) and \
            selected_square.coord.y == previous_square.piece.index_column_meta and \
            (previous_square.piece.coord_is_objetive(selected_square.coord, OBJ_EMPTY) or\
            previous_square.piece.coord_is_objetive(selected_square.coord, OBJ_ENEMY)):
                
                self.promoting = True
                army_class: str = previous_square.piece.clase

                if army_class == ID_ARMY_WHITE:
                    self.app.promotion_group_white.visible = True

                elif army_class == ID_ARMY_BLACK:
                    self.app.promotion_group_black.visible = True
                return
        

        # try mov chess
        format_uci: FormatUCI = FormatUCI.build_to_coords(
            self.previous_block.observed.coord,
            self.selected_block.observed.coord, 
            promotion_piece
        )
        
        try:
            self.app.chess_game.make_mov(format_uci)
        
        except IlegalMovChessError:
            pass
        
        else:
            self.app.update_view()
        
        self.selecting = False
    
    
    
class ViewCemetery(Widget, Observer["Army"]):

    DEFAULT_CSS = '''
    ViewCemetery{
        width: 14;
        height: 24;
        margin-left: 5;
        margin-right: 5;
        layout: grid;
        grid-size: 2 8;
    }
    ViewCemetery {
        background: black;
    }

    ViewCemetery.rojas Block{
        color: red;
    }

    ViewCemetery.azules Block{
        color: blue;
    }
    '''
    
    def react_changes(self) -> None:
        if len(self.observed.pieces_cemetery) == 0:
            self.remove_children(Block)
            return
        
        piece: "PieceChess" = self.observed.pieces_cemetery[-1]
        self.mount(Block(view= piece.char_view))



class GroupPromotionBlock(Horizontal):
    app: "ChessAppGui"

    DEFAULT_CSS = '''
    GroupPromotionBlocks{
    width: 28;
    height: 8;
    layout: grid;
    grid-size: 1 4;    
    }

    GroupPromotionBlock.promotion_black PromotionBlock Static{
        color: red;
    }

    GroupPromotionBlock.promotion_white PromotionBlock Static{
        color: blue
    }
    
    '''

    def __init__(self, classes: str) -> None:
        super().__init__(classes= classes)

        self.visible: bool = False

        self._add_children(
            PromotionBlock(piece_promotion=Torre()),
            PromotionBlock(piece_promotion=Alfil()),
            PromotionBlock(piece_promotion=Reina()),
            PromotionBlock(piece_promotion=Caballo()),
        )


    def on_click(self) -> None:
        if not self.visible:
            return
        
        if self.app.tablero.char_piece_promoting == None:
            return
        
        self.visible = False
        self.app.tablero.accion_game()
        self.app.tablero.char_piece_promoting = None
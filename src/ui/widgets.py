
from typing import TYPE_CHECKING, Optional

from textual.widgets import Static
from textual.containers import Vertical, Horizontal
from textual.widget import Widget

from src.core.types import PromotionPiece, ObjetiveChess
from src.ui.events import EventClickedBlock, EventClickedPromotionBlock

if TYPE_CHECKING:
    from src.core.piece import PieceChess
    from src.core.coordinate import Coord



class Block(Widget):
    
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
    
    Block.white {
        background: white;
    }
    
    Block.black{
        background: black;
    }
    
    Block.moved{
        background: yellow;
    }
    
    Block.enemy{
        background: red;
        border: solid;
    }
    
    Block.empty{
        background: green;
        border: solid;
    }

    Block.select{
        background: yellow;
    }
    
    /*
    Block.invalid{
        background: blue;
        border: solid;
    }
    */
    '''
    
    def __init__(self, coord:Optional[ "Coord"] = None, classes: Optional[str] = None, view: str = "") -> None:
        super().__init__(classes=classes)
        
        self.__coord: Optional["Coord"] = coord
        self.view: Static = Static(view)   
        self._add_child(self.view) 
    
    
    @property
    def coord(self) -> "Coord":
        if self.__coord is None:
            raise Exception("El valor de la coordenada es Nula")
        
        return self.__coord
    
    
    # Event Click
    def on_click(self) -> None:
        if not self.__coord is None:
            self.post_message(EventClickedBlock(self))
    
    
    def update_view(self, piece: Optional["PieceChess"]) -> None:
        self.view.update(piece.char_view if not piece is None else "")
        self.view.set_classes(piece.clase if not piece is None else "")



class PromotionBlock(Widget):
    
    DEFAULT_CSS = '''
    PromotionBlock{
        width: 7;
        height: 3;  
        align-vertical: middle; 
        background: black;
    }
    
    PromotionBlock Static{
        width: 5;
        height: 1;
        content-align-horizontal: center;
    }
    '''
    parent: "GroupPromotionBlock"   #type:ignore
    
    def __init__(self, promotion_id: PromotionPiece) -> None:
        super().__init__(classes = None)
        
        self.promotion_id: PromotionPiece = promotion_id
        self.view: Static = Static(self.promotion_id.char_view)   
        self._add_child(self.view) 
    
    
    async def on_click(self) -> None:
        self.post_message(EventClickedPromotionBlock(self.promotion_id, self.parent))
    
    
    def update_view(self, piece: Optional["PieceChess"]) -> None:
        self.view.update(piece.char_view if not piece is None else "")
        self.view.set_classes(piece.clase if not piece is None else "")



class GroupBlock(Vertical):
    
    def __init__(self, children: list[tuple["Coord", Block]]) -> None:
        super().__init__()
        
        self.dict_blocks: dict["Coord", Block] = {} 
        self.ultimate_coord_mov: Optional["Coord"] = None
        
        self.previous_block: Optional[Block] = None
        self.selected_block: Optional[Block] = None
        
        self.selecting: bool = False
        self.promoting: bool = False
        
        self.id_promotion: PromotionPiece | None = None
        
        for coord, block in children:
            self.dict_blocks[coord] = block
            self._add_child(block)
    
    
    # Funcions RegisterBlock
    def add_decoration_block(self, list_data: list[tuple["Coord", ObjetiveChess]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].add_class(key.value) 
    
    
    def clear_decoration_block(self, list_data: list[tuple["Coord", ObjetiveChess]]) -> None:
        for coord, key in list_data:
            self.dict_blocks[coord].remove_class(key.value) 
    
    
    def update_block_selected(self, block: Block) -> None:
        self.previous_block = self.selected_block
        self.selected_block = block

    def decorate_block_selected(self, coord: "Coord") -> None:
        self.dict_blocks[coord].add_class("select")

    def clear_block_selected(self, coord: "Coord") -> None:
        self.dict_blocks[coord].remove_class("select")

class ViewCemetery(Widget):
    
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
    
    def update_view(self, pieces: list["PieceChess"]) -> None:
        self.remove_children(Block)
        
        for piece in pieces:
            self.mount(Block(view= piece.char_view, classes= piece.clase))



class GroupPromotionBlock(Horizontal):
    
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
            PromotionBlock(promotion_id= PromotionPiece.ROOK),
            PromotionBlock(promotion_id= PromotionPiece.BISHOP),
            PromotionBlock(promotion_id= PromotionPiece.QUEEN),
            PromotionBlock(promotion_id= PromotionPiece.KNIGHT),
        )
    
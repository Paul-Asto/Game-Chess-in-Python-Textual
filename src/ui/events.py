from typing import TYPE_CHECKING
from textual.message import Message

if TYPE_CHECKING:
    from src.ui.widgets import Block
    from src.core.types import PromotionPiece
    from src.ui.widgets import GroupPromotionBlock



class EventClickedBlock(Message):
    
    def __init__(self, block: "Block") -> None:
        super().__init__()
        
        self.block: "Block" = block



class EventClickedPromotionBlock(Message):
    
    def __init__(self, promotion_id: "PromotionPiece" , group: "GroupPromotionBlock") -> None:
        super().__init__()
        
        self.promotion_id: "PromotionPiece" = promotion_id
        self.group : "GroupPromotionBlock" = group
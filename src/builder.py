from typing import Optional

from src.core.types import CharViewPiece, CharFenPiece, EDirectionPawn, ColorPiece, ArmyClass, IdPiece, PromotionPiece
from src.core.data_classes import DataArmy, DataPawn

from src.core.piece import PieceChess
from src.core.board import Board
from src.core.army import Army
from src.core.game import ChessGame
from src.core.coordinate import Coord

from src.core.movs.short_mov import ShortMov
from src.core.movs.long_mov import LongMov
from src.core.movs.king_mov import KingMov, ShortCastlingMov, LongCastlingMov
from src.core.movs.pawn_mov import PawnMovDiagonal, PawnMovPassant, PawnMovFrontal, PawnMovDoubleFrontal



class BuilderChess:
    
    @classmethod
    def build_piece(cls, id: IdPiece , pawn_direction: Optional[EDirectionPawn] = None) -> PieceChess: 
        piece: PieceChess
        
        match(id):
            case IdPiece.KING: piece = cls.build_king()
            case IdPiece.QUEEN: piece = cls.build_queen()
            case IdPiece.ROOK: piece = cls.build_rook()
            case IdPiece.BISHOP: piece = cls.build_bishop()
            case IdPiece.KNIGHT: piece = cls.build_knight()
            case IdPiece.PAWN: 
                if pawn_direction is None:
                    raise Exception("Error build pawn")
                
                piece = cls.build_pawn(pawn_direction)
        
        return piece
    
    
    @classmethod
    def build_promotion_piece(cls, promotion_id: PromotionPiece) -> PieceChess: 
        piece: PieceChess
        
        match(promotion_id):
            case PromotionPiece.QUEEN: piece = cls.build_queen()
            case PromotionPiece.ROOK: piece = cls.build_rook()
            case PromotionPiece.BISHOP: piece = cls.build_bishop()
            case PromotionPiece.KNIGHT: piece = cls.build_knight()
        
        return piece
    
    
    @classmethod
    def build_bishop(cls) -> PieceChess:
        piece = PieceChess(
            id= IdPiece.BISHOP,
            character_view= CharViewPiece.BISHOP,
            character_fen= CharFenPiece.BISHOP
        )
        
        piece.movs = [
            LongMov(piece, (-1, -1)),
            LongMov(piece, (-1, 1)),
            LongMov(piece, (1, -1)),
            LongMov(piece, (1, 1)),
        ]
        
        return piece
    
    
    @classmethod
    def build_knight(cls) -> PieceChess:
        piece = PieceChess(
            id= IdPiece.KNIGHT,
            character_view= CharViewPiece.KNIGHT,
            character_fen= CharFenPiece.KNIGHT
        )
        
        piece.movs = [
            ShortMov(piece, (2, 1)),
            ShortMov(piece, (2, -1)),
            ShortMov(piece, (-1, 2)),
            ShortMov(piece, (1, 2)),
            ShortMov(piece, (-2, -1)),
            ShortMov(piece, (-2, 1)),
            ShortMov(piece, (-1, -2)),
            ShortMov(piece, (1, -2)),
        ]
        
        return piece
    
    
    @classmethod
    def build_rook(cls) -> PieceChess:
        piece = PieceChess(
            id= IdPiece.ROOK,
            character_view= CharViewPiece.ROOK,
            character_fen= CharFenPiece.ROOK
        )
        
        piece.movs = [
            LongMov(piece, (0, 1)),
            LongMov(piece, (0, -1)),
            LongMov(piece, (-1, 0)),
            LongMov(piece, (1, 0)),
        ]
        
        return piece
    
    
    @classmethod
    def build_queen(cls) -> PieceChess:
        piece = PieceChess(
            id= IdPiece.QUEEN,
            character_view= CharViewPiece.QUEEN,
            character_fen= CharFenPiece.QUEEN
        )
        
        piece.movs = [
            LongMov(piece, (0, 1)),
            LongMov(piece, (0, -1)),
            LongMov(piece, (-1, 0)),
            LongMov(piece, (1, 0)),
            LongMov(piece, (-1, -1)),
            LongMov(piece, (-1, 1)),
            LongMov(piece, (1, -1)),
            LongMov(piece, (1, 1)),    
        ]
        
        return piece
    
    
    @classmethod
    def build_king(cls) -> PieceChess:
        piece = PieceChess(
            id= IdPiece.KING,
            character_view= CharViewPiece.KING,
            character_fen= CharFenPiece.KING,
            hacked_restricted= False
        )
        
        piece.movs = [
            KingMov(piece, (0, 1)),
            KingMov(piece, (0, -1)),
            KingMov(piece, (-1, 0)),
            KingMov(piece, (1, 0)),
            KingMov(piece, (-1, -1)),
            KingMov(piece, (-1, 1)),
            KingMov(piece, (1, -1)),
            KingMov(piece, (1, 1)),
            ShortCastlingMov(piece),
            LongCastlingMov(piece),
        ]
        
        return piece
    
    
    @classmethod
    def build_pawn(cls, direction: EDirectionPawn) -> PieceChess:
        direction_int: int = direction.value.direction
        index_meta: int = direction.value.index_goal_column
        
        piece = PieceChess(
            id= IdPiece.PAWN,
            character_view= CharViewPiece.PAWN,
            character_fen= CharFenPiece.PAWN,
        )
        
        double_frontal_mov  = PawnMovDoubleFrontal(piece, (direction_int * 2, 0))
        frontal_mov         = PawnMovFrontal(piece, (direction_int, 0))
        
        diagonal_left_mov   = PawnMovDiagonal(piece, (direction_int, -1))
        diagonal_right_mov  = PawnMovDiagonal(piece, (direction_int, 1))
        
        passant_left_mov    = PawnMovPassant(piece, (0, -1))
        passant_right_mov   = PawnMovPassant(piece, (0, 1))
        
        diagonal_left_mov.mov_off_passant        = passant_left_mov
        passant_left_mov.mov_off_final_position  = diagonal_left_mov
        
        diagonal_right_mov.mov_off_passant       = passant_right_mov
        passant_right_mov.mov_off_final_position = diagonal_right_mov
        
        data_pawn = DataPawn(
            direction= direction_int,
            index_column_meta= index_meta,
            frontal_mov= frontal_mov,
            double_frontal_mov= double_frontal_mov
        )
        
        piece.movs = [
            double_frontal_mov,
            frontal_mov,
            diagonal_left_mov, 
            diagonal_right_mov,
            passant_left_mov,
            passant_right_mov,
        ]
        
        piece.data_pawn = data_pawn
        
        return piece
    
    
    @classmethod
    def build_army_black(cls) -> Army: 
        data_army = DataArmy(
            king= (Coord(0, 4), cls.build_king()),
            pieces= [
                (Coord(1, 0), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 1), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 2), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 3), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 4), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 5), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 6), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(1, 7), cls.build_pawn(EDirectionPawn.DOWN)),
                (Coord(0, 0), cls.build_rook()),
                (Coord(0, 1), cls.build_knight()),
                (Coord(0, 2), cls.build_bishop()),
                (Coord(0, 3), cls.build_queen()),
                (Coord(0, 5), cls.build_bishop()),
                (Coord(0, 6), cls.build_knight()),
                (Coord(0, 7), cls.build_rook()),
            ]
        )
        
        
        return  Army(
            data_army= data_army,
            console_color= ColorPiece.BLACK,
            army_class= ArmyClass.BLACK
        )
    
    
    @classmethod
    def build_army_white(cls) -> Army: 
        data_army = DataArmy(
            king= (Coord(7, 4), cls.build_king()),
            pieces= [
                (Coord(6, 0), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 1), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 2), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 3), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 4), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 5), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 6), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(6, 7), cls.build_pawn(EDirectionPawn.UP)),
                (Coord(7, 0), cls.build_rook()),
                (Coord(7, 1), cls.build_knight()),
                (Coord(7, 2), cls.build_bishop()),
                (Coord(7, 3), cls.build_queen()),
                (Coord(7, 5), cls.build_bishop()),
                (Coord(7, 6), cls.build_knight()),
                (Coord(7, 7), cls.build_rook()),
            ]
        )
        
        return  Army(
            data_army= data_army,
            console_color= ColorPiece.WHITE,
            army_class= ArmyClass.WHITE
        )
    
    
    @classmethod
    def build_game(cls) -> ChessGame:
        board = Board(8, 8)
        
        army_white = cls.build_army_white()
        army_black = cls.build_army_black()
        
        game = ChessGame(
            army_white= army_white,
            army_black= army_black,
            board= board
        )
        
        return game

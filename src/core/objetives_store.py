from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.types import ObjetiveChess
    from src.core.coordinate import Coord
    from src.core.movs.piece_mov import PieceMov



class ObjetivesStore:
    
    def __init__(self) -> None:
        self.__store_data: dict["PieceMov", dict["Coord", "ObjetiveChess"]] = {}
    
    
    def set_movs(self, *movs_piece: "PieceMov") -> None:
        self.__store_data.clear()
        
        for mov in movs_piece:
            self.__store_data[mov] = {}
    
    
    def get_coords_off_mov(self, mov: "PieceMov") -> list["Coord"]:
        return list(self.__store_data[mov].keys())
    
    
    def get_coords(self) -> list["Coord"]:
        return [
            coord
            for data in self.__store_data.values()
            for coord in data.keys()
        ]
    
    
    def get_data_off_mov(self, mov: "PieceMov") -> list[tuple["Coord", "ObjetiveChess"]]:
        return list(self.__store_data[mov].items())
    
    
    def get_data(self) -> list[tuple["Coord", "ObjetiveChess"]]:
        return [
            item
            for data in self.__store_data.values()
            for item in data.items()
        ]
    
    
    def add_coord_off_mov(self, mov: "PieceMov", coord: "Coord", objetive: "ObjetiveChess") -> None:
        self.__store_data[mov][coord] = objetive
    
    
    def clear_store_off_mov(self, mov: "PieceMov") -> None:
        self.__store_data[mov].clear()
    
    
    def coord_in_store(self, coord: "Coord", objetive: "ObjetiveChess") -> bool:
        for mov in self.__store_data.keys():
            if self.coord_in_store_off_mov(mov, coord, objetive):
                return True
            
        data_filtred: list["PieceMov"] = list(filter(
            lambda mov: self.coord_in_store_off_mov(mov, coord, objetive),
            self.__store_data.keys()
        ))
        
        return any(data_filtred)
    
    
    def coord_in_store_off_mov(self, mov: "PieceMov", coord: "Coord", objetive: "ObjetiveChess") -> bool:
        input_data: tuple["Coord", "ObjetiveChess"] = (coord, objetive)
        
        data_filtred: list[tuple["Coord", "ObjetiveChess"]] = list(filter(
            lambda data: data == input_data, 
            self.get_data_off_mov(mov)
        ))
        
        return any(data_filtred)

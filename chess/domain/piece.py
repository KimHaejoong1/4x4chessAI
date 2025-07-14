from abc import ABC, abstractmethod
from typing import List, Tuple
from .position import Position

class Piece(ABC):
    def __init__(self, color: str):
        self.color = color  # 'white' 또는 'black'
        
    @property
    def name(self) -> str:
        return f"{self.color}_{self.__class__.__name__.lower()}"
    
    @abstractmethod
    def get_possible_moves(self, board: List[List[str]], pos: Position) -> List[Position]:
        """현재 위치에서 가능한 모든 이동 위치 반환"""
        pass
    
    def is_opponent_piece(self, board: List[List[str]], pos: Position) -> bool:
        """해당 위치에 상대편 말이 있는지 확인"""
        if board[pos.row][pos.col] == '':
            return False
        return 'white' in board[pos.row][pos.col] if self.color == 'black' else 'black' in board[pos.row][pos.col]
    
    def is_clear_path(self, board: List[List[str]], start: Position, end: Position) -> bool:
        """시작 위치와 끝 위치 사이에 다른 말이 없는지 확인"""
        row_step = 0 if start.row == end.row else (1 if end.row > start.row else -1)
        col_step = 0 if start.col == end.col else (1 if end.col > start.col else -1)

        row, col = start.row + row_step, start.col + col_step

        while (row, col) != (end.row, end.col):
            if board[row][col] != '':
                return False
            row += row_step
            col += col_step

        return True


class Pawn(Piece):
    def get_possible_moves(self, board: List[List[str]], pos: Position) -> List[Position]:
        possible_moves = []
        direction = -1 if self.color == 'white' else 1
        
        # 한 칸 앞으로 이동
        new_row = pos.row + direction
        if 0 <= new_row < 4 and board[new_row][pos.col] == '':
            possible_moves.append(Position(new_row, pos.col))
            
        # 대각선 잡기
        for side_col in [pos.col - 1, pos.col + 1]:
            if 0 <= side_col < 4 and 0 <= new_row < 4:
                if board[new_row][side_col] != '':
                    if self.is_opponent_piece(board, Position(new_row, side_col)):
                        possible_moves.append(Position(new_row, side_col))
                        
        return possible_moves


class Rook(Piece):
    def get_possible_moves(self, board: List[List[str]], pos: Position) -> List[Position]:
        possible_moves = []
        
        # 수평 이동
        for new_col in range(4):
            if new_col != pos.col:
                end = Position(pos.row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        # 수직 이동
        for new_row in range(4):
            if new_row != pos.row:
                end = Position(new_row, pos.col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        return possible_moves


class King(Piece):
    def get_possible_moves(self, board: List[List[str]], pos: Position) -> List[Position]:
        possible_moves = []
        
        # 킹은 모든 방향으로 한 칸만 이동 가능
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # 현재 위치 제외
                    
                new_row, new_col = pos.row + i, pos.col + j
                if 0 <= new_row < 4 and 0 <= new_col < 4:
                    if board[new_row][new_col] == '' or self.is_opponent_piece(board, Position(new_row, new_col)):
                        possible_moves.append(Position(new_row, new_col))
                        
        return possible_moves


class Queen(Piece):
    def get_possible_moves(self, board: List[List[str]], pos: Position) -> List[Position]:
        possible_moves = []
        
        # 수평, 수직 이동 (룩처럼)
        for new_col in range(4):
            if new_col != pos.col:
                end = Position(pos.row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        for new_row in range(4):
            if new_row != pos.row:
                end = Position(new_row, pos.col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
        
        # 대각선 이동 (비숍처럼)
        for i in range(-3, 4):
            if i == 0:
                continue
                
            new_row, new_col = pos.row + i, pos.col + i
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                end = Position(new_row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
            new_row, new_col = pos.row + i, pos.col - i
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                end = Position(new_row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end.row][end.col] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        return possible_moves 
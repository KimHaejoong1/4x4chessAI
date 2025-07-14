from typing import Optional
from ..domain.board import Board
from ..domain.position import Position
from ..domain.piece import Piece

class MoveValidator:
    """이동 유효성 검사"""
    
    def __init__(self, board: Board):
        self.board = board
    
    def is_valid_move(self, from_pos: Position, to_pos: Position, color: str) -> bool:
        """이동이 유효한지 확인"""
        # 1. 기본 이동 규칙 검사
        if not self._is_basic_move_valid(from_pos, to_pos, color):
            return False
        
        # 2. 킹 노출 검사
        if self._would_expose_king(from_pos, to_pos, color):
            return False
        
        return True
    
    def get_legal_moves(self, from_pos: Position, color: str) -> list[Position]:
        """특정 위치에서 가능한 합법적인 이동들 반환"""
        piece = self.board.get_piece(from_pos)
        if not piece or piece.color != color:
            return []
        
        legal_moves = []
        possible_moves = piece.get_possible_moves(self.board.board, from_pos)
        
        for move in possible_moves:
            if self.is_valid_move(from_pos, move, color):
                legal_moves.append(move)
        
        return legal_moves
    
    def _is_basic_move_valid(self, from_pos: Position, to_pos: Position, color: str) -> bool:
        """기본 이동 규칙 검사"""
        piece = self.board.get_piece(from_pos)
        
        # 말이 존재하는지 확인
        if not piece:
            return False
        
        # 올바른 색의 말인지 확인
        if piece.color != color:
            return False
        
        # 같은 위치로의 이동은 불가능
        if from_pos == to_pos:
            return False
        
        # 말의 기본 이동 규칙 확인
        possible_moves = piece.get_possible_moves(self.board.board, from_pos)
        if to_pos not in possible_moves:
            return False
        
        return True
    
    def _would_expose_king(self, from_pos: Position, to_pos: Position, color: str) -> bool:
        """이동 후 킹이 체크 상태가 되는지 검사"""
        # 임시로 말을 이동시켜보기
        original_board = [row[:] for row in self.board.board]
        original_pieces = self.board.pieces.copy()
        
        # 말 이동
        piece = self.board.get_piece(from_pos)
        if piece:
            # 기존 위치 제거
            self.board.board[from_pos.row][from_pos.col] = ''
            del self.board.pieces[from_pos]
            
            # 목적지에 상대 말이 있다면 제거
            if to_pos in self.board.pieces:
                del self.board.pieces[to_pos]
            
            # 말 이동
            self.board.board[to_pos.row][to_pos.col] = piece.name
            self.board.pieces[to_pos] = piece
            
            # 킹이 체크 상태인지 확인
            is_exposed = self._is_king_in_check(color)
            
            # 원래 상태로 복원
            self.board.board = original_board
            self.board.pieces = original_pieces
            
            return is_exposed
        
        return False
    
    def _is_king_in_check(self, color: str) -> bool:
        """특정 색의 킹이 체크 상태인지 확인"""
        king_name = f"{color}_king"
        king_pos = None
        
        # 킹 위치 찾기
        for row in range(4):
            for col in range(4):
                if self.board.board[row][col] == king_name:
                    king_pos = Position(row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # 상대방 말들이 킹을 공격할 수 있는지 확인
        attacking_color = 'black' if color == 'white' else 'white'
        
        for piece_pos, piece in self.board.pieces.items():
            if piece.color == attacking_color:
                possible_moves = piece.get_possible_moves(self.board.board, piece_pos)
                if king_pos in possible_moves:
                    return True
        
        return False 
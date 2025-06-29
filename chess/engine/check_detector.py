from typing import List, Optional
from ..domain.board import Board
from ..domain.position import Position
from ..domain.piece import Piece

class CheckDetector:
    """체크/체크메이트 감지"""
    
    def __init__(self, board: Board):
        self.board = board
    
    def is_king_in_check(self, color: str) -> bool:
        """특정 색의 킹이 체크 상태인지 확인"""
        king_pos = self._get_king_position(color)
        if not king_pos:
            return False
        
        return self._is_position_under_attack(king_pos, color)
    
    def is_checkmate(self, color: str) -> bool:
        """특정 색이 체크메이트 상태인지 확인"""
        # 1. 킹이 체크 상태인지 확인
        if not self.is_king_in_check(color):
            return False
        
        # 2. 킹이 벗어날 수 있는지 확인
        if self._can_escape_check(color):
            return False
        
        # 3. 다른 말로 체크를 막을 수 있는지 확인
        if self._can_block_check(color):
            return False
        
        return True
    
    def is_stalemate(self, color: str) -> bool:
        """특정 색이 스테일메이트 상태인지 확인"""
        # 1. 킹이 체크 상태가 아님
        if self.is_king_in_check(color):
            return False
        
        # 2. 하지만 모든 말이 움직일 수 없음
        return not self._has_legal_moves(color)
    
    def _get_king_position(self, color: str) -> Optional[Position]:
        """특정 색의 킹 위치 반환"""
        king_name = f"{color}_king"
        for row in range(4):
            for col in range(4):
                if self.board.board[row][col] == king_name:
                    return Position(row, col)
        return None
    
    def _is_position_under_attack(self, pos: Position, defending_color: str) -> bool:
        """특정 위치가 상대방 말들의 공격을 받고 있는지 확인"""
        attacking_color = 'black' if defending_color == 'white' else 'white'
        
        # 딕셔너리 복사본을 사용하여 순회
        pieces_copy = list(self.board.pieces.items())
        
        # 모든 상대방 말들의 가능한 이동 위치 확인
        for piece_pos, piece in pieces_copy:
            if piece.color == attacking_color:
                possible_moves = piece.get_possible_moves(self.board.board, piece_pos)
                if pos in possible_moves:
                    return True
        
        return False
    
    def _can_escape_check(self, color: str) -> bool:
        """체크 상태에서 벗어날 수 있는지 확인"""
        king_pos = self._get_king_position(color)
        if not king_pos:
            return False
        
        king = self.board.get_piece(king_pos)
        if not king:
            return False
        
        # 킹의 모든 가능한 이동 확인
        possible_moves = king.get_possible_moves(self.board.board, king_pos)
        
        for move in possible_moves:
            # 임시로 킹을 이동시켜보고 체크 상태인지 확인
            if self._is_move_safe(king_pos, move, color):
                return True
        
        return False
    
    def _can_block_check(self, color: str) -> bool:
        """다른 말로 체크를 막을 수 있는지 확인"""
        # 체크를 주는 말의 위치 찾기
        attacking_pieces = self._find_attacking_pieces(color)
        
        if len(attacking_pieces) > 1:
            # 더블 체크인 경우 다른 말로는 막을 수 없음
            return False
        
        if len(attacking_pieces) == 1:
            attacking_pos = attacking_pieces[0]
            king_pos = self._get_king_position(color)
            
            # 체크를 주는 말과 킹 사이의 경로 찾기
            blocking_positions = self._get_blocking_positions(attacking_pos, king_pos)
            
            # 체크를 주는 말을 직접 잡을 수도 있음
            blocking_positions.append(attacking_pos)
            
            # 다른 말로 그 경로를 막을 수 있는지 확인
            pieces_copy = list(self.board.pieces.items())
            for piece_pos, piece in pieces_copy:
                if piece.color == color and piece_pos != king_pos:
                    possible_moves = piece.get_possible_moves(self.board.board, piece_pos)
                    for move in possible_moves:
                        if move in blocking_positions and self._is_move_safe(piece_pos, move, color):
                            return True
        
        return False
    
    def _has_legal_moves(self, color: str) -> bool:
        """특정 색이 합법적인 수를 둘 수 있는지 확인"""
        # 딕셔너리 복사본을 사용하여 순회
        pieces_copy = list(self.board.pieces.items())
        
        for piece_pos, piece in pieces_copy:
            if piece.color == color:
                possible_moves = piece.get_possible_moves(self.board.board, piece_pos)
                for move in possible_moves:
                    if self._is_move_safe(piece_pos, move, color):
                        return True
        return False
    
    def _find_attacking_pieces(self, defending_color: str) -> List[Position]:
        """특정 색의 킹을 공격하는 말들의 위치 찾기"""
        king_pos = self._get_king_position(defending_color)
        if not king_pos:
            return []
        
        attacking_pieces = []
        attacking_color = 'black' if defending_color == 'white' else 'white'
        
        # 딕셔너리 복사본을 사용하여 순회
        pieces_copy = list(self.board.pieces.items())
        
        for piece_pos, piece in pieces_copy:
            if piece.color == attacking_color:
                possible_moves = piece.get_possible_moves(self.board.board, piece_pos)
                if king_pos in possible_moves:
                    attacking_pieces.append(piece_pos)
        
        return attacking_pieces
    
    def _get_blocking_positions(self, attacking_pos: Position, king_pos: Position) -> List[Position]:
        """공격하는 말과 킹 사이의 경로 위치들 반환"""
        blocking_positions = []
        
        # 같은 행에 있는 경우
        if attacking_pos.row == king_pos.row:
            start_col = min(attacking_pos.col, king_pos.col) + 1
            end_col = max(attacking_pos.col, king_pos.col)
            for col in range(start_col, end_col):
                blocking_positions.append(Position(attacking_pos.row, col))
        
        # 같은 열에 있는 경우
        elif attacking_pos.col == king_pos.col:
            start_row = min(attacking_pos.row, king_pos.row) + 1
            end_row = max(attacking_pos.row, king_pos.row)
            for row in range(start_row, end_row):
                blocking_positions.append(Position(row, attacking_pos.col))
        
        # 대각선에 있는 경우
        elif abs(attacking_pos.row - king_pos.row) == abs(attacking_pos.col - king_pos.col):
            row_step = 1 if king_pos.row > attacking_pos.row else -1
            col_step = 1 if king_pos.col > attacking_pos.col else -1
            
            row = attacking_pos.row + row_step
            col = attacking_pos.col + col_step
            
            while (row, col) != (king_pos.row, king_pos.col):
                blocking_positions.append(Position(row, col))
                row += row_step
                col += col_step
        
        return blocking_positions
    
    def _is_move_safe(self, from_pos: Position, to_pos: Position, color: str) -> bool:
        """특정 이동이 안전한지 확인 (킹을 체크 상태로 만들지 않는지)"""
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
            is_safe = not self.is_king_in_check(color)
            
            # 원래 상태로 복원
            self.board.board = original_board
            self.board.pieces = original_pieces
            
            return is_safe
        
        return False 
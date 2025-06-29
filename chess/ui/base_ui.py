from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.position import Position
from ..domain.board import Board

class BaseUI(ABC):
    """UI 기본 인터페이스"""
    
    @abstractmethod
    def display_board(self, board: Board, selected_pos: Optional[Position] = None, 
                     possible_moves: Optional[List[Position]] = None):
        """보드 표시"""
        pass
    
    @abstractmethod
    def get_user_move(self, board: Board) -> Optional[Position]:
        """사용자 입력 받기"""
        pass
    
    @abstractmethod
    def show_message(self, message: str):
        """메시지 표시"""
        pass
    
    @abstractmethod
    def update_display(self, board: Board, selected_pos: Optional[Position] = None, 
                      possible_moves: Optional[List[Position]] = None):
        """화면 업데이트"""
        pass 
import pygame
import sys
import time
from typing import Optional, List
from .domain.board import Board
from .domain.position import Position
from .engine.game_engine import GameEngine
from .ui.pygame_ui import PygameUI

class GameController:
    """게임 진행을 관리하는 컨트롤러"""
    
    def __init__(self):
        self.board = Board()
        self.engine = GameEngine(self.board)
        self.ui = PygameUI()
        self.selected_pos: Optional[Position] = None
        self.possible_moves: List[Position] = []
        self.game_status = 'normal'
        self.game_message = ""
        self.game_over = False
        self.game_over_timer = 0
        
    def run(self):
        """게임 실행"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self._handle_mouse_click(event.pos)
            
            # 게임 상태 업데이트
            self._update_game_status()
            
            # 화면 업데이트
            self._update_display()
            
            # 게임 종료 처리
            if self.game_over and time.time() - self.game_over_timer > 5.0:
                running = False
        
        pygame.quit()
        sys.exit()
    
    def _handle_mouse_click(self, mouse_pos):
        """마우스 클릭 처리"""
        board_pos = self.ui.get_board_position(mouse_pos)
        
        if not board_pos:
            return
        
        # 말 선택 또는 이동
        if self.selected_pos is None:
            # 말 선택
            piece = self.board.get_piece(board_pos)
            if piece and piece.color == self.board.turn:
                self.selected_pos = board_pos
                self.engine.selected_piece_pos = board_pos  # engine에도 설정
                self.possible_moves = self.engine.get_legal_moves(board_pos)
                print(f"선택된 말: {piece.name}")
            else:
                print("잘못된 말을 선택했습니다.")
        else:
            # 같은 말을 다시 클릭한 경우 선택 취소
            if self.selected_pos == board_pos:
                self.selected_pos = None
                self.engine.selected_piece_pos = None  # engine에도 설정
                self.possible_moves = []
                print("선택 취소")
                return
            
            # 말 이동
            if self.engine.move_selected_piece(board_pos):
                self.selected_pos = None
                self.engine.selected_piece_pos = None  # engine에도 설정
                self.possible_moves = []
                print(f"말 이동 완료: {board_pos.row}, {board_pos.col}")
            else:
                print("유효하지 않은 움직임입니다.")
    
    def _update_game_status(self):
        """게임 상태 업데이트"""
        # 체크 상태 확인
        check_pos = None
        if self.engine.check_detector.is_king_in_check(self.board.turn):
            check_pos = self.engine.check_detector._get_king_position(self.board.turn)
        
        # 게임 종료 조건 확인
        if self.engine.check_detector.is_checkmate(self.board.turn):
            self.game_status = 'checkmate'
            winner = 'Black' if self.board.turn == 'white' else 'White'
            self.game_message = f"Checkmate! {winner} wins!"
            self.game_over = True
            self.game_over_timer = time.time()
        elif self.engine.check_detector.is_stalemate(self.board.turn):
            self.game_status = 'stalemate'
            self.game_message = "Stalemate! It's a draw!"
            self.game_over = True
            self.game_over_timer = time.time()
        elif self.engine.check_detector.is_insufficient_material():
            self.game_status = 'insufficient_material'
            self.game_message = "Insufficient material! It's a draw!"
            self.game_over = True
            self.game_over_timer = time.time()
        elif check_pos:
            self.game_status = 'check'
            self.game_message = f"{self.board.turn.capitalize()} king is in check!"
        else:
            self.game_status = 'normal'
            self.game_message = f"{self.board.turn.capitalize()}'s turn"
    
    def _update_display(self):
        """화면 업데이트"""
        check_pos = None
        if self.engine.check_detector.is_king_in_check(self.board.turn):
            check_pos = self.engine.check_detector._get_king_position(self.board.turn)
        
        self.ui.update_display(
            self.board,
            self.selected_pos,
            self.possible_moves,
            check_pos,
            self.game_status,
            self.game_message
        ) 
from typing import Optional
from .domain.board import Board
from .domain.position import Position
from .engine.game_engine import GameEngine
from .ui.base_ui import BaseUI

class GameController:
    """게임 전체를 관리하는 컨트롤러"""
    
    def __init__(self, ui: BaseUI):
        self.board = Board()
        self.game_engine = GameEngine(self.board)
        self.ui = ui
        self.game_status = 'normal'  # 게임 상태 추적
        self.current_message = ""  # 현재 메시지
        
    def run(self):
        """게임 실행"""
        # Pygame 루프
        import pygame
        clock = pygame.time.Clock()
        running = True
        
        # 선택된 말과 가능한 이동 위치 추적
        selected_pos = None
        possible_moves = []
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
                    # 게임이 종료된 상태라면 클릭 무시
                    if self.game_status in ['checkmate', 'stalemate']:
                        continue
                        
                    board_pos = self.ui.get_board_position(event.pos)
                    if board_pos:  # 유효한 보드 위치인지 확인
                        if self.game_engine.selected_piece_pos is None:  # 말을 선택하지 않은 경우
                            if self.game_engine.select_piece(board_pos):
                                selected_pos = board_pos
                                possible_moves = self.game_engine.get_legal_moves(selected_pos)
                                self.current_message = f"Piece selected: {self.board.get_piece(board_pos).name}"
                            else:
                                self.current_message = "Invalid piece selected"
                        else:  # 이동 위치 선택
                            # 같은 위치를 클릭한 경우 선택 취소
                            if board_pos == selected_pos:
                                selected_pos = None
                                possible_moves = []
                                self.game_engine.selected_piece_pos = None
                                self.current_message = "Selection cancelled"
                            else:
                                # 이동 시도
                                move_success = self.game_engine.move_selected_piece(board_pos)
                                
                                if move_success:
                                    # 이동 성공 시 선택 상태 초기화
                                    selected_pos = None
                                    possible_moves = []
                                    self.current_message = "Move completed"
                                    
                                    # 게임 상태 확인
                                    self.game_status = self.game_engine._check_game_status()
                                    
                                    # 게임 종료 여부 확인
                                    if self.game_status in ['checkmate', 'stalemate']:
                                        # UI 업데이트 후 딜레이
                                        self._update_display_with_check_status(selected_pos, possible_moves)
                                        print("Game ended. Closing in 5 seconds...")
                                        pygame.time.delay(5000)  # 5초 대기
                                        running = False
                                else:
                                    # 이동 실패 시 선택 상태 유지 (selected_pos와 possible_moves는 그대로)
                                    self.current_message = "Invalid move"
            
            # 게임이 진행 중일 때만 일반적인 화면 업데이트
            if self.game_status not in ['checkmate', 'stalemate']:
                self._update_display_with_check_status(selected_pos, possible_moves)
            
            clock.tick(30)  # 초당 30 프레임으로 제한
        
        pygame.quit()
    
    def _update_display_with_check_status(self, selected_pos, possible_moves):
        """체크 상태를 포함한 화면 업데이트"""
        # 체크 상태 확인
        check_pos = None
        if self.game_engine.check_detector.is_king_in_check(self.board.turn):
            check_pos = self.game_engine.check_detector._get_king_position(self.board.turn)
        
        # 화면 업데이트
        self.ui.update_display(self.board, selected_pos, possible_moves, check_pos, self.game_status, self.current_message) 
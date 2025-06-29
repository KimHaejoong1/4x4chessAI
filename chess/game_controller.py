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
                    board_pos = self.ui.get_board_position(event.pos)
                    if board_pos:  # 유효한 보드 위치인지 확인
                        if self.game_engine.selected_piece_pos is None:  # 말을 선택하지 않은 경우
                            if self.game_engine.select_piece(board_pos):
                                selected_pos = board_pos
                                possible_moves = self.board.get_possible_moves(selected_pos)
                        else:  # 이동 위치 선택
                            self.game_engine.move_selected_piece(board_pos)
                            selected_pos = None
                            possible_moves = []
                            
                            # 게임 종료 여부 확인
                            if not self.game_engine.running:
                                print("게임이 종료되었습니다. 5초 후 창이 닫힙니다.")
                                pygame.time.delay(5000)  # 5초 대기
                                running = False
            
            # 화면 업데이트
            self.ui.update_display(self.board, selected_pos, possible_moves)
            clock.tick(30)  # 초당 30 프레임으로 제한
        
        pygame.quit() 
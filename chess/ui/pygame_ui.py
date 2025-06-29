import pygame
import sys
from typing import Optional, List
from .base_ui import BaseUI
from ..domain.position import Position
from ..domain.board import Board

class PygameUI(BaseUI):
    """Pygame UI 구현"""
    
    def __init__(self, screen_width: int = 900, screen_height: int = 700):
        # Pygame 초기화 및 디스플레이 설정
        pygame.init()
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("4 x 4 chess")
        
        # 크기 정의 및 보드 위치 설정
        self.block_size = 160
        self.border_thickness = 3
        self.board_size = 4 * self.block_size + 5 * self.border_thickness
        self.start_x = (self.screen_width - self.board_size) / 2
        self.start_y = (self.screen_height - self.board_size) / 2
        
        # 색상 및 체스말 이미지 로드
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.beige = (245, 245, 220)
        self.brown = (151, 88, 43)
        self.highlight_color = (100, 200, 100, 100)  # 선택된 말이나 가능한 이동 위치 표시
        self.check_color = (255, 100, 100, 150)  # 체크 상태 하이라이트
        
        # UI 정보 표시용 색상
        self.info_bg_color = (50, 50, 50, 200)
        self.text_color = (255, 255, 255)
        self.turn_white_color = (255, 255, 255)
        self.turn_black_color = (0, 0, 0)
        self.error_color = (255, 100, 100)
        self.success_color = (100, 255, 100)
        
        self.chess_piece = {}
        self.piece_size = 100
        self.load_chess_pieces()
        
        # 폰트 초기화
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
    def load_chess_pieces(self):
        """체스 말 이미지 로드"""
        colors = ['black', 'white']
        pieces = ['king', 'queen', 'rook', 'pawn']
        
        for color in colors:
            for piece in pieces:
                dict_key = f'{color}_{piece}'
                try:
                    self.chess_piece[dict_key] = pygame.transform.scale(
                        pygame.image.load(f'image/{dict_key}.png'),
                        (self.piece_size, self.piece_size)
                    )
                except pygame.error:
                    print(f"Error loading image for {dict_key}")
                    sys.exit()
                    
    def draw_chess_board(self):
        """체스 보드 그리기"""
        self.screen.fill(self.white)
        pygame.draw.rect(self.screen, self.black, (self.start_x, self.start_y, self.board_size, self.board_size))
        
        for row in range(4):
            for col in range(4):
                x = self.start_x + col * (self.block_size + self.border_thickness) + self.border_thickness
                y = self.start_y + row * (self.block_size + self.border_thickness) + self.border_thickness
                color = self.beige if (row + col) % 2 == 0 else self.brown
                pygame.draw.rect(self.screen, color, (x, y, self.block_size, self.block_size))
                
    def draw_chess_pieces(self, board: Board, selected_pos: Optional[Position] = None, 
                         possible_moves: Optional[List[Position]] = None, check_pos: Optional[Position] = None):
        """체스 말 그리기"""
        # 기본 보드 그리기
        self.draw_chess_board()
        
        # 체크 상태 하이라이트 (가장 아래 레이어)
        if check_pos:
            x = self.start_x + check_pos.col * (self.block_size + self.border_thickness) + self.border_thickness
            y = self.start_y + check_pos.row * (self.block_size + self.border_thickness) + self.border_thickness
            highlight = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
            highlight.fill(self.check_color)
            self.screen.blit(highlight, (x, y))
        
        # 가능한 이동 위치 하이라이트
        if possible_moves:
            for move in possible_moves:
                x = self.start_x + move.col * (self.block_size + self.border_thickness) + self.border_thickness
                y = self.start_y + move.row * (self.block_size + self.border_thickness) + self.border_thickness
                highlight = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
                highlight.fill((100, 100, 200, 100))
                self.screen.blit(highlight, (x, y))
        
        # 선택된 위치 하이라이트
        if selected_pos:
            x = self.start_x + selected_pos.col * (self.block_size + self.border_thickness) + self.border_thickness
            y = self.start_y + selected_pos.row * (self.block_size + self.border_thickness) + self.border_thickness
            highlight = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
            highlight.fill(self.highlight_color)
            self.screen.blit(highlight, (x, y))
        
        # 말 그리기 (가장 위 레이어)
        for row in range(4):
            for col in range(4):
                piece_name = board.board[row][col]
                if piece_name:
                    piece_image = self.chess_piece[piece_name]
                    x = self.start_x + col * (self.block_size + self.border_thickness) + self.border_thickness + (self.block_size - self.piece_size) / 2
                    y = self.start_y + row * (self.block_size + self.border_thickness) + self.border_thickness + (self.block_size - self.piece_size) / 2
                    self.screen.blit(piece_image, (x, y))
    
    def draw_game_info(self, board: Board, game_status: str = 'normal', message: str = ""):
        """게임 정보 표시"""
        # 정보 패널 배경
        info_panel = pygame.Surface((300, 200), pygame.SRCALPHA)
        info_panel.fill(self.info_bg_color)
        
        # 패널 위치 (오른쪽 상단)
        panel_x = self.screen_width - 320
        panel_y = 20
        
        # 현재 턴 표시
        turn_text = f"Turn: {'White' if board.turn == 'white' else 'Black'}"
        turn_color = self.turn_white_color if board.turn == 'white' else self.turn_black_color
        turn_surface = self.font_medium.render(turn_text, True, turn_color)
        info_panel.blit(turn_surface, (10, 10))
        
        # 게임 상태 표시
        status_text = ""
        status_color = self.text_color
        
        if game_status == 'check':
            status_text = "CHECK!"
            status_color = self.error_color
        elif game_status == 'checkmate':
            status_text = "CHECKMATE!"
            status_color = self.error_color
        elif game_status == 'stalemate':
            status_text = "STALEMATE!"
            status_color = self.error_color
        else:
            status_text = "Game in Progress"
            status_color = self.success_color
        
        status_surface = self.font_medium.render(status_text, True, status_color)
        info_panel.blit(status_surface, (10, 40))
        
        # 추가 메시지 표시
        if message:
            message_surface = self.font_small.render(message, True, self.text_color)
            info_panel.blit(message_surface, (10, 70))
        
        # 사용법 안내
        instruction_text = "Click: Select/Move Piece"
        instruction_surface = self.font_small.render(instruction_text, True, self.text_color)
        info_panel.blit(instruction_surface, (10, 170))
        
        # 패널을 화면에 그리기
        self.screen.blit(info_panel, (panel_x, panel_y))
                    
    def display_board(self, board: Board, selected_pos: Optional[Position] = None, 
                     possible_moves: Optional[List[Position]] = None, check_pos: Optional[Position] = None,
                     game_status: str = 'normal', message: str = ""):
        """보드 표시"""
        self.draw_chess_pieces(board, selected_pos, possible_moves, check_pos)
        self.draw_game_info(board, game_status, message)
        pygame.display.flip()
        
    def get_user_move(self, board: Board) -> Optional[Position]:
        """사용자 입력 받기 - 이 메서드는 pygame 이벤트 루프에서 호출됨"""
        # 이 메서드는 실제로는 사용되지 않고, main.py에서 직접 이벤트 처리
        pass
        
    def show_message(self, message: str):
        """메시지 표시"""
        print(message)  # 간단한 구현
        
    def update_display(self, board: Board, selected_pos: Optional[Position] = None, 
                      possible_moves: Optional[List[Position]] = None, check_pos: Optional[Position] = None,
                      game_status: str = 'normal', message: str = ""):
        """화면 업데이트"""
        self.display_board(board, selected_pos, possible_moves, check_pos, game_status, message)
        
    def get_board_position(self, mouse_pos) -> Optional[Position]:
        """마우스 위치를 보드의 행, 열 위치로 변환"""
        mouse_x, mouse_y = mouse_pos
        
        # 보드 영역 밖인지 확인
        if (mouse_x < self.start_x or mouse_x > self.start_x + self.board_size or
            mouse_y < self.start_y or mouse_y > self.start_y + self.board_size):
            return None
            
        col = int((mouse_x - self.start_x) // (self.block_size + self.border_thickness))
        row = int((mouse_y - self.start_y) // (self.block_size + self.border_thickness))
        
        if 0 <= row < 4 and 0 <= col < 4:
            return Position(row, col)
        return None 
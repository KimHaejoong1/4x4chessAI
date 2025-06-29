import pygame
import sys
import time
from typing import Optional, List
from .base_ui import BaseUI
from ..domain.position import Position
from ..domain.board import Board
from ..engine.game_engine import GameEngine

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
        
        self.board = None
        self.engine = None
        self.font = None
        self.small_font = None
        self.images = {}
        self.square_size = 100
        self.margin = 50
        self.window_width = self.board_size + 2 * self.margin
        self.window_height = self.board_size + 2 * self.margin + 100  # 메시지 영역 추가
        self.colors = {
            'light': (240, 217, 181),
            'dark': (181, 136, 99),
            'highlight': (255, 255, 0),
            'selected': (255, 255, 0),
            'legal_move': (144, 238, 144),
            'check': (255, 0, 0),
            'text': (0, 0, 0),
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        self.game_message = ""
        self.message_timer = 0
        self.game_over = False
        self.game_over_timer = 0
        
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
        elif game_status == 'insufficient_material':
            status_text = "DRAW!"
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
        """보드와 게임 정보 표시"""
        self.draw_chess_pieces(board, selected_pos, possible_moves, check_pos)
        self.draw_game_info(board, game_status, message)
        pygame.display.flip()
        
    def get_user_move(self, board: Board) -> Optional[Position]:
        """사용자로부터 이동 입력 받기"""
        # 이 메서드는 게임 컨트롤러에서 사용되지 않음
        pass
        
    def show_message(self, message: str):
        """메시지 표시"""
        print(message)  # 간단한 구현
        
    def update_display(self, board: Board, selected_pos: Optional[Position] = None, 
                      possible_moves: Optional[List[Position]] = None, check_pos: Optional[Position] = None,
                      game_status: str = 'normal', message: str = ""):
        """디스플레이 업데이트"""
        self.display_board(board, selected_pos, possible_moves, check_pos, game_status, message)
        
    def get_board_position(self, mouse_pos) -> Optional[Position]:
        """마우스 위치를 보드 좌표로 변환"""
        x, y = mouse_pos
        
        # 보드 영역 내인지 확인
        if (self.start_x <= x <= self.start_x + self.board_size and 
            self.start_y <= y <= self.start_y + self.board_size):
            
            # 보드 좌표 계산
            col = int((x - self.start_x - self.border_thickness) / (self.block_size + self.border_thickness))
            row = int((y - self.start_y - self.border_thickness) / (self.block_size + self.border_thickness))
            
            if 0 <= row < 4 and 0 <= col < 4:
                return Position(row, col)
        return None

    def initialize(self):
        """UI 초기화"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("4x4 Chess")
        
        # 폰트 초기화
        try:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
        except:
            self.font = pygame.font.SysFont('arial', 36)
            self.small_font = pygame.font.SysFont('arial', 24)
        
        # 이미지 로드
        self._load_images()
        
    def _load_images(self):
        """체스 말 이미지 로드"""
        piece_images = [
            'white_king', 'white_queen', 'white_rook', 'white_pawn',
            'black_king', 'black_queen', 'black_rook', 'black_pawn'
        ]
        
        for piece in piece_images:
            try:
                image_path = f"image/{piece}.png"
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (self.square_size - 10, self.square_size - 10))
                self.images[piece] = image
            except pygame.error as e:
                print(f"이미지 로드 실패: {image_path} - {e}")
                # 이미지가 없으면 빈 이미지 생성
                self.images[piece] = pygame.Surface((self.square_size - 10, self.square_size - 10))
                self.images[piece].fill((128, 128, 128))
    
    def run(self):
        """게임 루프 실행"""
        self.initialize()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self._handle_mouse_click(event.pos)
                    
            self._update()
            self._draw()
            pygame.display.flip()
            
    def _handle_mouse_click(self, pos):
        """마우스 클릭 처리"""
        # 보드 영역 계산
        board_x = self.margin
        board_y = self.margin
        
        # 클릭 위치가 보드 안인지 확인
        if (board_x <= pos[0] <= board_x + self.board_size and 
            board_y <= pos[1] <= board_y + self.board_size):
            
            # 보드 좌표로 변환
            col = (pos[0] - board_x) // self.square_size
            row = (pos[1] - board_y) // self.square_size
            
            board_pos = Position(row, col)
            
            # 게임 엔진에 클릭 전달
            if self.engine.handle_click(board_pos):
                # 게임 상태 확인
                game_status = self.engine._check_game_status()
                self._update_game_message(game_status)
                
                # 게임 종료 조건 확인
                if game_status in ['checkmate', 'stalemate', 'insufficient_material']:
                    self.game_over = True
                    self.game_over_timer = time.time()
    
    def _update_game_message(self, game_status):
        """게임 상태에 따른 메시지 업데이트"""
        if game_status == 'checkmate':
            winner = 'Black' if self.board.turn == 'white' else 'White'
            self.game_message = f"Checkmate! {winner} wins!"
        elif game_status == 'stalemate':
            self.game_message = "Stalemate! It's a draw!"
        elif game_status == 'insufficient_material':
            self.game_message = "Insufficient material! It's a draw!"
        elif game_status == 'check':
            self.game_message = f"{self.board.turn.capitalize()} king is in check!"
        else:
            self.game_message = f"{self.board.turn.capitalize()}'s turn"
        
        self.message_timer = time.time()
    
    def _update(self):
        """게임 상태 업데이트"""
        current_time = time.time()
        
        # 메시지 타이머 업데이트
        if current_time - self.message_timer > 3.0 and not self.game_over:
            self.game_message = f"{self.board.turn.capitalize()}'s turn"
        
        # 게임 종료 후 5초 후 종료
        if self.game_over and current_time - self.game_over_timer > 5.0:
            pygame.quit()
            sys.exit()
    
    def _draw(self):
        """화면 그리기"""
        self.screen.fill(self.colors['white'])
        
        # 보드 그리기
        self._draw_board()
        
        # 말 그리기
        self._draw_pieces()
        
        # UI 요소 그리기
        self._draw_ui()
    
    def _draw_board(self):
        """체스 보드 그리기"""
        board_x = self.margin
        board_y = self.margin
        
        for row in range(4):
            for col in range(4):
                x = board_x + col * self.square_size
                y = board_y + row * self.square_size
                
                # 기본 색상
                color = self.colors['light'] if (row + col) % 2 == 0 else self.colors['dark']
                
                # 선택된 말 하이라이트
                if (self.engine.selected_piece_pos and 
                    self.engine.selected_piece_pos.row == row and 
                    self.engine.selected_piece_pos.col == col):
                    color = self.colors['selected']
                
                # 합법적인 이동 위치 하이라이트
                if self.engine.selected_piece_pos:
                    legal_moves = self.engine.get_legal_moves(self.engine.selected_piece_pos)
                    if Position(row, col) in legal_moves:
                        color = self.colors['legal_move']
                
                # 체크 상태 하이라이트
                if self.engine.check_detector.is_king_in_check(self.board.turn):
                    king_pos = self.engine.check_detector._get_king_position(self.board.turn)
                    if king_pos and king_pos.row == row and king_pos.col == col:
                        color = self.colors['check']
                
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, self.colors['black'], (x, y, self.square_size, self.square_size), 1)
    
    def _draw_pieces(self):
        """체스 말 그리기"""
        board_x = self.margin
        board_y = self.margin
        
        for row in range(4):
            for col in range(4):
                piece_name = self.board.board[row][col]
                if piece_name:
                    x = board_x + col * self.square_size + 5
                    y = board_y + row * self.square_size + 5
                    
                    if piece_name in self.images:
                        self.screen.blit(self.images[piece_name], (x, y))
                    else:
                        # 이미지가 없으면 텍스트로 표시
                        text = self.small_font.render(piece_name, True, self.colors['text'])
                        text_rect = text.get_rect(center=(x + self.square_size//2 - 5, y + self.square_size//2 - 5))
                        self.screen.blit(text, text_rect)
    
    def _draw_ui(self):
        """UI 요소 그리기"""
        # 게임 메시지
        if self.game_message:
            text = self.font.render(self.game_message, True, self.colors['text'])
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height - 50))
            self.screen.blit(text, text_rect)
        
        # 게임 종료 시 추가 메시지
        if self.game_over:
            exit_text = self.small_font.render("Game will exit in 5 seconds...", True, self.colors['text'])
            exit_rect = exit_text.get_rect(center=(self.window_width // 2, self.window_height - 20))
            self.screen.blit(exit_text, exit_rect) 
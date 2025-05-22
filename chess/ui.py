import pygame
import sys

class ChessUI:
    def __init__(self):
        # Pygame 초기화 및 디스플레이 설정
        pygame.init()
        
        self.screen_width = 900
        self.screen_height = 700
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
        
        self.chess_piece = {}
        self.piece_size = 100
        self.load_chess_pieces()
        
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
                
    def draw_chess_pieces(self, board, selected_pos=None, possible_moves=None):
        """체스 말 그리기"""
        # 기본 보드 그리기
        self.draw_chess_board()
        
        # 선택된 위치 하이라이트
        if selected_pos:
            row, col = selected_pos
            x = self.start_x + col * (self.block_size + self.border_thickness) + self.border_thickness
            y = self.start_y + row * (self.block_size + self.border_thickness) + self.border_thickness
            highlight = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
            highlight.fill((100, 200, 100, 100))
            self.screen.blit(highlight, (x, y))
            
        # 가능한 이동 위치 하이라이트
        if possible_moves:
            for move in possible_moves:
                row, col = move
                x = self.start_x + col * (self.block_size + self.border_thickness) + self.border_thickness
                y = self.start_y + row * (self.block_size + self.border_thickness) + self.border_thickness
                highlight = pygame.Surface((self.block_size, self.block_size), pygame.SRCALPHA)
                highlight.fill((100, 100, 200, 100))
                self.screen.blit(highlight, (x, y))
        
        # 말 그리기
        for row in range(4):
            for col in range(4):
                piece = board[row][col]
                if piece:
                    piece_image = self.chess_piece[piece]
                    x = self.start_x + col * (self.block_size + self.border_thickness) + self.border_thickness + (self.block_size - self.piece_size) / 2
                    y = self.start_y + row * (self.block_size + self.border_thickness) + self.border_thickness + (self.block_size - self.piece_size) / 2
                    self.screen.blit(piece_image, (x, y))
                    
    def update_display(self, board, selected_pos=None, possible_moves=None):
        """화면 업데이트"""
        self.draw_chess_pieces(board, selected_pos, possible_moves)
        pygame.display.flip()
        
    def get_board_position(self, mouse_pos):
        """마우스 위치를 보드의 행, 열 위치로 변환"""
        mouse_x, mouse_y = mouse_pos
        
        # 보드 영역 밖인지 확인
        if (mouse_x < self.start_x or mouse_x > self.start_x + self.board_size or
            mouse_y < self.start_y or mouse_y > self.start_y + self.board_size):
            return None
            
        col = int((mouse_x - self.start_x) // (self.block_size + self.border_thickness))
        row = int((mouse_y - self.start_y) // (self.block_size + self.border_thickness))
        
        if 0 <= row < 4 and 0 <= col < 4:
            return (row, col)
        return None
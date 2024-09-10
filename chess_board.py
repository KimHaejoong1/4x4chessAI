import pygame
import sys

# Pygame 초기화 및 디스플레이 설정
pygame.init()

screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("4 x 4 chess")

# 크기 정의 및 보드 위치 설정
block_size = 160
border_thickness = 3
board_size = 4 * block_size + 5 * border_thickness
start_x = (screen_width - board_size) / 2
start_y = (screen_height - board_size) / 2

# 색상 및 체스말 이미지 로드
white = (255, 255, 255)
black = (0, 0, 0)
beige = (245, 245, 220)
brown = (151, 88, 43)
chess_piece = {}
piece_size = 100
colors = ['black', 'white']
pieces = ['king', 'queen', 'rook', 'pawn']

for color in colors:
    for piece in pieces:
        dict_key = f'{color}_{piece}'
        try:
            chess_piece[dict_key] = pygame.transform.scale(
                pygame.image.load(f'image/{dict_key}.png'),
                (piece_size, piece_size)
            )
        except pygame.error:
            print(f"Error loading image for {dict_key}")
            sys.exit()

# Pygame 보드 그리기 함수
def draw_chess_board():
    screen.fill(white)
    pygame.draw.rect(screen, black, (start_x, start_y, board_size, board_size))
    for row in range(4):
        for col in range(4):
            x = start_x + col * (block_size + border_thickness) + border_thickness
            y = start_y + row * (block_size + border_thickness) + border_thickness
            color = beige if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color, (x, y, block_size, block_size))

# Pygame 체스말 그리기 함수
def draw_chess_pieces(board):
    for row in range(4):
        for col in range(4):
            piece = board[row][col]
            if piece:
                piece_image = chess_piece[piece]
                x = start_x + col * (block_size + border_thickness) + border_thickness + (block_size - piece_size) / 2
                y = start_y + row * (block_size + border_thickness) + border_thickness + (block_size - piece_size) / 2
                screen.blit(piece_image, (x, y))

def update_display(board):
    draw_chess_board()
    draw_chess_pieces(board)
    pygame.display.flip()

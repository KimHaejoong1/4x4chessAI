import pygame
import sys

# pygame 초기화
pygame.init()

# 디스플레이 초기화
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# 제목 설정
pygame.display.set_caption("4 x 4 chess")

# 크기 정의
block_size = 160
border_thickness = 3
board_size = 4 * block_size + 5 * border_thickness

# 체스 보드 위치
start_x = (screen_width - board_size) / 2
start_y = (screen_height - board_size) / 2

# 색상 정의
white = (255, 255, 255)
black = (0, 0, 0)
beige = (245, 245, 220)
brown = (151, 88, 43)

# 체스말 초기화
chess_piece = {}
piece_size  = 100
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

def draw_chess_board():
    screen.fill(white)
    pygame.draw.rect(screen, black, (start_x, start_y, board_size, board_size))

    # 체스 보드의 사각형 그리기
    for row in range(4):
        for col in range(4):
            x = start_x + col * (block_size + border_thickness) + border_thickness
            y = start_y + row * (block_size + border_thickness) + border_thickness

            color = beige if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color, (x, y, block_size, block_size))

def draw_chess_pieces():
    initial_setup = [
        ['black_rook', 'black_queen', 'black_king', 'black_rook'],
        ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
        ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
        ['white_rook', 'white_queen', 'white_king', 'white_rook']
    ]

    for row in range(4):
        for col in range(4):
            piece_image = chess_piece[initial_setup[row][col]]
            x = start_x + col * (block_size + border_thickness) + border_thickness + (block_size - piece_size) / 2
            y = start_y + row * (block_size + border_thickness) + border_thickness + (block_size - piece_size) / 2

            screen.blit(piece_image, (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_chess_board()
    draw_chess_pieces()
    pygame.display.flip()

pygame.quit()
sys.exit()

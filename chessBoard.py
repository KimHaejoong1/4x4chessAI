import pygame
import sys

#pygame initialization
pygame.init()

#display initialization
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

#title
pygame.display.set_caption("4 x 4 chess")

#define size
block_size = 160
border_thickness = 5
board_size = 4 * block_size + 5 * border_thickness

#define color
white = (255, 255, 255)
black = (0, 0, 0)
beige = (245, 245, 220)
brown = (151, 88, 43)

#chess piece init
chess_piece = {}
colors = ['black','white']
pieces = ['king','queen','rook','pawn']
for color in colors:
    for piece in pieces:
        dict_key = f'{color}_{piece}'
        chess_piece[dict_key] = pygame.transform.scale(pygame.image.load(f'image/{dict_key}.png'), (block_size, block_size))

def draw_chess_board():
    
    screen.fill(white)

    #chess board border
    start_x = (screen_width - board_size) / 2
    start_y = (screen_height - board_size) / 2
    pygame.draw.rect(screen, black, (start_x, start_y, board_size, board_size) )

    #chess board square
    for row in range(4):
        for col in range(4):
            x = start_x + col * (block_size + border_thickness) + border_thickness
            y = start_y + row * (block_size + border_thickness) + border_thickness

            if (row + col) % 2 == 0:
                color = beige
            else:
                color = brown
            pygame.draw.rect(screen, color, (x, y, block_size, block_size))

running = True
while running:
    #check event
    for event in pygame.event.get():
        #click close button
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(white)
    draw_chess_board()
    #display update
    pygame.display.flip()

#exit
pygame.quit()
sys.exit()
from chess_game import ChessBoard
from chess_board import update_display, start_x, start_y, block_size, border_thickness
import pygame
import sys

# 체스 보드 초기화
chess_board = ChessBoard()

# Pygame 초기화
pygame.init()

# 선택된 말과 이동 위치를 추적하기 위한 변수
selected_piece_pos = None

# Pygame 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 클릭 이벤트
            mouse_x, mouse_y = event.pos
            # 클릭한 위치를 체스 보드의 행, 열로 변환
            col = int((mouse_x - start_x) // (block_size + border_thickness))
            row = int((mouse_y - start_y) // (block_size + border_thickness))
            if 0 <= row < 4 and 0 <= col < 4:  # 유효한 보드 위치인지 확인
                if selected_piece_pos is None:  # 말을 선택하지 않은 경우
                    piece = chess_board.board[row][col]
                    if piece and chess_board.turn in piece:  # 현재 턴의 말을 선택
                        selected_piece_pos = (row, col)
                        print(f"선택된 말: {piece} (위치: {selected_piece_pos})")
                    else:
                        print("잘못된 말을 선택했습니다.")
                else:  # 이동 위치 선택
                    end_pos = (row, col)
                    if chess_board.move_piece(selected_piece_pos, end_pos):
                        print(f"말 이동 완료: {selected_piece_pos} -> {end_pos}")
                        selected_piece_pos = None
                    else:
                        print("유효하지 않은 움직임입니다. 다시 시도하세요.")

    # Pygame 보드 업데이트
    update_display(chess_board.board)

    # 승리 조건 확인
    if chess_board.is_king_captured():
        print(f"{chess_board.turn} 팀이 이겼습니다!")
        break

pygame.quit()
sys.exit()

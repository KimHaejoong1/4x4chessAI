from chess_game import ChessBoard
from chess_board import update_display
import pygame
import sys

# 체스 보드 초기화
chess_board = ChessBoard()

# Pygame 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Pygame 보드 업데이트
    update_display(chess_board.board)

    # 터미널에 텍스트 보드 출력
    print(f"{chess_board.turn}의 차례입니다.")
    chess_board.display()

    if chess_board.is_king_captured():
        print(f"{chess_board.turn} 팀이 이겼습니다!")
        break

    while True:
        start_pos = tuple(map(int, input("이동할 말을 선택하세요 (행 열): ").split()))
        piece = chess_board.board[start_pos[0]][start_pos[1]]

        if piece == '' or chess_board.turn not in piece:
            print(f"잘못된 말 선택입니다. {chess_board.turn}의 말을 선택하세요.")
            continue
        else:
            break

    possible_moves = chess_board.get_possible_moves(start_pos)

    if not possible_moves:
        print("이동 가능한 위치가 없습니다. 다른 말을 선택하세요.")
        continue

    print(f"이동 가능한 위치: {possible_moves}")

    end_pos = tuple(map(int, input("이동할 위치를 입력하세요 (행 열): ").split()))
    if chess_board.move_piece(start_pos, end_pos):
        print("이동 완료!")
    else:
        print("유효하지 않은 움직임입니다. 다시 시도하세요.")

pygame.quit()
sys.exit()

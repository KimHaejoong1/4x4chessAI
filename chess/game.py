import pygame
from chess.board import Board

class ChessGame:
    def __init__(self, display_handler=None):
        self.board = Board()
        self.selected_piece_pos = None
        self.display_handler = display_handler
        self.running = True
        
    def select_piece(self, pos):
        """체스 말 선택"""
        row, col = pos
        piece = self.board.get_piece(pos)
        
        if piece and piece.color == self.board.turn:
            self.selected_piece_pos = pos
            print(f"선택된 말: {piece.name} (위치: {pos})")
            return True
        else:
            print("잘못된 말을 선택했습니다.")
            return False
            
    def move_selected_piece(self, pos):
        """선택된 말 이동"""
        if not self.selected_piece_pos:
            return False
            
        if self.selected_piece_pos == pos:
            piece = self.board.get_piece(pos)
            print(f"선택 취소: {piece.name if piece else ''} (위치: {pos})")
            self.selected_piece_pos = None
            return False
            
        if self.board.move_piece(self.selected_piece_pos, pos):
            print(f"말 이동 완료: {self.selected_piece_pos} -> {pos}")
            self.selected_piece_pos = None
            
            # 승리 조건 확인
            if self.board.is_king_captured():
                winner = 'black' if self.board.turn == 'white' else 'white'
                print(f"{winner} 팀이 이겼습니다!")
                self.running = False
                
            return True
        else:
            print("유효하지 않은 움직임입니다. 다시 시도하세요.")
            return False
            
    def handle_click(self, pos):
        """마우스 클릭 처리"""
        row, col = pos
        
        if 0 <= row < 4 and 0 <= col < 4:  # 유효한 보드 위치인지 확인
            if self.selected_piece_pos is None:  # 말을 선택하지 않은 경우
                self.select_piece(pos)
            else:  # 이동 위치 선택
                self.move_selected_piece(pos)
                
            # UI 업데이트
            if self.display_handler:
                self.display_handler(self.board.board)
                
        return self.running
            
    def run_console_game(self):
        """콘솔 기반 게임 실행"""
        while self.running:
            self.board.display()
            print(f"{self.board.turn}의 차례입니다.")
            
            try:
                # 말 선택
                start_row = int(input("선택할 말의 행 (0-3): "))
                start_col = int(input("선택할 말의 열 (0-3): "))
                
                if not self.select_piece((start_row, start_col)):
                    continue
                    
                # 이동할 위치 선택
                end_row = int(input("이동할 위치의 행 (0-3): "))
                end_col = int(input("이동할 위치의 열 (0-3): "))
                
                self.move_selected_piece((end_row, end_col))
                
            except ValueError:
                print("유효한 숫자를 입력하세요.")
            except KeyboardInterrupt:
                print("\n게임을 종료합니다.")
                self.running = False
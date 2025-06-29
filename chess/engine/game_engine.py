from typing import Optional, List
from ..domain.board import Board
from ..domain.position import Position
from ..domain.piece import Piece
from .check_detector import CheckDetector
from .move_validator import MoveValidator

class GameEngine:
    """게임 진행을 관리하는 엔진"""
    
    def __init__(self, board: Board):
        self.board = board
        self.selected_piece_pos: Optional[Position] = None
        self.running = True
        self.check_detector = CheckDetector(board)
        self.move_validator = MoveValidator(board)
        
    def select_piece(self, pos: Position) -> bool:
        """체스 말 선택"""
        piece = self.board.get_piece(pos)
        
        if piece and piece.color == self.board.turn:
            self.selected_piece_pos = pos
            print(f"선택된 말: {piece.name} (위치: {pos.row}, {pos.col})")
            return True
        else:
            print("잘못된 말을 선택했습니다.")
            return False
            
    def move_selected_piece(self, pos: Position) -> bool:
        """선택된 말 이동"""
        if not self.selected_piece_pos:
            return False
            
        if self.selected_piece_pos == pos:
            piece = self.board.get_piece(pos)
            print(f"선택 취소: {piece.name if piece else ''} (위치: {pos.row}, {pos.col})")
            self.selected_piece_pos = None
            return False
            
        # 이동 유효성 검사
        if not self.move_validator.is_valid_move(self.selected_piece_pos, pos, self.board.turn):
            print("유효하지 않은 움직임입니다. 다시 시도하세요.")
            # 잘못된 움직임이어도 선택 상태는 유지
            return False
            
        if self.board.move_piece(self.selected_piece_pos, pos):
            print(f"말 이동 완료: ({self.selected_piece_pos.row}, {self.selected_piece_pos.col}) -> ({pos.row}, {pos.col})")
            self.selected_piece_pos = None
            
            # 게임 상태 확인
            self._check_game_status()
                
            return True
        else:
            print("유효하지 않은 움직임입니다. 다시 시도하세요.")
            # 잘못된 움직임이어도 선택 상태는 유지
            return False
    
    def _check_game_status(self):
        """게임 상태 확인 및 업데이트"""
        current_color = self.board.turn
        
        # 체크메이트 확인
        if self.check_detector.is_checkmate(current_color):
            winner = 'black' if current_color == 'white' else 'white'
            print(f"체크메이트! {winner} 팀이 승리했습니다!")
            # 게임 종료는 즉시 하지 않고, UI에서 처리하도록 함
            return 'checkmate'
            
        # 스테일메이트 확인
        elif self.check_detector.is_stalemate(current_color):
            print("스테일메이트! 무승부입니다.")
            # 게임 종료는 즉시 하지 않고, UI에서 처리하도록 함
            return 'stalemate'
            
        # 체크 확인
        elif self.check_detector.is_king_in_check(current_color):
            print(f"{current_color} 킹이 체크 상태입니다!")
            return 'check'
            
        return 'normal'
            
    def handle_click(self, pos: Position) -> bool:
        """마우스 클릭 처리"""
        if 0 <= pos.row < 4 and 0 <= pos.col < 4:  # 유효한 보드 위치인지 확인
            if self.selected_piece_pos is None:  # 말을 선택하지 않은 경우
                self.select_piece(pos)
            else:  # 이동 위치 선택
                self.move_selected_piece(pos)
                
        return self.running
    
    def get_legal_moves(self, pos: Position) -> List[Position]:
        """특정 위치에서 가능한 합법적인 이동들 반환"""
        return self.move_validator.get_legal_moves(pos, self.board.turn)
            
    def run_console_game(self):
        """콘솔 기반 게임 실행"""
        while self.running:
            self.board.display()
            print(f"{self.board.turn}의 차례입니다.")
            
            # 체크 상태 표시
            if self.check_detector.is_king_in_check(self.board.turn):
                print(f"{self.board.turn} 킹이 체크 상태입니다!")
            
            try:
                # 말 선택
                start_row = int(input("선택할 말의 행 (0-3): "))
                start_col = int(input("선택할 말의 열 (0-3): "))
                
                if not self.select_piece(Position(start_row, start_col)):
                    continue
                    
                # 이동할 위치 선택
                end_row = int(input("이동할 위치의 행 (0-3): "))
                end_col = int(input("이동할 위치의 열 (0-3): "))
                
                self.move_selected_piece(Position(end_row, end_col))
                
            except ValueError:
                print("유효한 숫자를 입력하세요.")
            except KeyboardInterrupt:
                print("\n게임을 종료합니다.")
                self.running = False 
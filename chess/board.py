from chess.piece import Pawn, Rook, King, Queen

class Board:
    def __init__(self):
        # 보드 초기화
        self.board = [[''] * 4 for _ in range(4)]
        self.pieces = {}
        self.initialize_board()
        self.turn = 'white'  # 선공은 백색 말
        
    def initialize_board(self):
        """체스 보드 초기 상태 설정"""
        # 검은색 말 배치
        self.place_piece(Rook('black'), (0, 0))
        self.place_piece(Queen('black'), (0, 1))
        self.place_piece(King('black'), (0, 2))
        self.place_piece(Rook('black'), (0, 3))
        
        # 검은색 폰 배치
        for col in range(4):
            self.place_piece(Pawn('black'), (1, col))
            
        # 흰색 폰 배치
        for col in range(4):
            self.place_piece(Pawn('white'), (2, col))
            
        # 흰색 말 배치
        self.place_piece(Rook('white'), (3, 0))
        self.place_piece(Queen('white'), (3, 1))
        self.place_piece(King('white'), (3, 2))
        self.place_piece(Rook('white'), (3, 3))
        
    def place_piece(self, piece, pos):
        """말을 보드에 배치"""
        row, col = pos
        self.board[row][col] = piece.name
        self.pieces[(row, col)] = piece
        
    def display(self):
        """콘솔에 체스 보드 표시"""
        print("         0            1            2            3")
        print("  +------------+------------+------------+------------+")
        for idx, row in enumerate(self.board):
            row_str = f"{idx} |"
            for piece in row:
                if piece == '':
                    row_str += "            |"
                else:
                    row_str += f" {piece:<11}|"
            print(row_str)
            print("  +------------+------------+------------+------------+")
        print()
        
    def get_piece(self, pos):
        """해당 위치의 말 객체 반환"""
        row, col = pos
        return self.pieces.get((row, col), None)
        
    def get_possible_moves(self, start):
        """특정 위치에서 가능한 모든 이동 위치 반환"""
        piece = self.get_piece(start)
        if not piece:
            return []
            
        return piece.get_possible_moves(self.board, start)
        
    def move_piece(self, start, end):
        """말 이동하기"""
        piece = self.get_piece(start)
        
        if not piece:
            print("선택된 위치에 말이 없습니다.")
            return False
            
        if self.turn not in piece.color:
            print()
            print(f"{self.turn}의 차례입니다.")
            return False
            
        possible_moves = self.get_possible_moves(start)
        if end not in possible_moves:
            print("유효하지 않은 움직임입니다.")
            return False
            
        # 기존 위치의 말 제거
        del self.pieces[start]
        
        # 목적지에 상대 말이 있다면 제거 (말 잡기)
        if end in self.pieces:
            del self.pieces[end]
            
        # 말 이동
        self.board[end[0]][end[1]] = piece.name
        self.board[start[0]][start[1]] = ''
        self.pieces[end] = piece
        
        # 턴 변경
        self.turn = 'black' if self.turn == 'white' else 'white'
        return True
        
    def is_king_captured(self):
        """왕이 잡혔는지 확인 (게임 종료 조건)"""
        # 현재 턴의 킹을 기준으로 확인
        king_name = f"{self.turn}_king"
        for row in self.board:
            if king_name in row:
                return False  # 현재 턴의 킹이 존재하면 게임 계속 진행
        return True  # 현재 턴의 킹이 없다면 게임 종료
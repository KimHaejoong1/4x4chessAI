class ChessBoard:
    def __init__(self):
        self.board = [
            ['black_rook', 'black_queen', 'black_king', 'black_rook'],
            ['black_pawn', 'black_pawn', 'black_pawn', 'black_pawn'],
            ['white_pawn', 'white_pawn', 'white_pawn', 'white_pawn'],
            ['white_rook', 'white_queen', 'white_king', 'white_rook']
        ]
        self.turn = 'white'  # 선공은 백색 말

    def display(self):
        # 열 번호 출력
        print("         0            1            2            3")
        print("  +------------+------------+------------+------------+")
        for idx, row in enumerate(self.board):
            # 행 번호 및 행 내용 출력
            row_str = f"{idx} |"
            for piece in row:
                if piece == '':
                    row_str += "            |"
                else:
                    row_str += f" {piece:<11}|"
            print(row_str)
            print("  +------------+------------+------------+------------+")
        print()

    def get_possible_moves(self, start):
        piece = self.board[start[0]][start[1]]
        possible_moves = []

        if not piece:
            return possible_moves

        for i in range(4):
            for j in range(4):
                if self.is_valid_move(piece, start, (i, j)):
                    possible_moves.append((i, j))
        return possible_moves

    def move_piece(self, start, end):
        piece = self.board[start[0]][start[1]]

        if not piece:
            print("선택된 위치에 말이 없습니다.")
            return False

        if self.turn not in piece:
            print()
            print(f"{self.turn}의 차례입니다.")
            return False

        possible_moves = self.get_possible_moves(start)
        if end not in possible_moves:
            print("유효하지 않은 움직임입니다.")
            return False

        self.board[end[0]][end[1]] = piece  # 상대방 말이 있으면 잡히게 됨
        self.board[start[0]][start[1]] = ''  # 원래 위치를 빈칸으로 설정
        self.turn = 'black' if self.turn == 'white' else 'white'
        return True

    def is_valid_move(self, piece, start, end):
        if 'pawn' in piece:
            return self.is_valid_pawn_move(piece, start, end)
        if 'rook' in piece:
            return self.is_valid_rook_move(piece, start, end)
        if 'king' in piece:
            return self.is_valid_king_move(piece, start, end)
        if 'queen' in piece:
            return self.is_valid_queen_move(piece, start, end)
        return False

    def is_valid_pawn_move(self, piece, start, end):
        direction = -1 if 'white' in piece else 1
        start_row, start_col = start
        end_row, end_col = end

        # 한 칸 앞으로 이동
        if start_col == end_col and self.board[end_row][end_col] == '':
            if end_row - start_row == direction:
                return True

        # 대각선 잡기
        if abs(end_col - start_col) == 1 and end_row - start_row == direction:
            if 'black' in piece and 'white' in self.board[end_row][end_col]:
                return True
            if 'white' in piece and 'black' in self.board[end_row][end_col]:
                return True

        return False

    def is_valid_rook_move(self, piece, start, end):
        if start[0] != end[0] and start[1] != end[1]:
            return False

        if not self.is_clear_path(start, end):
            return False

        if self.is_opponent_piece(piece, end):
            return True

        if self.board[end[0]][end[1]] == '':
            return True

        return False

    def is_valid_king_move(self, piece, start, end):
        if max(abs(start[0] - end[0]), abs(start[1] - end[1])) == 1:
            if self.is_opponent_piece(piece, end) or self.board[end[0]][end[1]] == '':
                return True

        return False

    def is_valid_queen_move(self, piece, start, end):
        if start[0] == end[0] or start[1] == end[1] or abs(start[0] - end[0]) == abs(start[1] - end[1]):
            if self.is_clear_path(start, end):
                if self.is_opponent_piece(piece, end) or self.board[end[0]][end[1]] == '':
                    return True

        return False

    def is_clear_path(self, start, end):
        row_step = 0 if start[0] == end[0] else (1 if end[0] > start[0] else -1)
        col_step = 0 if start[1] == end[1] else (1 if end[1] > start[1] else -1)

        row, col = start[0] + row_step, start[1] + col_step

        while (row, col) != end:
            if self.board[row][col] != '':
                return False
            row += row_step
            col += col_step

        return True

    def is_opponent_piece(self, piece, end):
        if 'white' in piece and 'black' in self.board[end[0]][end[1]]:
            return True
        if 'black' in piece and 'white' in self.board[end[0]][end[1]]:
            return True
        return False

    def is_king_captured(self):
        # 현재 턴의 킹을 기준으로 확인
        current_king = f"{self.turn}_king"
        for row in self.board:
            if current_king in row:
                return False  # 현재 턴의 킹이 존재하면 게임 계속 진행
        return True  # 현재 턴의 킹이 없다면 게임 종료
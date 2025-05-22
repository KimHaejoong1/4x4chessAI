from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color = color  # 'white' 또는 'black'
        
    @property
    def name(self):
        return f"{self.color}_{self.__class__.__name__.lower()}"
    
    @abstractmethod
    def get_possible_moves(self, board, pos):
        """현재 위치에서 가능한 모든 이동 위치 반환"""
        pass
    
    def is_opponent_piece(self, board, pos):
        """해당 위치에 상대편 말이 있는지 확인"""
        if board[pos[0]][pos[1]] == '':
            return False
        return 'white' in board[pos[0]][pos[1]] if self.color == 'black' else 'black' in board[pos[0]][pos[1]]
    
    def is_clear_path(self, board, start, end):
        """시작 위치와 끝 위치 사이에 다른 말이 없는지 확인"""
        row_step = 0 if start[0] == end[0] else (1 if end[0] > start[0] else -1)
        col_step = 0 if start[1] == end[1] else (1 if end[1] > start[1] else -1)

        row, col = start[0] + row_step, start[1] + col_step

        while (row, col) != end:
            if board[row][col] != '':
                return False
            row += row_step
            col += col_step

        return True


class Pawn(Piece):
    def get_possible_moves(self, board, pos):
        possible_moves = []
        row, col = pos
        direction = -1 if self.color == 'white' else 1
        
        # 한 칸 앞으로 이동
        if 0 <= row + direction < 4 and board[row + direction][col] == '':
            possible_moves.append((row + direction, col))
            
        # 대각선 잡기
        for side_col in [col - 1, col + 1]:
            if 0 <= side_col < 4 and 0 <= row + direction < 4:
                if board[row + direction][side_col] != '':
                    if self.is_opponent_piece(board, (row + direction, side_col)):
                        possible_moves.append((row + direction, side_col))
                        
        return possible_moves


class Rook(Piece):
    def get_possible_moves(self, board, pos):
        possible_moves = []
        row, col = pos
        
        # 수평 이동
        for new_col in range(4):
            if new_col != col:
                end = (row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        # 수직 이동
        for new_row in range(4):
            if new_row != row:
                end = (new_row, col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        return possible_moves


class King(Piece):
    def get_possible_moves(self, board, pos):
        possible_moves = []
        row, col = pos
        
        # 킹은 모든 방향으로 한 칸만 이동 가능
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # 현재 위치 제외
                    
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 4 and 0 <= new_col < 4:
                    if board[new_row][new_col] == '' or self.is_opponent_piece(board, (new_row, new_col)):
                        possible_moves.append((new_row, new_col))
                        
        return possible_moves


class Queen(Piece):
    def get_possible_moves(self, board, pos):
        possible_moves = []
        row, col = pos
        
        # 수평, 수직 이동 (룩처럼)
        for new_col in range(4):
            if new_col != col:
                end = (row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        for new_row in range(4):
            if new_row != row:
                end = (new_row, col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
        
        # 대각선 이동 (비숍처럼)
        for i in range(-3, 4):
            if i == 0:
                continue
                
            new_row, new_col = row + i, col + i
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                end = (new_row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
            new_row, new_col = row + i, col - i
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                end = (new_row, new_col)
                if self.is_clear_path(board, pos, end):
                    if board[end[0]][end[1]] == '' or self.is_opponent_piece(board, end):
                        possible_moves.append(end)
                        
        return possible_moves 
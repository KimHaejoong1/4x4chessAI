import gym
from gym import spaces
import numpy as np
from chess.domain.board import Board
from chess.engine.game_engine import GameEngine

class Chess4x4Env(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = spaces.Box(low=0, high=10, shape=(4,4), dtype=np.int8)
        self.action_space = spaces.Discrete(16*16)
        self.board = Board()
        self.engine = GameEngine(self.board)
        self.reset()

    def reset(self):
        self.board = Board()
        self.engine = GameEngine(self.board)
        obs = self._get_observation()
        return obs

    def step(self, action):
        from_pos = action // 16
        to_pos = action % 16
        from_row, from_col = divmod(from_pos, 4)
        to_row, to_col = divmod(to_pos, 4)
        # 실제 move 적용 (실제 move 함수에 맞게 수정 필요)
        # 아래는 예시입니다. 실제 move 함수에 맞게 바꿔야 합니다.
        move_result = self.engine.move_selected_piece((from_row, from_col), (to_row, to_col))
        reward = 0
        done = False
        info = {}
        if self.engine.check_detector.is_checkmate(self.board.turn):
            reward = 1
            done = True
        elif self.engine.check_detector.is_stalemate(self.board.turn):
            reward = 0.5
            done = True
        obs = self._get_observation()
        return obs, reward, done, info

    def render(self, mode='human'):
        print(self._get_observation())

    def _get_observation(self):
        obs = np.zeros((4,4), dtype=np.int8)
        for row in range(4):
            for col in range(4):
                piece = self.board.get_piece((row, col))
                if piece:
                    obs[row, col] = piece.to_int()  # to_int()는 Piece 클래스에 직접 구현 필요
        return obs 
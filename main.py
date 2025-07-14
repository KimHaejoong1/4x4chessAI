import sys
from chess.game_controller import GameController

def main():
    # 게임 컨트롤러 초기화 (UI는 내부에서 생성됨)
    game_controller = GameController()
    
    # 게임 실행
    game_controller.run()

if __name__ == "__main__":
    main()

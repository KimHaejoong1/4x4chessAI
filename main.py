import sys
from chess.ui.pygame_ui import PygameUI
from chess.game_controller import GameController

def main():
    # UI 초기화
    ui = PygameUI()
    
    # 게임 컨트롤러 초기화
    game_controller = GameController(ui)
    
    # 게임 실행
    game_controller.run()

if __name__ == "__main__":
    main()

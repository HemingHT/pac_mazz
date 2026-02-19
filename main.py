import asyncio
from pyray import *
from settings import *
from levels import level_1 
from game_board import GameBoard
from player import Player

async def main():

    init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Cookie Mazzster")
    set_target_fps(TARGET_FPS)
    
    board = GameBoard(SCREEN_WIDTH, SCREEN_HEIGHT, level_1)
    
    player = Player(336, 464)

    while not window_should_close():
        
        player.update(board)
        
        begin_drawing()
        clear_background(BLACK)
        
        board.render_level()
        player.draw()
        
        score_text = f"SCORE: {board.score}"
        draw_text(score_text, 10, SCREEN_HEIGHT - 30, 20, WHITE)
        
        end_drawing()

        await asyncio.sleep(0)
    
    unload_texture(player.texture)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())
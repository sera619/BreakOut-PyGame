from src.settings import *
from src.paddle import Paddle
from src.ball import Ball
from src.blocks import GameBlocks
from src.ui_text import InfoText as pt
from src.menu import BDMenu
from src.player import Player

BASE_DIR = os.path.dirname(__file__)
class BreakOut:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode((DISPLAY_W, DISPLAY_H))
        pg.display.set_caption('BreakOut PyGame')
        self.bg_img = pg.image.load(os.path.join(BASE_DIR +'\\assets\\img\\','bg.jpg')).convert_alpha()
        self.bg_img = pg.transform.scale(self.bg_img,(DISPLAY_W, DISPLAY_H))
        self.manager = pgGUI.UIManager((DISPLAY_W , DISPLAY_H), 'theme.json')
        self.state = State.MENU
        self.Menu = BDMenu(self.manager)
        self.Menu.show_mainmenu()
        self.blockboard = GameBlocks(BLOCK_W, BLOCK_H, 5, int(DISPLAY_W // BLOCK_W))
        self.menu_text = pt(self)
        self.paddle = Paddle(PADDLE_W, PADDLE_H, 0, 0, 15)
        self.ball = Ball(10, 10, 7)
        self.ballRect = self.ball.ballRect
        
        self.player = Player("Sera", self.ball._speed)
        self.clock = pg.time.Clock()

        self.running = False
        self.pause = False
        self.game_over = False
        self.game_started = False

        self.score = 0
        self.score_next = LEVEL_BREAKPOINTS['1']
        self.level = 1
        self.broken_blocks = 0
        self.fps = FPS
        self.dx, self.dy = 1, -1


    def check_level_up(self):
        if self.score >= self.score_next:
            self.level +=1
            self.score_next = LEVEL_BREAKPOINTS[str(self.level)] 
        else:
            return

    def update_player(self):
        self.fps += 2
        self.score += self.blockboard.reward_score
        self.broken_blocks += 1
        self.check_level_up()
        self.player.update_player(self.score, self.level, self.broken_blocks)
        self.Menu.show_gameinfo(self.player)

    def start_game(self):
        self.player.update_player(self.score, self.level, self.broken_blocks)
        self.Menu.show_gameinfo(self.player)
        if not self.game_started:
            self.game_started = True
        if self.game_over:
            self.set_gameover(False)
        if not self.ball.active:
            self.ball.set_active(True)
    
    def reset_game(self):
        self.level = 1
        self.score = 0
        self.broken_blocks = 0
        self.game_started = False
        self.score_next = LEVEL_BREAKPOINTS['1']
        self.ball.reset_position(self.screen)
        self.ball.set_active(False)
        self.blockboard.reset_current()
        self.update_player()


    def play_state(self):
        # paddle + ball collision
        if self.ballRect.colliderect(self.paddle) and self.dy > 0:
            self.dx, self.dy = self.check_block_collision(self.dx, self.dy, self.ballRect, self.paddle.rect)

        # block + ball collision
        hit_index = self.ballRect.collidelist(self.blockboard.block_list)
        if hit_index != -1:
            hit_rect = self.blockboard.block_list.pop(hit_index)
            hit_color = self.blockboard.new_color_list.pop(hit_index)
            self.dx, self.dy = self.check_block_collision(self.dx, self.dy, self.ballRect, hit_rect)
            hit_rect.inflate_ip(self.ball.width * 4, self.ball.height * 4)
            pg.draw.rect(self.screen, hit_color, hit_rect)
            self.update_player()

        # paddle controls
        key = pg.key.get_pressed()
        if (key[pg.K_a] or key[pg.K_LEFT]) and self.paddle.rect.left > 10:
            self.paddle.move(MoveDirection.LEFT)
        elif (key[pg.K_d] or key[pg.K_RIGHT]) and self.paddle.rect.right < DISPLAY_W - 10:
            self.paddle.move(MoveDirection.RIGHT)

    def draw(self):
        self.paddle.draw(self.screen)
        self.blockboard.draw(self.screen)

    def check_block_collision(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else: 
            delta_x = rect.right - ball.left
        
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else: 
            delta_y = rect.bottom - ball.top
        
        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def set_gameover(self, state: bool):
        self.game_over = state
        if self.score > self.Menu.best_score:
            self.state = State.NAMEINPUT
            self.Menu.show_highscoreinput()
        print("Game: Gameover: ", state)

    def check_win(self) -> bool:
        if not len(self.blockboard.block_list):
            self.set_gameover(True)
            return True
        return False

    def set_new_highscore(self):
        if not self.Menu.score_name_input.get_text() == "":
            self.Menu.data.add_new_highscore(self.Menu.score_name_input.get_text(), self.score)
            self.Menu.highscores = self.Menu.data.load()
            self.Menu.best_score = self.Menu.data.get_best_score(self.Menu.highscores)
            print("Game: Highscore saved!")

    def reset_screen(self):
        self.screen.blit(self.bg_img,(0,0))

    def run(self):
        self.running = True
        self.state = State.MENU
        while self.running:                
            time_delta = self.clock.tick(self.fps) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.state == State.INGAME):
                    self.running = False


                
                # keyboard events
                if event.type == pg.KEYUP:
                    k = event.key
                    if k ==  pg.K_p:
                        if self.game_started:                                
                            self.pause = not self.pause
                            if self.ball.active and self.pause:
                                self.ball.set_active(False)
                                print("Game paused!")
                            else:
                                self.ball.set_active(True)
                    elif k == pg.K_ESCAPE and self.state == State.INGAME:
                        self.reset_game()
                        self.Menu.show_mainmenu()
                        self.state = State.MENU
                    elif k == pg.K_RETURN and self.state == State.INGAME and self.game_over:
                        self.start_game()
                    elif k == pg.K_RETURN and self.state == State.INGAME and not self.game_started:
                        self.start_game()

                # Menu Button events
                if event.type == pgGUI.UI_BUTTON_PRESSED:
#                    if event.user_type == pgGUI.UI_BUTTON_PRESSED:
                    if event.ui_element == self.Menu.highscore_button:
                        self.Menu.show_score()
                        self.state = State.HIGHSCORE
                        print("Highscore pressed")
                    elif event.ui_element == self.Menu.nameinput_button:
                        self.set_new_highscore()
                        self.reset_game()
                        self.Menu.show_score()
                        self.state = State.HIGHSCORE
                    elif event.ui_element == self.Menu.play_button:
                        self.Menu.show_gameinfo(self.player)
                        self.state = State.INGAME

                    elif event.ui_element == self.Menu.score_backbutton:
                        self.Menu.show_mainmenu()
                        self.state = State.MENU

                    # elif event.ui_element == self.Menu.test_button:
                    #     self.Menu.show_highscoreinput()
                    #     self.state = State.NAMEINPUT


                    elif event.ui_element == self.Menu.exit_button:
                        self.running = False


                self.manager.process_events(event)

            # set backup img


            self.reset_screen()
            if self.state == State.MENU:
                #self.Menu.run()
                self.manager.draw_ui(self.screen)
            elif self.state == State.HIGHSCORE:
                self.manager.draw_ui(self.screen)
            elif self.state == State.NAMEINPUT:
                self.manager.draw_ui(self.screen)
            elif self.state == State.INGAME:
                self.draw()
                #self.menu_text.draw_infotext()
                self.manager.draw_ui(self.screen)
                if not self.game_started:
                    self.menu_text.draw_startText()
                self.ball.move(self.screen, self)

                if self.pause:
                    self.draw()
                    self.menu_text.draw_pause()
                elif self.game_over:
                    self.draw()
                    self.menu_text.draw_gameover()
                else:
                    self.play_state()
            self.manager.update(time_delta)

            pg.display.update()
            self.clock.tick(self.fps)
        
        pg.quit()


    


if __name__ == '__main__':
    game = BreakOut()
    try:
        game.run()
    except KeyboardInterrupt:
        print("ESC Breakout Game")
        pg.quit()

    

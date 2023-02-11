from src.settings import *


class Ball(object):
    def __init__(self, width, height, speed=0):
        self.width = width
        self.height = height
        self.active = False
        self._speed: int = speed
        self.radius = 20
        self.ball_rect = int(self.radius * 2 ** 0.5)
        self.ballRect = pg.Rect(random.randrange(self.ball_rect, GAMEFIELD_W - self.ball_rect), (GAMEFIELD_H - MENU_H)  // 2, self.ball_rect, self.ball_rect)

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value: int):
        self._speed = value

    def update_position(self, screen):
        pg.draw.circle(screen, pg.Color('orange'), self.ballRect.center, self.radius)

    def reset_position(self, screen):
        pg.draw.circle(screen, pg.Color('orange'), self.ballRect.center, self.radius)

    def check_collision(self, mainframe):
        if self.ballRect.centerx < self.radius or self.ballRect.centerx > GAMEFIELD_W - self.radius:
            mainframe.dx = - mainframe.dx

        if self.ballRect.centery < self.radius: 
            mainframe.dy = - mainframe.dy    
        if self.ballRect.centery > (GAMEFIELD_H - MENU_H) + self.radius:
            mainframe.set_gameover(True)
            self.set_active(False)
            print("Game Over")

    def move(self, screen, mainframe):
        if self.active:
            self.update_position(screen)
            self.ballRect.x += self._speed * mainframe.dx
            self.ballRect.y += self._speed * mainframe.dy
            
            self.check_collision(mainframe)
        else:
            self.update_position(screen)
    

    def set_active(self, active: bool):
        self.active = active
        print("Ball active: ", self.active)
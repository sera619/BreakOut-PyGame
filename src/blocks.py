from src.settings import *


class GameBlocks:
    def __init__(self, width, height, rows: int, column: int) -> None:
        self.width = width
        self.height = height
        self.rows = rows
        self.column = column
        self.reward_score = 120
        self.block_list = [pg.Rect(10 + (self.width + 10) * i, 10 + (self.height + 5 )* j, self.width, self.height) for i in range(column) for j in range(rows)]
        self.color_list = [(255, 0, random.randrange(1, 256)) for i in range(column) for j in range(rows)]
        self.new_color_list =[(BLOCK_COLORS[random.randint(0, 7)]) for x in self.block_list]

    def reset_current(self):
        self.block_list = [pg.Rect(10 + (self.width + 5 ) * i, 10 + (self.height + 5 )* j, self.width, self.height) for i in range(self.column) for j in range(self.rows)]
        self.new_color_list =[(BLOCK_COLORS[random.randint(0, 7)]) for x in self.block_list]

    def draw(self, screen):
        [pg.draw.rect(screen, self.new_color_list[color], block) for color, block in enumerate(self.block_list)]
    

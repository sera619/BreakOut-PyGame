from src.settings import *

@dataclass
class Player:
    name: str
    score: int = 0
    level: int = 0
    broken_blocks: int  = 0
    speed: int = 0
    def __init__(self, name, speed) -> None:
        self.name = name
        self.speed = speed
    
    def update_player(self, score: int, level: int, blocks: int):
        self.score = score
        self.level = level
        self.broken_blocks = blocks
    
    def reset_player(self):
        self.score = 0
        self.level = 0
        self.broken_blocks = 0
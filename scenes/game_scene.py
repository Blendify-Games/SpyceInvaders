import pygame

from scenes import Scene

from game_instance import game_instance
from gameobj.invaders import (
    OctopusInvader, SquidInvader,
    CrabInvader, UFOInvader
)
from res.config import SCREEN_SIZE
from res.util import sprite_sheet, get_text, change_surf_color
from res.util import SPRITE_SIZE
from scenes.writing import TextWrite

class _ScoreBoard(TextWrite):
    def __init__(self, render_group:pygame.sprite.Group):
        text = TextWrite(render_group, 'Score', 
                    (SCREEN_SIZE[0]*0.4, SCREEN_SIZE[1]*0.05))
        change_surf_color(text.image, '#f59342')
        super().__init__(render_group, '0000', 
                    (SCREEN_SIZE[0]*0.58, SCREEN_SIZE[1]*0.05))
        self.score_points = 0
    def add_to_score(self, v:int):
        self.score_points += v
        self.setup_text(f'{self.score_points:04d}')

class GameScene(Scene):
    def setup(self):
        self.score = _ScoreBoard(self.render_group)
        game_instance().game_input.set_keypressing({
            pygame.K_u: self.test
        })
    def test(self):
        self.score.add_to_score(30)
    def when_unload_do(self):
        pass
    def update(self):
        super().update()

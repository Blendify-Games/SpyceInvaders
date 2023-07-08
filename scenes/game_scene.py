import pygame

from scenes import Scene

from game_instance import game_instance
from gameobj.invaders import (
    OctopusInvader, SquidInvader,
    CrabInvader, UFOInvader
)
from res.util import sprite_sheet, get_text, change_surf_color
from res.util import SPRITE_SIZE

class GameScene(Scene):
    def setup(self):
        i1 = OctopusInvader(self.render_group)
        i2 = SquidInvader(self.render_group)
        i3 = CrabInvader(self.render_group)
        i4 = UFOInvader(self.render_group)
        i2.rect.topleft = SPRITE_SIZE[0] * 2, SPRITE_SIZE[1]
        i3.rect.topleft = SPRITE_SIZE[0] * 4, SPRITE_SIZE[1] * 2
        i4.rect.topleft = SPRITE_SIZE[0] * 6, SPRITE_SIZE[1] * 3
        self.__text = get_text('Blendifý Games')
        game_instance().game_input.set_keypressing({
            pygame.K_1: i1.kill,
            pygame.K_2: i2.kill,
            pygame.K_3: i3.kill,
            pygame.K_4: i4.kill,
        })
    def when_unload_do(self):
        pass
    def update(self):
        super().update()
        self.screen.blit(self.__text, (100, 500))

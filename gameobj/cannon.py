import pygame
from res.config import ENTITY_COLORS
from res.util import get_sprite_block, change_surf_color
from gameobj.explosion import Explosion
from gameobj.shot import ShotObject

class Cannon(pygame.sprite.Sprite):
    def __init__(self, *groups:'render_group, ...'):
        super().__init__(*groups)
        self.__groups = groups
        self.image = get_sprite_block('cannon')
        change_surf_color(self.image, ENTITY_COLORS['cannon'])
        self.rect = self.image.get_rect()
    def kill(self):
        explosion = Explosion(
            self.rect, self.__groups[0],
            iterate_over=['explosion_4', 'explosion_5'],
            number_iterations=5,
            time_between_frame=100
        )
        super().kill()
    def shoot(self, shot_group:pygame.sprite.Group):
        shot = ShotObject(self.rect, 
                    (self.__groups[0], shot_group),
                    'shot_3')
        shot.set_direction(go_up=True)

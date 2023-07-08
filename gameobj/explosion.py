import pygame

from res.config import (
    SPRITE_SIZE,
    EXPLOSION_COLOR
)
from res.util import (
    change_surf_color,
    get_sprite_block
)

class Explosion(pygame.sprite.Sprite):
    '''
    This class represents a generic explosion 
    sprite. Everytime an invader is killed, 
    this sprite runs for 200ms before 
    autodestruction.
    '''
    def __init__(self, posrect:pygame.Rect,
                    render_group:pygame.sprite.Group,
                    exptype:str='explosion_0'):
        super().__init__(render_group)
        self.type = exptype
        self.image = get_sprite_block(exptype)
        self.rect = self.image.get_rect()
        change_surf_color(self.image, EXPLOSION_COLOR)
        self.rect.center = posrect.center
        self.__time = pygame.time.get_ticks()
    def update(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 200:
            self.kill()
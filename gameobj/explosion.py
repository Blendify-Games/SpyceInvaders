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
                    exptype:str='explosion_0',
                    iterate_over:'list_of_explosion_keys'=None,
                    number_iterations:int=1,
                    time_between_frame:int=200):
        super().__init__(render_group)
        self.index = 0
        self.time_between_frame = time_between_frame
        self.number_iterations = number_iterations
        self.image_list = []
        self.iterate_over = iterate_over
        if not self.iterate_over:
            self.iterate_over = [exptype]
        for key in self.iterate_over:
            img = get_sprite_block(key)
            change_surf_color(img, EXPLOSION_COLOR)
            self.image_list.append(img)
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = posrect.center
        self.__time = pygame.time.get_ticks()
    def update(self):
        t = pygame.time.get_ticks()
        if t - self.__time > self.time_between_frame:
            self.index = (self.index + 1) % len(self.image_list)
            self.image = self.image_list[self.index]
            if self.index < 1:
                self.number_iterations -= 1
            if self.number_iterations < 1:
                self.kill()
            self.__time = t

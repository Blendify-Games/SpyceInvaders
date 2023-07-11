import pygame
import random
from gameobj.explosion import Explosion
from res.config import SCREEN_SIZE, SHOT_COLORS
from res.util import get_sprite_block, change_surf_color

class ShotObject(pygame.sprite.Sprite):
    '''
    This class is instantiated by an entity
    and represents the shot object.
    There are three types of shots, shot_0, shot_1,
    and shot_2
    '''
    _SPEED_Y = 10
    LIMIT = (0, SCREEN_SIZE[1])
    def __init__(self, posrect:pygame.Rect,
                    groups:'render_group, shot_group',
                    shot_type:str='shot_0'):
        super().__init__(*groups)
        self.__groups = groups
        self.__time = pygame.time.get_ticks()
        self.__shot_type = shot_type
        self.__build_sprite_image()
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = posrect.center
        self.__time = pygame.time.get_ticks()
        self.explosion_type = 'explosion_2' \
                                if self.__shot_type == 'shot_3' \
                                else 'explosion_1'
    def set_direction(self, go_up:bool):
        ''' if go_up is true the shot direction
        is up, otherwise it is down'''
        speed = abs(self._SPEED_Y)
        self._SPEED_Y = -speed if go_up else speed
    def __build_sprite_image(self):
        img = get_sprite_block(self.__shot_type)
        w, h = img.get_rect().size
        self.image_list = [
            img.subsurface((0, 0, w//4, h)),
            img.subsurface((w//4, 0, w//4, h)),
            img.subsurface((w//2, 0, w//4, h)),
            img.subsurface((w//2 + w//4, 0, w//4, h)),
        ]
    def miss(self):
        explosion = Explosion(
            self.rect, self.__groups[0],
            self.explosion_type
        )
        super().kill()
    def update(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 10:
            self.index = (self.index + 1) % len(self.image_list)
            self.image = self.image_list[self.index]
            self.__time = t
        self.rect.centery += self._SPEED_Y
        if self.rect.top < self.LIMIT[0] or \
            self.rect.bottom > self.LIMIT[1]:
            self.miss()

class InvaderShotObject(ShotObject):
    def __init__(self, posrect:pygame.Rect,
                    groups:'render_group, shot_group'):
        shot_type = random.choice(['shot_0', 'shot_1', 'shot_2'])
        super().__init__(posrect, groups, shot_type)
        choice = random.choice(SHOT_COLORS)
        for img in self.image_list:
            change_surf_color(img, choice)

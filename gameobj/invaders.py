import pygame
import random
from gameobj.explosion import Explosion
from game_instance import game_instance
from res import SPRITE_MAP
from res.config import (
    SPRITE_SIZE, INVADER_COLORS,
    SHOT_COLORS, FLOOR
)
from res.util import (
    change_surf_color,
    get_sprite_block
)

class _InvaderShot(pygame.sprite.Sprite):
    '''
    This class is instantiated by the Invader
    and represents the shot object.
    There are three types of shots, shot_0, shot_1,
    and shot_2
    '''
    speed_y = 10
    def __init__(self, posrect:pygame.Rect,
                    groups:'GroupList',
                    shot_type:str='shot_0'):
        super().__init__(*groups)
        self.__groups = groups
        self.__time = pygame.time.get_ticks()
        self.__shot_type = shot_type
        self.__build_sprite_image()
        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = posrect.center
        self.__time = pygame.time.get_ticks()
    def __build_sprite_image(self):
        img = get_sprite_block(self.__shot_type)
        w, h = img.get_rect().size
        self.image_list = [
            img.subsurface((0, 0, w//4, h)),
            img.subsurface((w//4, 0, w//4, h)),
            img.subsurface((w//2, 0, w//4, h)),
            img.subsurface((w//2 + w//4, 0, w//4, h)),
        ]
        choice = random.choice(SHOT_COLORS)
        for img in self.image_list:
            change_surf_color(img, choice)
    def kill(self):
        explosion = Explosion(
            self.rect, self.__groups[0],
            'explosion_1'
        )
        super().kill()
    def update(self):
        t = pygame.time.get_ticks()
        if t - self.__time > 10:
            self.index = (self.index + 1) % len(self.image_list)
            self.image = self.image_list[self.index]
            self.__time = t
        self.rect.centery += self.speed_y
        if self.rect.bottom > FLOOR:
            self.kill()

class Invader(pygame.sprite.Sprite):
    '''
    This class represents a generic invader sprite.
    sprite_refs must be a name in res.SPRITE_MAP.
    For each sprite_ref key in res.SPRITE_MAP, 
    it may contain an entry that has left (L) 
    and right (R) attributes.

    Invader(groups, *sprite_refs: str)
    '''
    def __init__(self, groups:'GroupList', *sprite_refs:str):
        super().__init__(*groups)
        self.__groups = groups
        self.index = 0
        self.__build_image_list(*sprite_refs)
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect()
        self.__t = pygame.time.get_ticks()
        self.__time_speed = 500
        self.__color = '#ffffff'
        self.speed = self.rect.w//4
        self._explosion_key = 'explosion_0'
    def __build_image_list(self, *sprite_refs:str):
        w, h = SPRITE_SIZE
        self.image_list = []
        for sn in sprite_refs:
            img = get_sprite_block(sn)
            self.image_list.append(img)
    def shot(self):
        shot = _InvaderShot(
            self.rect, self.__groups,
            random.choice(['shot_0', 'shot_1', 'shot_2'])
        )
    def kill(self):
        explosion = Explosion(
            self.rect, self.__groups[0],
            self._explosion_key
        )
        super().kill()
    def set_color(self, color:'color_value'):
        for img in self.image_list:
            change_surf_color(img, color, self.__color)
        self.__color = color
    def update_sprite(self):
        self.index = (self.index + 1) % len(self.image_list)
        self.image = self.image_list[self.index]
    def move(self, x_inv:bool=False, y:bool=False):
        if x_inv:
            self.speed = -self.speed
        self.rect.x += self.speed
        if y:
            self.rect.y += abs(self.speed)
        self.update_sprite()

class CrabInvader(Invader):
    '''
    This class represents a crab invader.
    '''
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(groups, 'crab_1', 'crab_2')
        self.set_color(INVADER_COLORS['crab_invader'])

class OctopusInvader(Invader):
    '''
    This class represents a octopus invader.
    '''
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(groups, 'octopus_1', 'octopus_2')
        self.set_color(INVADER_COLORS['octopus_invader'])

class SquidInvader(Invader):
    '''
    This class represents a squid invader.
    '''
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(groups, 'squid_1', 'squid_2')
        self.set_color(INVADER_COLORS['squid_invader'])

class UFOInvader(Invader):
    '''
    This class represents a ufo invader.
    '''
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(groups, 'ufo')
        self.set_color(INVADER_COLORS['ufo_invader'])
        self._explosion_key = 'explosion_3'

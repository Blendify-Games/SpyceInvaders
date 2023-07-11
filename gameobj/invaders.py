import pygame
import random
from game_instance import game_instance
from gameobj.explosion import Explosion
from gameobj.shot import InvaderShotObject
from res import SPRITE_MAP
from res.config import (
    SPRITE_SIZE, ENTITY_COLORS,
    SHOT_COLORS, SCREEN_SIZE
)
from res.util import (
    change_surf_color,
    get_sprite_block
)

class Invader(pygame.sprite.Sprite):
    '''
    This class represents a generic invader sprite.
    sprite_refs must be a name in res.SPRITE_MAP.
    For each sprite_ref key in res.SPRITE_MAP, 
    it may contain an entry that has left (L) 
    and right (R) attributes.

    Invader(groups, *sprite_refs: str)
    '''
    SCORE_POINT = 0 # score point value
    def __init__(self, groups:'render_group, ...', 
                *sprite_refs:str):
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
    def shoot(self, shot_group:pygame.sprite.Group, limit:tuple=None):
        shot = InvaderShotObject(self.rect, (self.__groups[0], shot_group))
        if limit:
            shot.LIMIT = limit
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
    def change_direction(self):
        self.speed = -self.speed
    def move(self, down:bool=False):
        if down:
            self.rect.y += abs(self.speed)
        else:
            self.rect.x += self.speed
        self.update_sprite()

class UFOInvader(Invader):
    '''
    This class represents a ufo invader.
    '''
    def __init__(self, *groups:'render_group, ...'):
        super().__init__(groups, 'ufo')
        self.SCORE_POINT = 50
        self.set_color(ENTITY_COLORS['ufo_invader'])
        self._explosion_key = 'explosion_3'
        self.speed = 2
    def move_until_limits(self, limits:tuple=(0, SCREEN_SIZE[0])) -> bool:
        '''move ufo until beyond its limits and then invert his
        direction. If reached limit this method returns true.'''
        reached_limit = False
        if (self.speed > 0 and self.rect.left - 10 > limits[1]) or \
            (self.speed < 0 and self.rect.right + 10 < limits[0]):
            self.change_direction()
            reached_limit = True
        self.move()
        return reached_limit

class SquidInvader(Invader):
    '''
    This class represents a squid invader.
    '''
    def __init__(self, *groups:'render_group, ...'):
        super().__init__(groups, 'squid_1', 'squid_2')
        self.SCORE_POINT = 30
        self.set_color(ENTITY_COLORS['squid_invader'])

class CrabInvader(Invader):
    '''
    This class represents a crab invader.
    '''
    def __init__(self, *groups:'render_group, ...'):
        super().__init__(groups, 'crab_2', 'crab_1')
        self.SCORE_POINT = 20
        self.set_color(ENTITY_COLORS['crab_invader'])

class OctopusInvader(Invader):
    '''
    This class represents a octopus invader.
    '''
    def __init__(self, *groups:'render_group, ...'):
        super().__init__(groups, 'octopus_2', 'octopus_1')
        self.SCORE_POINT = 10
        self.set_color(ENTITY_COLORS['octopus_invader'])

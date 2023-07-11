import pygame
from res.config import ENTITY_COLORS
from res.util import get_sprite_block, change_surf_color

class Hangar(pygame.sprite.Sprite):
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(*groups)
        self.image = get_sprite_block('hangar')
        self.rect = self.image.get_rect()
        change_surf_color(self.image, ENTITY_COLORS['hangar'])
        self.mask = pygame.mask.from_surface(self.image)
    def subtract_by_collision(self, shot:'ShotObject'):
        img = get_sprite_block(shot.explosion_type)
        change_surf_color(img, ENTITY_COLORS['hangar'])
        pos = (abs(self.rect.left - shot.rect.left)-5,
                abs(self.rect.top - shot.rect.top)-12)
        self.image.blit(img, pos, 
                special_flags=pygame.BLEND_RGBA_SUB)
        self.mask = pygame.mask.from_surface(self.image)
        shot.miss()

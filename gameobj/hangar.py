import pygame
from res.config import ENTITY_COLORS
from res.util import get_sprite_block, change_surf_color

class Hangar(pygame.sprite.Sprite):
    def __init__(self, *groups:pygame.sprite.Group):
        super().__init__(*groups)
        self.image = get_sprite_block('hangar')
        self.rect = self.image.get_rect()
        change_surf_color(self.image, ENTITY_COLORS['hangar'])

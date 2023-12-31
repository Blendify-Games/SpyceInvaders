import pygame
from res.config import SCREEN_SIZE
from res.util import get_text, get_sprite_block

class TextWrite(pygame.sprite.Sprite):
    def __init__(self, 
            render_group:pygame.sprite.Group,
            text:str,
            centerpos:tuple=(
                SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2),
            step_writing_time:int=0, wait_to_begin:int=0):
        super().__init__(render_group)
        self.step_writing_time = step_writing_time
        self.wait_to_begin = wait_to_begin
        self.step_index = 0
        self.text = text
        if self.step_writing_time:
            self.image = get_text(' '*len(self.text))
        else:
            self.image = get_text(self.text)
        self.rect = self.image.get_rect()
        self.rect.center = centerpos
        self.__time = pygame.time.get_ticks()
        self.__wait_time = pygame.time.get_ticks()
        self.__must_wait = self.wait_to_begin > 0
    def setup_text(self, text:str):
        pos = self.rect.topleft
        self.image = get_text(text)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update(self):
        if self.step_writing_time > 0:
            t = pygame.time.get_ticks()
            if self.__must_wait and t - self.__wait_time > self.wait_to_begin:
                self.__must_wait = False
            if(not self.__must_wait and 
                self.step_index < len(self.text)+1 and
                t - self.__time > self.step_writing_time):
                self.setup_text(self.text[0:self.step_index])
                self.step_index += 1
                self.__time = t

class Figure(pygame.sprite.Sprite):
    def __init__(self, 
            render_group:pygame.sprite.Group,
            figure_key:str,
            centerpos:tuple=(
                SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2),
            fadein:bool=False):
        super().__init__(render_group)
        self.image = get_sprite_block(figure_key)
        self.rect = self.image.get_rect()
        self.rect.center = centerpos
        self.__fadein = fadein
        self.__image_alpha = 0
        if self.__fadein:
            self.image.set_alpha(self.__image_alpha)
        self.__time = pygame.time.get_ticks()
        self.__init_time = pygame.time.get_ticks()
    def update(self):
        if self.__fadein and self.__image_alpha < 255:
            self.image.set_alpha(self.__image_alpha)
            t = pygame.time.get_ticks()
            if t - self.__time > 15:
                self.__image_alpha += 4
                self.__time = t

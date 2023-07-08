import pygame
from res.config import SCREEN_SIZE
from res.util import get_text

class TextWrite(pygame.sprite.Sprite):
    def __init__(self, 
            render_group:pygame.sprite.Group,
            text:str,
            centerpos:tuple=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2),
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
